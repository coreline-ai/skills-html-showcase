#!/usr/bin/env python3
"""Verify a rendered manual tutorial video and optional lesson HTML.

Usage:
  python verify-video-artifact.py media/videos/lesson.mp4 [lesson.html]

Checks:
- ffprobe can read the video
- dimensions/duration/fps are non-empty
- file size is plausible
- optional HTML references the video path
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def ffprobe(path: Path) -> dict:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,codec_name,duration",
        "-show_entries", "format=duration,size",
        "-of", "json", str(path),
    ]
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip())
    return json.loads(p.stdout)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip())
        return 2
    video = Path(sys.argv[1]).resolve()
    if not video.exists():
        print(f"FAIL missing video: {video}")
        return 1
    if video.stat().st_size < 1024:
        print(f"FAIL video too small: {video.stat().st_size} bytes")
        return 1
    try:
        meta = ffprobe(video)
    except Exception as exc:
        print(f"FAIL ffprobe: {exc}")
        return 1
    streams = meta.get("streams") or []
    if not streams:
        print("FAIL no video stream")
        return 1
    stream = streams[0]
    width, height = stream.get("width"), stream.get("height")
    duration = float((meta.get("format") or {}).get("duration") or stream.get("duration") or 0)
    if not width or not height or duration <= 0:
        print(f"FAIL invalid metadata: width={width} height={height} duration={duration}")
        return 1
    print(f"PASS video metadata: {width}x{height}, {duration:.2f}s, codec={stream.get('codec_name')}, fps={stream.get('r_frame_rate')}")

    if len(sys.argv) >= 3:
        html = Path(sys.argv[2]).resolve()
        if not html.exists():
            print(f"FAIL missing html: {html}")
            return 1
        text = html.read_text(encoding="utf-8", errors="ignore")
        if video.name not in text and str(video) not in text:
            print(f"FAIL html does not reference video filename: {video.name}")
            return 1
        print("PASS html references video filename")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
