#!/usr/bin/env python3
"""Probe a media file and optionally create key frames/contact sheet.

Usage:
  python media_probe.py video.mp4 --out review-dir

Requires ffprobe. Requires ffmpeg only when --out is provided.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", help="Directory for frames/contact sheet")
    ap.add_argument("--frames", default="1,4,8", help="Comma-separated timestamps in seconds")
    args = ap.parse_args()
    video = Path(args.video).resolve()
    if not video.exists():
        print(f"FAIL missing video: {video}")
        return 1
    if shutil.which("ffprobe") is None:
        print("FAIL ffprobe not found")
        return 1
    p = run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,r_frame_rate,codec_name", "-show_entries", "format=duration,size", "-of", "json", str(video)])
    if p.returncode:
        print("FAIL ffprobe", p.stderr.strip())
        return 1
    meta = json.loads(p.stdout)
    print(json.dumps(meta, indent=2))
    if args.out:
        if shutil.which("ffmpeg") is None:
            print("FAIL ffmpeg not found")
            return 1
        out = Path(args.out).resolve()
        out.mkdir(parents=True, exist_ok=True)
        frame_paths = []
        for raw in args.frames.split(','):
            ts = raw.strip()
            frame = out / f"frame-{ts.replace('.', '_')}.jpg"
            p = run(["ffmpeg", "-y", "-ss", ts, "-i", str(video), "-frames:v", "1", str(frame)])
            if p.returncode:
                print(f"FAIL frame at {ts}: {p.stderr.strip()}")
                return 1
            frame_paths.append(frame)
        sheet = out / "contact-sheet.jpg"
        p = run(["ffmpeg", "-y", *sum((["-i", str(f)] for f in frame_paths), []), "-filter_complex", f"tile={len(frame_paths)}x1", str(sheet)])
        if p.returncode:
            print("WARN contact sheet failed:", p.stderr.strip())
        else:
            print(f"Contact sheet: {sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
