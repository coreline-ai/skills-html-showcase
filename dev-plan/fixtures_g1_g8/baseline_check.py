#!/usr/bin/env python3
"""G1~G8 fixture/gate 전이 검증기 — implement_20260618_221706.md Phase 0(baseline) → Phase 2(detection).

실행: python3 dev-plan/fixtures_g1_g8/baseline_check.py
종료코드:
  0 = 기대 상태가 성립(현재 = Phase 2 이후: 정적 게이트가 fixture를 '검출'로 뒤집음).
  1 = 기대 상태 위반.

이력:
  - Phase 0(2026-06-21): 게이트 신설 전, 여덟 결함이 모두 '현행 미검출(INVISIBLE)'임을 입증해
    회귀 기준선을 만들었다(git 이력에 보존).
  - Phase 2(2026-06-21): validate_output.py에 G3~G8 게이트를 신설. 이 스크립트는 이제 동일 fixture가
    '검출(CAUGHT)'로 뒤집혔는지 검증한다. G1은 작성 계약(.status-pill)·G2는 render-audit(별도 .mjs)라
    정적 게이트 대상이 아니다(아래 NOTE).

스킬 패키지(.skill) 영향 0: dev-plan/ 밖이 아니라 안에 있고 skills/ 밖이므로 skill_package 게이트와 무관.
"""
from __future__ import annotations
import importlib.util, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent.parent / "skills" / "adaptive-html-final"
spec = importlib.util.spec_from_file_location("validate_output", SKILL / "scripts" / "validate_output.py")
v = importlib.util.module_from_spec(spec); sys.modules["validate_output"] = v; spec.loader.exec_module(v)

def read(name): return (HERE / name).read_text(encoding="utf-8")
def style_of(html): return "\n".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", html, re.I))

A = SKILL / "assets"
comp = (A / "components.css").read_text(); edit = (A / "editorial-patterns.css").read_text()

_fails = 0
rows = []
def expect_caught(gid, defect, caught: bool, via: str):
    global _fails
    if not caught: _fails += 1
    rows.append((gid, defect, "CAUGHT ✓" if caught else "MISSED ✗", via))
def note(gid, defect, via):
    rows.append((gid, defect, "NOTE", via))

# G3 (per-page static): 결함 fixture는 inner-card 링크 reset이 없는 인라인 CSS → 게이트가 검출
g3 = read("g3_try_inner_card_link.html")
expect_caught("G3", ".try 흰 카드 링크 저대비",
    bool(v.try_inner_card_link_contrast_gate(g3, style_of(g3))), "try_inner_card_link_contrast_gate (static)")
# G4/G5/G8 (asset): 결함은 정본 규칙 부재 → 악성 CSS로 검출 입증(자산 자체는 Phase1로 클린)
expect_caught("G4", "source-preserve gutter 부재",
    bool(v.source_preserve_gutter_gate(".source-preserve{border-left:4px}")), "source_preserve_gutter_gate (asset)")
expect_caught("G5", "mini-card tag rhythm 부재",
    bool(v.mini_card_tag_rhythm_gate(".mini-card{padding:16px}")), "mini_card_tag_rhythm_gate (asset)")
expect_caught("G8", "core-insight heading reset 부재",
    bool(v.core_insight_heading_reset_gate(".core-insight{background:red}")), "core_insight_heading_reset_gate (asset)")
# G6/G7 (per-page DOM): fixture가 검출됨
expect_caught("G6", "TOC가 executive-summary 내부 중첩",
    bool(v.toc_in_executive_summary_gate(read("g6_toc_nested_in_section.html"))), "toc_in_executive_summary_gate (DOM)")
expect_caught("G7", "<h2> 앞 빈 anchor 선행",
    bool(v.section_leading_empty_anchor_gate(read("g7_h2_leading_anchor.html"))), "section_leading_empty_anchor_gate (DOM)")
# G1/G2: 정적 게이트 대상 아님
note("G1", "표 셀 짧은 코드 줄바꿈", "작성 계약(.status-pill 정본) + Phase 5 문서 — 정적 게이트 비대상")
note("G2", "wg-04 SVG 노드 겹침", "render-audit (scripts/micro_layout_audit.mjs → node_overlap_ok) — 정적 불가")

# 무회귀: 정본 자산(Phase1 적용본)은 자산 게이트 클린
asset_clean = (v.source_preserve_gutter_gate(edit) == [] and v.core_insight_heading_reset_gate(edit) == []
               and v.mini_card_tag_rhythm_gate(comp) == [])

print("=" * 80)
print("G1~G8 fixture/gate 전이 검증 (Phase 2: 검출 게이트 신설 후)")
print("=" * 80)
for gid, defect, verdict, via in rows:
    print(f"[{gid}] {defect:34} {verdict:10} via {via}")
print("-" * 80)
print(f"정본 자산(Phase1) 게이트 클린: {'예 ✓' if asset_clean else '아니오 ✗'}")
ok = (_fails == 0) and asset_clean
print(f"결과: 정적 게이트 6종(G3~G8)이 모두 fixture를 검출. G1=계약, G2=render-audit(.mjs).")
print("VERDICT:", "PASS — Phase 2 검출 전이 확인" if ok else "FAIL")
print("=" * 80)
sys.exit(0 if ok else 1)
