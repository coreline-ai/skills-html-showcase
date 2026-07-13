#!/usr/bin/env python3
"""
new_project.py — bizplan 프로젝트 폴더 스캐폴딩 (PRD §22 구조 + project.json)

사용:
  python3 new_project.py --dir <작업디렉토리> --slug <영문slug> \
      --name "<프로젝트명>" --type "<문서유형>" --org "<신청기관>" --deadline "YYYY-MM-DD"

산출물 위치 매핑은 SKILL.md "프로젝트 스캐폴딩" 섹션의 단일 출처와 일치해야 한다.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

# PRD §22 — 프로젝트 폴더 구조 (단일 출처)
DIRS = [
    "00-source/notice",
    "00-source/attachments",
    "00-source/templates",
    "00-source/company",
    "00-source/user-files",
    "01-notice-analysis",
    "02-interview",
    "03-idea-and-title",
    "04-research/market",
    "04-research/competitors",
    "04-research/technology",
    "04-research/patents",
    "04-research/papers",
    "05-business-core",
    "06-template-design",
    "07-diagrams/diagram-source",
    "07-diagrams/images",
    "08-draft",
    "09-audit",
    "10-final",
]

# 문서 유형 → 평가 가중 라벨 (SKILL.md 발동 3번 표와 일치)
DOC_TYPES = {
    "정부지원", "중소기업지원", "R&D", "산학협력",
    "투자덱", "기업제안", "공공제안", "내부신사업", "자유형식",
}

# 프로젝트 산출물 기본 위치 = 스킬 폴더 내 dist/ (2026-06-17 작가님 지시)
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DIST = os.path.join(SKILL_ROOT, "dist")


def main() -> int:
    ap = argparse.ArgumentParser(description="bizplan 프로젝트 스캐폴딩")
    ap.add_argument("--dir", default=DEFAULT_DIST, help="프로젝트를 만들 디렉토리(기본: 스킬 폴더 내 dist/)")
    ap.add_argument("--slug", required=True, help="영문 slug (폴더명 bizplan-<slug>)")
    ap.add_argument("--name", default="", help="프로젝트명")
    ap.add_argument("--type", default="자유형식", help="문서 유형")
    ap.add_argument("--org", default="", help="신청 기관/제출 대상")
    ap.add_argument("--deadline", default="", help="마감일 YYYY-MM-DD")
    ap.add_argument("--notice", default="", help="공고명 또는 URL")
    ap.add_argument("--force", action="store_true", help="이미 있어도 진행(덮어쓰지 않고 누락 폴더만 생성)")
    args = ap.parse_args()

    root = os.path.abspath(os.path.join(args.dir, f"bizplan-{args.slug}"))
    pj_path = os.path.join(root, "project.json")

    if os.path.exists(pj_path) and not args.force:
        print(f"[중단] 이미 존재: {pj_path}\n  --force 로 누락 폴더만 보강할 수 있습니다.", file=sys.stderr)
        return 1

    if args.type not in DOC_TYPES:
        print(f"[경고] 알 수 없는 문서 유형 '{args.type}'. 허용: {sorted(DOC_TYPES)}", file=sys.stderr)

    for d in DIRS:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    # 기존 project.json 보존(상태 유지), 없으면 새로 생성
    if os.path.exists(pj_path):
        with open(pj_path, encoding="utf-8") as f:
            meta = json.load(f)
        meta.setdefault("scaffold_repaired_at", _now())
    else:
        meta = {
            "project_id": f"bizplan-{args.slug}",
            "project_name": args.name,
            "slug": args.slug,
            "document_type": args.type,
            "organization": args.org,
            "deadline": args.deadline,
            "notice": args.notice,
            "created_at": _now(),
            "status": "created",  # created→notice_analyzed→interviewed→researched→core_locked→drafted→audited→final
            "gates_passed": [],   # ["gate0","gate1",...]
            "outputs": {},        # 단계별 산출 파일 경로 기록
        }

    with open(pj_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # business-core.yaml 시드 복사 (없을 때만)
    core_dst = os.path.join(root, "05-business-core", "business-core.yaml")
    if not os.path.exists(core_dst):
        seed = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates", "business-core.yaml")
        if os.path.exists(seed):
            with open(seed, encoding="utf-8") as s, open(core_dst, "w", encoding="utf-8") as d:
                d.write(s.read())

    print(f"[완료] 프로젝트 생성: {root}")
    print(f"  - project.json (status={meta['status']})")
    print(f"  - {len(DIRS)}개 폴더 + business-core.yaml 시드")
    return 0


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


if __name__ == "__main__":
    raise SystemExit(main())
