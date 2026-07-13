/**
 * Markdown → HWPX (한국 정부지원사업 서식용).
 *
 * 변환 엔진은 kordoc 의 `markdownToHwpx` — npm 공개(MIT), macOS 한컴 호환 검증됨.
 * 마크다운의 헤딩/단락/목록/표(GFM)/굵게/인용이 모두 실제 HWPX 문단·표 객체로 들어가
 * 한컴오피스에서 직접 편집 가능하다. 변환 후 `parseHwpx` 라운드트립으로 자가검증한다.
 *
 * 사용:
 *   npx tsx scripts/build_hwpx.mts <in.md> <out.hwpx>
 *
 * 예:
 *   npx tsx scripts/build_hwpx.mts 08-draft/business-plan.md 10-final/final-business-plan.hwpx
 *
 * 주의(kordoc 2.8 실제 지원 범위):
 *   - 표는 GFM 파이프 표( | a | b | / | --- | --- | )만 인식한다. 표 셀에는 테두리가 적용된다.
 *   - HwpxTheme 으로 헤딩 색·본문 색·인용 색·표 헤더 굵게만 제어 가능(폰트 family 옵션은 없음 →
 *     한컴 기본 한글 폰트로 들어간다). 추측 API 를 쓰지 않고 doc-2-deck 검증 경로만 사용한다.
 */
import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { markdownToHwpx, parseHwpx, type HwpxTheme } from 'kordoc';

// 한국 공식 문서용 차분한 테마 — 헤딩은 진한 남색, 본문은 거의 검정, 표 헤더 굵게.
// (kordoc 이 지원하는 필드만 사용. 추측 필드 금지.)
const THEME: HwpxTheme = {
  headingColors: { 1: '#1A3C8A', 2: '#1A3C8A', 3: '#22324A', 4: '#22324A' },
  bodyColor: '#1B1F27',
  quoteColor: '#3A4A66',
  tableHeaderColor: '#0E1A33',
  tableHeaderBold: true,
};

function usage(): never {
  process.stderr.write(
    [
      'BizPlan HWPX 빌더 — Markdown 을 한컴 편집 가능 HWPX 로 변환합니다.',
      '',
      '사용법:',
      '  npx tsx scripts/build_hwpx.mts <in.md> <out.hwpx>',
      '',
      '예시:',
      '  npx tsx scripts/build_hwpx.mts 08-draft/business-plan.md 10-final/final-business-plan.hwpx',
      '',
    ].join('\n'),
  );
  process.exit(1);
}

/**
 * 마크다운을 kordoc 친화적으로 가볍게 정규화한다.
 *  - 윈도우 개행(CRLF) → LF
 *  - 탭 → 스페이스 4칸 (kordoc 표/리스트 파서 안정화)
 *  - 선행 BOM 제거
 * 내용을 바꾸지 않는 무해한 정규화만 한다(7대 절대 규칙 — 임의 창작 금지).
 */
function normalizeMarkdown(src: string): string {
  return src
    .replace(/^﻿/, '')
    .replace(/\r\n?/g, '\n')
    .replace(/\t/g, '    ');
}

async function main(): Promise<void> {
  const [, , inArg, outArg] = process.argv;
  if (!inArg || !outArg) usage();

  const inPath = resolve(inArg);
  const outPath = resolve(outArg);

  let raw: string;
  try {
    raw = await readFile(inPath, 'utf-8');
  } catch (err) {
    process.stderr.write(`✗ 입력 파일을 읽을 수 없습니다: ${inPath}\n  ${String(err)}\n`);
    process.exit(1);
  }

  const markdown = normalizeMarkdown(raw);
  if (!markdown.trim()) {
    process.stderr.write(`✗ 입력 마크다운이 비어 있습니다: ${inPath}\n`);
    process.exit(1);
  }

  // 변환
  let buf: ArrayBuffer;
  try {
    buf = await markdownToHwpx(markdown, { theme: THEME });
  } catch (err) {
    process.stderr.write(`✗ HWPX 변환 실패 (kordoc markdownToHwpx):\n  ${String(err)}\n`);
    process.exit(1);
  }

  await writeFile(outPath, Buffer.from(buf));

  // 자가검증 — 라운드트립 파싱으로 한컴 호환 구조 + 본문 보존 확인
  let blocks = 0;
  let tables = 0;
  let textOk = true;
  try {
    const parsed = await parseHwpx(buf);
    const blockList = parsed.success ? parsed.blocks : [];
    blocks = blockList.length;
    tables = blockList.filter((b) => b.type === 'table').length;

    // 본문 첫 의미 토큰(헤딩/단락 텍스트)이 보존됐는지 가볍게 확인
    const probe = (markdown.match(/[^\s#>*|\-]{4,}/) ?? [''])[0].slice(0, 6);
    if (probe) textOk = JSON.stringify(parsed).includes(probe);

    // 입력에 GFM 표가 있는데 table 블록이 0개면 경고(치명 아님 — 표 문법 점검 안내)
    const hasMdTable = /\n\|.*\|.*\n\|[\s:|-]+\|/.test(`\n${markdown}\n`);
    if (hasMdTable && tables === 0) {
      process.stderr.write(
        '⚠ 입력에 GFM 표가 있으나 HWPX table 블록으로 변환되지 않았습니다.\n' +
          '  표 문법(| 헤더 | ... | / | --- | --- |)을 확인하세요.\n',
      );
    }
  } catch (err) {
    process.stderr.write(`⚠ 자가검증(parseHwpx) 건너뜀: ${String(err)}\n`);
  }

  if (!textOk) {
    process.stderr.write('⚠ 자가검증: 본문 텍스트 보존을 확인하지 못했습니다. 결과 파일을 직접 열어 확인하세요.\n');
  }

  const kb = (Buffer.from(buf).length / 1024).toFixed(0);
  process.stdout.write(`✓ HWPX 생성 → ${outPath}  (블록 ${blocks}개 / 표 ${tables}개 / ${kb} KB)\n`);
}

main().catch((err) => {
  process.stderr.write(`✗ 예기치 못한 오류:\n  ${String(err?.stack ?? err)}\n`);
  process.exit(1);
});
