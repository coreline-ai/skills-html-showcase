#!/usr/bin/env python3
"""
validate_project.py — bizplan 프로젝트 자동 검증 게이트 (PRD §19·§20, SKILL.md 게이트)

진단용 리포트다. 차단(exit≠0)하지 않는다. 게이트별 ✓/✗/⚠ 를 보고하고
사용자가 어느 단계를 보강해야 하는지 알려준다.

사용:
  python3 validate_project.py <bizplan-slug 디렉토리>

점검 항목:
  1) project.json 존재 + status 유효
  2) 폴더 구조 완전성 (new_project.py DIRS 기준)
  3) business-core.yaml 의 [확인 필요] 잔존 개수
  4) 게이트별 필수 산출물 파일 존재 여부
  5) business-core.yaml 모호어("많은/효율적/혁신적/대폭" 등) 탐지
  6) source-index.xlsx 행 수 (출처 0이면 경고)
"""
import json
import os
import re
import sys

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

try:
    import openpyxl
    _HAS_OPENPYXL = True
except ImportError:
    _HAS_OPENPYXL = False


# new_project.py DIRS 와 동일 (단일 출처)
EXPECTED_DIRS = [
    "00-source/notice", "00-source/attachments", "00-source/templates",
    "00-source/company", "00-source/user-files",
    "01-notice-analysis", "02-interview", "03-idea-and-title",
    "04-research/market", "04-research/competitors", "04-research/technology",
    "04-research/patents", "04-research/papers",
    "05-business-core", "06-template-design",
    "07-diagrams/diagram-source", "07-diagrams/images",
    "08-draft", "09-audit", "10-final",
]

VALID_STATUS = [
    "created", "notice_analyzed", "interviewed", "researched",
    "core_locked", "drafted", "audited", "final",
]

# Gate 0 — 공고 분석 8 산출물 (SKILL.md / references/01-notice-analysis.md)
GATE0_FILES = [
    "01-notice-analysis/notice-summary.md",
    "01-notice-analysis/eligibility-check.md",
    "01-notice-analysis/evaluation-criteria.md",
    "01-notice-analysis/required-documents.md",
    "01-notice-analysis/budget-rules.md",
    "01-notice-analysis/schedule.md",
    "01-notice-analysis/format-constraints.md",
    "01-notice-analysis/disqualification-risks.md",
]

# 게이트별 필수 산출물 (대표 파일. 전수 아님 — 핵심 게이트 통과 신호)
GATE_OUTPUTS = {
    "Gate 0 (공고 분석)": GATE0_FILES,
    "Gate 1 (인터뷰)": [
        "02-interview/idea-brief.md",
        "02-interview/interview-summary.md",
        "02-interview/confirmed-facts.md",
        "03-idea-and-title/title-candidates.md",
    ],
    "Gate 2 (리서치)": [
        "03-idea-and-title/research-plan.md",
        "04-research/research-report.md",
        "04-research/source-index.xlsx",
    ],
    "Gate 3·4 (코어/숫자)": [
        "05-business-core/business-core.yaml",
        "05-business-core/evidence-ledger.xlsx",
        "05-business-core/market-sizing.xlsx",
        "05-business-core/financial-model.xlsx",
    ],
    "Gate 6 (서식/다이어그램)": [
        "06-template-design/template-structure.yaml",
        "06-template-design/template-map.yaml",
        "06-template-design/section-outline.md",
    ],
    "Draft (초안)": [
        "08-draft/business-plan-draft.docx",
    ],
    "Gate 5·7 (검증)": [
        "09-audit/scorecard.md",
        "09-audit/revision-log.md",
    ],
    "Final (출력)": [
        "10-final/final-business-plan.html",  # 유형 무관 항상 생성(의존성 0)
        "10-final/submission-checklist.md",
    ],
}

# 모호어 — 인터뷰/코어 단계에서 수치·사례로 구체화해야 할 표현 (SKILL.md §116)
VAGUE_WORDS = [
    "많은", "다양한", "효율적", "효율화", "혁신적", "혁신", "대폭", "상당한",
    "최고", "최첨단", "최적", "획기적", "글로벌", "차별화된", "압도적",
    "수많은", "탁월한", "선도적", "독보적", "고도화",
]

# [확인 필요] 마커 (대괄호 유무 모두)
NEEDS_CHECK_RE = re.compile(r"\[?\s*확인\s*필요\s*\]?")


# ----------------------------------------------------------------------------
class Report:
    def __init__(self):
        self.lines = []
        self.pass_n = 0
        self.fail_n = 0
        self.warn_n = 0

    def ok(self, msg):
        self.lines.append(f"  ✓ {msg}")
        self.pass_n += 1

    def fail(self, msg):
        self.lines.append(f"  ✗ {msg}")
        self.fail_n += 1

    def warn(self, msg):
        self.lines.append(f"  ⚠ {msg}")
        self.warn_n += 1

    def info(self, msg):
        self.lines.append(f"    {msg}")

    def section(self, title):
        self.lines.append("")
        self.lines.append(f"── {title} ──")


def _exists(root, rel):
    return os.path.exists(os.path.join(root, rel))


def check_project_json(root, rep):
    rep.section("1. project.json")
    pj = os.path.join(root, "project.json")
    if not os.path.exists(pj):
        rep.fail("project.json 없음 — new_project.py 로 스캐폴딩이 필요합니다")
        return None
    try:
        with open(pj, encoding="utf-8") as f:
            meta = json.load(f)
    except Exception as e:
        rep.fail(f"project.json 파싱 실패: {e}")
        return None
    rep.ok("project.json 존재")
    status = meta.get("status")
    if status in VALID_STATUS:
        rep.ok(f"status 유효: {status}")
    else:
        rep.warn(f"status 비표준: {status!r} (허용: {VALID_STATUS})")
    gp = meta.get("gates_passed", [])
    rep.info(f"통과 게이트: {gp if gp else '(없음)'}")
    rep.info(f"문서 유형: {meta.get('document_type', '?')} / 기관: {meta.get('organization', '?')}")
    return meta


def check_dirs(root, rep):
    rep.section("2. 폴더 구조 완전성")
    missing = [d for d in EXPECTED_DIRS if not os.path.isdir(os.path.join(root, d))]
    if not missing:
        rep.ok(f"{len(EXPECTED_DIRS)}개 폴더 모두 존재")
    else:
        rep.warn(f"누락 폴더 {len(missing)}개 — new_project.py --force 로 보강 가능")
        for d in missing:
            rep.info(f"누락: {d}/")


def check_core_needs_check(root, rep):
    rep.section("3. business-core.yaml [확인 필요] 잔존")
    core = os.path.join(root, "05-business-core", "business-core.yaml")
    if not os.path.exists(core):
        rep.warn("business-core.yaml 없음 — Gate 3 진입 전이거나 미생성")
        return
    try:
        with open(core, encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        rep.fail(f"business-core.yaml 읽기 실패: {e}")
        return
    count = len(NEEDS_CHECK_RE.findall(text))
    if count == 0:
        rep.ok("[확인 필요] 잔존 0건 — 코어 항목이 모두 확정/근거화됨")
    else:
        rep.warn(f"[확인 필요] {count}건 잔존 — 후속 인터뷰/리서치로 채워야 함")
    # YAML 파싱 가능성 점검(파싱 자체 실패는 정보용)
    if _HAS_YAML:
        try:
            yaml.safe_load(text)
            rep.ok("YAML 파싱 정상")
        except Exception as e:
            rep.warn(f"YAML 파싱 경고: {e}")


def check_gate_outputs(root, rep):
    rep.section("4. 게이트별 필수 산출물")
    for gate, files in GATE_OUTPUTS.items():
        present = [f for f in files if _exists(root, f)]
        n_total = len(files)
        n_have = len(present)
        if n_have == n_total:
            rep.ok(f"{gate}: {n_have}/{n_total} 산출물 완비")
        elif n_have == 0:
            rep.fail(f"{gate}: 0/{n_total} — 미진행")
        else:
            rep.warn(f"{gate}: {n_have}/{n_total} (일부 누락)")
            for f in files:
                if not _exists(root, f):
                    rep.info(f"누락: {f}")


def check_vague_words(root, rep):
    rep.section("5. 모호어 탐지 (business-core.yaml)")
    core = os.path.join(root, "05-business-core", "business-core.yaml")
    if not os.path.exists(core):
        rep.info("business-core.yaml 미생성 — 모호어 점검 생략")
        return
    try:
        with open(core, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        rep.fail(f"business-core.yaml 읽기 실패: {e}")
        return
    # 부분문자열 이중 카운트 방지(예: '혁신적' 매칭 시 '혁신' 제외)를 위해 긴 단어 우선
    words_sorted = sorted(VAGUE_WORDS, key=len, reverse=True)
    hits = []  # (lineno, word, snippet)
    for idx, line in enumerate(lines, start=1):
        # 주석(#) 줄은 제외 — 템플릿 안내문에 모호어 예시가 있을 수 있음
        stripped = line.strip()
        if stripped.startswith("#") or stripped == "":
            continue
        # 값 부분만 검사 (key: value 의 value), 주석 꼬리 제거
        value = line.split(":", 1)[1] if ":" in line else line
        value = value.split("#", 1)[0]
        # 표시용 스니펫도 주석 제거
        snippet = stripped.split("#", 1)[0].strip()[:60]
        matched = value
        for w in words_sorted:
            if w in matched:
                hits.append((idx, w, snippet))
                # 같은 영역의 짧은 부분문자열 재카운트 방지
                matched = matched.replace(w, " " * len(w))
    if not hits:
        rep.ok("모호어 0건 — 값이 구체적으로 작성됨")
    else:
        rep.warn(f"모호어 {len(hits)}건 — 수치·사례로 구체화 필요 (SKILL.md §116)")
        seen = set()
        for lineno, w, snip in hits:
            key = (lineno, w)
            if key in seen:
                continue
            seen.add(key)
            rep.info(f"L{lineno} [{w}]: {snip}")


def check_source_index(root, rep):
    rep.section("6. source-index.xlsx 출처 행 수")
    sidx = os.path.join(root, "04-research", "source-index.xlsx")
    if not os.path.exists(sidx):
        rep.warn("source-index.xlsx 없음 — Gate 2 미진행 또는 미생성")
        return
    if not _HAS_OPENPYXL:
        rep.info("openpyxl 미설치 — 행 수 점검 생략 (pip3 install openpyxl)")
        return
    try:
        wb = openpyxl.load_workbook(sidx, read_only=True)
        ws = wb.active
        # 헤더 1행 제외, 비어있지 않은 데이터 행 카운트
        data_rows = 0
        for r, row in enumerate(ws.iter_rows(values_only=True)):
            if r == 0:
                continue
            if any(c is not None and str(c).strip() != "" for c in row):
                data_rows += 1
        wb.close()
    except Exception as e:
        rep.fail(f"source-index.xlsx 읽기 실패: {e}")
        return
    if data_rows == 0:
        rep.warn("출처 0건 — 출처 없는 핵심 통계 금지(7대 규칙 #3). 자료 등재 필요")
    else:
        rep.ok(f"출처 {data_rows}행 등재됨")


def main() -> int:
    if len(sys.argv) < 2:
        print("사용: python3 validate_project.py <bizplan-slug 디렉토리>", file=sys.stderr)
        print("예 : python3 validate_project.py bizplan-smartfarm/", file=sys.stderr)
        return 1

    root = os.path.abspath(sys.argv[1])
    if not os.path.isdir(root):
        print(f"[오류] 디렉토리 없음: {root}", file=sys.stderr)
        return 1

    rep = Report()
    print("=" * 60)
    print(f"bizplan 프로젝트 검증: {root}")
    print("=" * 60)

    check_project_json(root, rep)
    check_dirs(root, rep)
    check_core_needs_check(root, rep)
    check_gate_outputs(root, rep)
    check_vague_words(root, rep)
    check_source_index(root, rep)

    print("\n".join(rep.lines))
    print("")
    print("=" * 60)
    print(f"요약: ✓ {rep.pass_n}  ⚠ {rep.warn_n}  ✗ {rep.fail_n}")
    if rep.fail_n == 0 and rep.warn_n == 0:
        print("→ 모든 점검 통과. 다음 단계로 진행 가능.")
    elif rep.fail_n == 0:
        print("→ 차단 항목 없음. ⚠ 경고는 해당 단계 진입 전 보강 권장.")
    else:
        print("→ ✗ 미진행 게이트가 있습니다. 해당 단계부터 작업하세요(진단용, 비차단).")
    print("=" * 60)

    # 진단용 — 항상 0 (비차단)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
