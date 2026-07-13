/**
 * deck.json → PPTX (투자 피치덱용).
 *
 * 변환 엔진은 pptxgenjs — 텍스트·표·도형을 네이티브 객체로 생성하므로
 * PowerPoint/한쇼/Keynote 에서 글자·표를 바로 수정할 수 있다(편집 가능 우선).
 * 16:9(13.333 × 7.5 inch), 한글 폰트(맑은 고딕), 일관된 색 테마.
 *
 * 사용:
 *   npx tsx scripts/build_pptx.mts <deck.json> <out.pptx>
 *
 * ─────────────────────────────────────────────────────────────────────────
 * deck.json 스키마
 * ─────────────────────────────────────────────────────────────────────────
 * {
 *   "title":  "스타트업 IR 덱",            // 필수. 표지/문서 메타 제목
 *   "subtitle": "한 줄 가치 제안",          // 선택
 *   "author": "홍길동",                     // 선택
 *   "date":   "2026-06",                    // 선택
 *   "theme":  "navy",                       // 선택: navy(기본) | slate | forest | plum
 *   "slides": [ <slide>, ... ]              // 필수
 * }
 *
 * <slide> 공통(모든 layout): { layout, title?, notes? }
 *   - notes: 발표자 노트(speaker note)
 *
 * layout 종류와 추가 필드:
 *   title       표지.        { subtitle?, author?, date?, badge? }
 *   section     장 구분.     { index?(번호), subtitle?, bullets?(string[]) }
 *   bullets     불릿 목록.   { kicker?, subtitle?, bullets:(string | {text, sub?:string[]})[] }
 *   two-column  좌우 비교.   { kicker?, subtitle?,
 *                              left:{ label, body?:string[], bullets?:string[], metric?:{value,label?} },
 *                              right:{ ... 동일 ... } }
 *   table       표.          { kicker?, subtitle?, table:{ headers:string[], rows:string[][] },
 *                              emphasisCol?(강조 열 index), note? }
 *   image       이미지 1장.  { kicker?, subtitle?, image(파일경로), caption?, body?:string[] }
 *                              (이미지 파일이 없으면 정직한 placeholder 박스 + 캡션)
 *   stat        핵심 지표.   { kicker?, subtitle?,
 *                              stats:{ value, label, desc? }[] (1~4개 권장), note? }
 *   quote       인용.        { body(인용문 본문), cite?(출처) }     ← title 생략 가능
 *   closing     마무리.      { message?, cta? }                      ← title=THANK YOU 등
 *
 * 피치덱 표준(문제/해결/시장/BM/경쟁/팀/투자금)은 위 layout 조합으로 표현한다:
 *   문제·해결 → bullets/two-column, 시장(TAM/SAM/SOM) → stat/table,
 *   BM → bullets/table, 경쟁 → two-column/table, 팀 → bullets,
 *   투자금(use of funds) → table/stat.
 */
import { dirname, isAbsolute, join, resolve } from 'node:path';
import { existsSync, readFileSync } from 'node:fs';
import PptxGenJSImport from 'pptxgenjs';
import type PptxGenJSNS from 'pptxgenjs';

// pptxgenjs v4: default export = 생성자 클래스, 타입은 네임스페이스 멤버(PptxGenJS.TextProps 등).
// CJS/ESM interop 환경에서 default 가 한 번 더 감싸질 수 있어 안전 폴백을 둔다(런타임만 영향).
const PptxGenJS = ((PptxGenJSImport as unknown as { default?: unknown }).default ??
  PptxGenJSImport) as typeof PptxGenJSImport;

type PptxSlide = ReturnType<InstanceType<typeof PptxGenJSImport>['addSlide']>;
type TextProps = PptxGenJSNS.TextProps;
type Border = PptxGenJSNS.BorderProps;
const borders = (t: Border, r: Border, b: Border, l: Border): [Border, Border, Border, Border] => [t, r, b, l];

// ── 레이아웃 상수 (16:9, inch) ──────────────────────────────────────────────
const W = 13.333;
const H = 7.5;
const ML = 0.9; // 좌우 여백
const CW = W - ML * 2; // 콘텐츠 폭
const F = '맑은 고딕'; // 한글 호환 본문 폰트

// ── 색 테마 ─────────────────────────────────────────────────────────────────
interface Palette {
  accent: string; // 강조·바·도형
  accentText: string; // 밝은 배경 위 강조 텍스트
  ink: string; // 본문·제목
  muted: string; // 보조 텍스트
  onAccent: string; // accent/dark 위 텍스트
  bg: string; // 슬라이드 배경
  line: string; // hairline
  emphTint: string; // 표 강조열 옅은 틴트
  dark: string; // 표지·마무리 다크 배경
}

type ThemeName = 'navy' | 'slate' | 'forest' | 'plum';

const THEME: Record<ThemeName, Palette> = {
  // 투자덱 기본 — 신뢰감 있는 네이비
  navy: { accent: '2455D8', accentText: '1E47B8', ink: '141A24', muted: '5C6878', onAccent: 'F4F8FF', bg: 'FFFFFF', line: 'DDE2EC', emphTint: 'EAF0FF', dark: '0F1A33' },
  slate: { accent: '4B5563', accentText: '374151', ink: '111827', muted: '6B7280', onAccent: 'F9FAFB', bg: 'FFFFFF', line: 'E2E5EA', emphTint: 'EEF1F4', dark: '1F2937' },
  forest: { accent: '128A5E', accentText: '0E7350', ink: '12211B', muted: '566B61', onAccent: 'F3FBF7', bg: 'FFFFFF', line: 'D9E4DD', emphTint: 'E7F4ED', dark: '0E2A20' },
  plum: { accent: '8A3FB0', accentText: '743397', ink: '1E1424', muted: '6B5C76', onAccent: 'FBF5FE', bg: 'FFFFFF', line: 'E7DDED', emphTint: 'F4EAFA', dark: '2A1633' },
};

// ── deck.json 타입 ──────────────────────────────────────────────────────────
interface SideSpec {
  label: string;
  body?: string[];
  bullets?: string[];
  metric?: { value: string; label?: string };
}
interface Bullet {
  text: string;
  sub?: string[];
}
interface Slide {
  layout: string;
  title?: string;
  notes?: string;
  // 공통/레이아웃별 (느슨하게 받음 — 런타임 검증)
  kicker?: string;
  subtitle?: string;
  author?: string;
  date?: string;
  badge?: string;
  index?: number | string;
  bullets?: (string | Bullet)[];
  body?: string[] | string;
  left?: SideSpec;
  right?: SideSpec;
  table?: { headers: string[]; rows: string[][] };
  emphasisCol?: number;
  note?: string;
  image?: string;
  caption?: string;
  stats?: { value: string; label: string; desc?: string }[];
  cite?: string;
  message?: string;
  cta?: string;
}
interface Deck {
  title: string;
  subtitle?: string;
  author?: string;
  date?: string;
  theme?: ThemeName;
  slides: Slide[];
}

function usage(): never {
  process.stderr.write(
    [
      'BizPlan PPTX 빌더 — deck.json 을 투자 피치덱 PPTX 로 변환합니다.',
      '',
      '사용법:',
      '  npx tsx scripts/build_pptx.mts <deck.json> <out.pptx>',
      '',
      '예시:',
      '  npx tsx scripts/build_pptx.mts data/deck.json 10-final/pitch-deck.pptx',
      '',
      'deck.json 스키마는 이 파일 상단 주석을 참고하세요.',
      '',
    ].join('\n'),
  );
  process.exit(1);
}

const asBullet = (b: string | Bullet): Bullet => (typeof b === 'string' ? { text: b } : b);

/** body 를 문자열 배열로 정규화 (string | string[] | undefined 모두 허용) */
const bodyLines = (body: unknown): string[] =>
  Array.isArray(body) ? (body as string[]) : typeof body === 'string' && body ? [body] : [];

// ── 공통 헤더 (kicker / title / underline / subtitle). 본문 시작 y 반환 ──────
function addHead(s: PptxSlide, c: Palette, head: { kicker?: string; title?: string; subtitle?: string }): number {
  let y = 0.55;
  if (head.kicker) {
    s.addText(head.kicker, {
      x: ML, y, w: CW, h: 0.3,
      fontFace: F, fontSize: 11, bold: true, color: c.accentText, charSpacing: 2,
    });
    y += 0.34;
  }
  if (head.title) {
    s.addText(head.title, {
      x: ML - 0.03, y, w: CW, h: 0.62,
      fontFace: F, fontSize: 26, bold: true, color: c.ink,
    });
    y += 0.66;
    s.addShape('line', { x: ML, y, w: 0.7, h: 0, line: { color: c.accent, width: 3 } });
    y += 0.12;
  }
  if (head.subtitle) {
    s.addText(head.subtitle, {
      x: ML, y, w: CW, h: 0.38,
      fontFace: F, fontSize: 13, color: c.muted,
    });
    y += 0.46;
  }
  return Math.max(y + 0.15, 1.8);
}

function bulletProps(bullets: Bullet[], c: Palette, size = 16.5): TextProps[] {
  const lines: TextProps[] = [];
  for (const b of bullets) {
    lines.push({
      text: b.text,
      options: {
        bullet: { code: '2022', indent: 14 },
        fontFace: F, fontSize: size, color: c.ink, paraSpaceBefore: 8, breakLine: true,
      },
    });
    for (const sub of b.sub ?? []) {
      lines.push({
        text: sub,
        options: {
          bullet: { code: '2013', indent: 12 }, indentLevel: 1,
          fontFace: F, fontSize: size - 2.5, color: c.muted, breakLine: true,
        },
      });
    }
  }
  return lines;
}

/** 상대 이미지 경로를 절대경로로 — 존재할 때만 반환 */
function resolveImg(rel: string, baseDir: string): string | null {
  const abs = isAbsolute(rel) ? rel : join(baseDir, rel);
  return existsSync(abs) ? abs : null;
}

/** 한 컬럼(two-column 좌/우) 렌더 */
function renderSide(s: PptxSlide, c: Palette, side: SideSpec, x: number, colW: number, y0: number): void {
  s.addText(side.label, {
    x, y: y0 + 0.05, w: colW, h: 0.4,
    fontFace: F, fontSize: 14, bold: true, color: c.accentText, charSpacing: 1,
  });
  s.addShape('line', { x, y: y0 + 0.5, w: colW, h: 0, line: { color: c.accent, width: 2 } });
  let py = y0 + 0.72;
  if (side.metric) {
    s.addText(side.metric.value, {
      x: x - 0.04, y: py, w: colW, h: 1.0,
      fontFace: F, fontSize: 40, bold: true, color: c.accent,
    });
    if (side.metric.label) {
      s.addText(side.metric.label, {
        x, y: py + 1.0, w: colW, h: 0.28,
        fontFace: F, fontSize: 11, bold: true, color: c.muted, charSpacing: 1,
      });
      py += 0.32;
    }
    py += 1.1;
  }
  if (side.body?.length) {
    s.addText(side.body.join('\n'), {
      x, y: py, w: colW, h: 0.5 * side.body.length,
      fontFace: F, fontSize: 14, color: c.ink, lineSpacing: 24,
    });
    py += 0.5 * side.body.length + 0.2;
  }
  if (side.bullets?.length) {
    s.addText(bulletProps(side.bullets.map(asBullet), c, 14), {
      x, y: py, w: colW, h: H - py - 0.8, valign: 'top',
    });
  }
}

// ── 슬라이드 렌더 디스패치 ───────────────────────────────────────────────────
function renderSlide(s: PptxSlide, slide: Slide, c: Palette, baseDir: string): boolean {
  const layout = (slide.layout || 'bullets').toLowerCase();
  switch (layout) {
    // ── 표지 ──
    case 'title': {
      s.background = { color: c.dark };
      s.addShape('rect', { x: 0, y: 0, w: 0.22, h: H, fill: { color: c.accent } });
      if (slide.badge) {
        s.addText(slide.badge, {
          x: ML, y: 1.7, w: CW, h: 0.34,
          fontFace: F, fontSize: 12.5, bold: true, color: 'AEC2F2', charSpacing: 5,
        });
      }
      s.addText(slide.title ?? '', {
        x: ML - 0.04, y: 2.35, w: CW, h: 1.7,
        fontFace: F, fontSize: 38, bold: true, color: 'FFFFFF', lineSpacing: 50,
      });
      if (slide.subtitle) {
        s.addText(slide.subtitle, {
          x: ML, y: 4.25, w: CW - 1, h: 0.7,
          fontFace: F, fontSize: 16, color: 'C3CEE2', lineSpacing: 24,
        });
      }
      const meta = [slide.author, slide.date].filter(Boolean).join('   ·   ');
      if (meta) {
        s.addShape('line', { x: ML, y: H - 1.2, w: 6, h: 0, line: { color: '37486E', width: 1 } });
        s.addText(meta, {
          x: ML, y: H - 1.05, w: 9, h: 0.35,
          fontFace: F, fontSize: 12.5, color: '90A1BE',
        });
      }
      return true; // 다크 표지 — 페이지 번호 생략
    }

    // ── 장 구분 ──
    case 'section': {
      if (slide.index != null) {
        s.addText(String(slide.index).padStart(2, '0'), {
          x: ML - 0.05, y: 2.2, w: 2.4, h: 1.6,
          fontFace: F, fontSize: 88, bold: true, color: c.accent,
        });
      }
      const tx = slide.index != null ? ML + 2.5 : ML;
      s.addText(slide.title ?? '', {
        x: tx, y: 2.75, w: W - tx - ML, h: 0.9,
        fontFace: F, fontSize: 30, bold: true, color: c.ink,
      });
      if (slide.subtitle) {
        s.addText(slide.subtitle, {
          x: tx, y: 3.65, w: W - tx - ML, h: 0.5,
          fontFace: F, fontSize: 14, color: c.muted,
        });
      }
      if (slide.bullets?.length) {
        s.addText(
          slide.bullets.map(asBullet).map((b): TextProps => ({
            text: b.text,
            options: { bullet: { code: '2022', indent: 12 }, fontFace: F, fontSize: 12, color: c.muted, breakLine: true, paraSpaceBefore: 5 },
          })),
          { x: tx, y: 4.35, w: W - tx - ML, h: H - 5 },
        );
      }
      break;
    }

    // ── 불릿 목록 ──
    case 'bullets': {
      const y = addHead(s, c, { kicker: slide.kicker, title: slide.title, subtitle: slide.subtitle });
      const bs = (slide.bullets ?? []).map(asBullet);
      const body = bodyLines(slide.body);
      if (body.length) {
        s.addText(body.join('\n'), {
          x: ML, y, w: CW, h: 0.5 * body.length + 0.1,
          fontFace: F, fontSize: 16, color: c.ink, lineSpacing: 28,
        });
      }
      const by = body.length ? y + 0.55 * body.length + 0.25 : y;
      if (bs.length) {
        s.addText(bulletProps(bs, c), { x: ML, y: by, w: CW, h: H - by - 0.6, valign: 'top' });
      }
      break;
    }

    // ── 좌우 비교 ──
    case 'two-column':
    case 'twocolumn':
    case 'two_column': {
      const y = addHead(s, c, { kicker: slide.kicker, title: slide.title, subtitle: slide.subtitle });
      const colW = CW / 2 - 0.4;
      const left = slide.left ?? { label: '좌' };
      const right = slide.right ?? { label: '우' };
      renderSide(s, c, left, ML, colW, y);
      renderSide(s, c, right, ML + CW / 2 + 0.4, colW, y);
      s.addShape('line', { x: ML + CW / 2, y: y + 0.1, w: 0, h: H - y - 1.0, line: { color: c.line, width: 0.75 } });
      break;
    }

    // ── 표 ──
    case 'table': {
      const y = addHead(s, c, { kicker: slide.kicker, title: slide.title, subtitle: slide.subtitle });
      const t = slide.table ?? { headers: [], rows: [] };
      const noBorder: Border = { type: 'none' };
      const hair: Border = { type: 'solid', color: c.line, pt: 0.75 };
      const inkThin: Border = { type: 'solid', color: c.ink, pt: 1.25 };
      const inkThick: Border = { type: 'solid', color: c.ink, pt: 2.25 };
      const header = t.headers.map((h, col) => ({
        text: h,
        options: {
          bold: true, color: col === slide.emphasisCol ? c.accent : c.ink, align: 'left' as const,
          fill: { color: c.bg }, border: borders(inkThick, noBorder, inkThin, noBorder),
        },
      }));
      const body = t.rows.map((row) =>
        t.headers.map((_, col) => ({
          text: row[col] ?? '',
          options: {
            color: c.ink, bold: col === 0, align: 'left' as const,
            fill: { color: col === slide.emphasisCol ? c.emphTint : c.bg },
            border: borders(noBorder, noBorder, hair, noBorder),
          },
        })),
      );
      const noteH = slide.note ? 0.45 : 0;
      const tFont = t.rows.length > 9 ? 11 : 12.5;
      if (header.length) {
        s.addTable([header, ...body], {
          x: ML, y, w: CW, h: H - y - 0.6 - noteH,
          fontFace: F, fontSize: tFont, valign: 'middle', autoPage: false, margin: [3, 6, 3, 2],
        });
      }
      if (slide.note) {
        s.addText(slide.note, {
          x: ML, y: H - 0.95, w: CW, h: 0.35,
          fontFace: F, fontSize: 10, italic: true, color: c.muted,
        });
      }
      break;
    }

    // ── 이미지 1장 ──
    case 'image': {
      const y = addHead(s, c, { kicker: slide.kicker, title: slide.title, subtitle: slide.subtitle });
      const body = bodyLines(slide.body);
      const bodyW = body.length ? 4.4 : 0;
      const imgX = ML;
      const imgW = CW - bodyW - (bodyW ? 0.5 : 0);
      const imgY = y;
      const imgH = H - y - 0.7 - (slide.caption ? 0.35 : 0);
      const abs = slide.image ? resolveImg(slide.image, baseDir) : null;
      if (abs) {
        // sizing contain — 비율 보존 (sizing.w/h 박스에 맞춤)
        s.addImage({ path: abs, x: imgX, y: imgY, w: imgW, h: imgH, sizing: { type: 'contain', w: imgW, h: imgH } });
      } else {
        // 정직한 placeholder — 이미지 파일이 없으면 회색 박스 + 라벨 (가짜 이미지 금지)
        s.addShape('rect', { x: imgX, y: imgY, w: imgW, h: imgH, fill: { color: c.emphTint }, line: { color: c.line, width: 0.75 } });
        const label = slide.image ? `[이미지 누락] ${slide.image}` : '[이미지 경로 미지정]';
        s.addText(label, {
          x: imgX, y: imgY + imgH / 2 - 0.25, w: imgW, h: 0.5,
          fontFace: F, fontSize: 12, italic: true, color: c.muted, align: 'center', valign: 'middle',
        });
      }
      if (slide.caption) {
        s.addText(slide.caption, {
          x: imgX, y: imgY + imgH + 0.06, w: imgW, h: 0.3,
          fontFace: F, fontSize: 10.5, italic: true, color: c.muted,
        });
      }
      if (body.length) {
        s.addText(bulletProps(body.map((t) => ({ text: t })), c, 14), {
          x: ML + imgW + 0.5, y, w: bodyW, h: H - y - 0.7, valign: 'top',
        });
      }
      break;
    }

    // ── 핵심 지표 ──
    case 'stat':
    case 'stats': {
      const y = addHead(s, c, { kicker: slide.kicker, title: slide.title, subtitle: slide.subtitle });
      const stats = slide.stats ?? [];
      const n = Math.max(1, stats.length);
      const gap = 0.4;
      const boxW = (CW - gap * (n - 1)) / n;
      const top = y + 0.4;
      stats.forEach((st, i) => {
        const x = ML + i * (boxW + gap);
        s.addShape('rect', { x, y: top, w: 0.55, h: 0.045, fill: { color: c.accent } });
        s.addText(st.value, {
          x, y: top + 0.22, w: boxW, h: 1.0,
          fontFace: F, fontSize: i === 0 ? 48 : 40, bold: true, color: i === 0 ? c.accent : c.ink,
        });
        s.addText(st.label, {
          x, y: top + 1.45, w: boxW, h: 0.4,
          fontFace: F, fontSize: 13, bold: true, color: c.ink,
        });
        if (st.desc) {
          s.addText(st.desc, {
            x, y: top + 1.85, w: boxW, h: 0.8,
            fontFace: F, fontSize: 10.5, color: c.muted, valign: 'top',
          });
        }
      });
      if (slide.note) {
        s.addText(slide.note, {
          x: ML, y: H - 0.95, w: CW, h: 0.35,
          fontFace: F, fontSize: 10, italic: true, color: c.muted,
        });
      }
      break;
    }

    // ── 인용 ──
    case 'quote': {
      s.addText('“', {
        x: ML, y: 1.2, w: 2, h: 1.4,
        fontFace: F, fontSize: 110, bold: true, color: c.accent,
      });
      s.addText(bodyLines(slide.body).join('\n') || slide.title || '', {
        x: ML + 0.4, y: 2.6, w: CW - 0.8, h: 2.2,
        fontFace: F, fontSize: 26, italic: true, color: c.ink, lineSpacing: 38,
      });
      if (slide.cite) {
        s.addText(`— ${slide.cite}`, {
          x: ML + 0.4, y: 5.2, w: CW - 0.8, h: 0.4,
          fontFace: F, fontSize: 13, color: c.muted,
        });
      }
      break;
    }

    // ── 마무리 ──
    case 'closing': {
      s.background = { color: c.dark };
      s.addText('THANK YOU', {
        x: ML, y: 1.9, w: CW, h: 0.3,
        fontFace: F, fontSize: 11, bold: true, color: '7C8DAE', charSpacing: 5,
      });
      s.addText(slide.title ?? '함께 만들어 갑니다', {
        x: ML - 0.04, y: 2.35, w: CW, h: 1.1,
        fontFace: F, fontSize: 42, bold: true, color: 'FFFFFF',
      });
      s.addShape('line', { x: ML, y: 3.55, w: 0.7, h: 0, line: { color: 'AEC2F2', width: 3 } });
      if (slide.message) {
        s.addText(slide.message, {
          x: ML, y: 3.9, w: CW, h: 0.6,
          fontFace: F, fontSize: 15, color: 'C3CEE2', lineSpacing: 24,
        });
      }
      if (slide.cta) {
        s.addText(slide.cta, {
          x: ML, y: 5.4, w: CW, h: 0.45,
          fontFace: F, fontSize: 13.5, bold: true, color: 'EAF0FF', underline: { style: 'sng' },
        });
      }
      return true; // 다크 마무리 — 페이지 번호 생략
    }

    default: {
      // 알 수 없는 layout — 정직하게 표기하고 본문만 출력
      const y = addHead(s, c, { kicker: slide.kicker, title: slide.title ?? `(알 수 없는 layout: ${slide.layout})`, subtitle: slide.subtitle });
      if (slide.bullets?.length) {
        s.addText(bulletProps(slide.bullets.map(asBullet), c), { x: ML, y, w: CW, h: H - y - 0.6, valign: 'top' });
      }
      break;
    }
  }
  return false;
}

async function main(): Promise<void> {
  const [, , inArg, outArg] = process.argv;
  if (!inArg || !outArg) usage();

  const inPath = resolve(inArg);
  const outPath = resolve(outArg);

  let deck: Deck;
  try {
    deck = JSON.parse(readFileSync(inPath, 'utf-8')) as Deck;
  } catch (err) {
    process.stderr.write(`✗ deck.json 을 읽거나 파싱할 수 없습니다: ${inPath}\n  ${String(err)}\n`);
    process.exit(1);
  }
  if (!deck || !Array.isArray(deck.slides) || deck.slides.length === 0) {
    process.stderr.write('✗ deck.json 에 slides 배열이 없거나 비어 있습니다.\n');
    process.exit(1);
  }

  const themeName: ThemeName = (deck.theme && THEME[deck.theme] ? deck.theme : 'navy');
  const c = THEME[themeName];

  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'WIDE_16x9', width: W, height: H });
  pptx.layout = 'WIDE_16x9';
  pptx.title = deck.title ?? 'BizPlan Pitch Deck';
  if (deck.author) pptx.author = deck.author;

  const baseDir = dirname(inPath);
  const total = deck.slides.length;

  deck.slides.forEach((slide, i) => {
    const s = pptx.addSlide();
    s.background = { color: c.bg };
    const noFooter = renderSlide(s, slide, c, baseDir);
    if (!noFooter) {
      s.addText(`${i + 1} / ${total}`, {
        x: W - 1.6, y: H - 0.42, w: 1.2, h: 0.3,
        fontFace: F, fontSize: 9, color: c.muted, align: 'right',
      });
    }
    if (slide.notes) s.addNotes(slide.notes);
  });

  try {
    await pptx.writeFile({ fileName: outPath });
  } catch (err) {
    process.stderr.write(`✗ PPTX 쓰기 실패:\n  ${String(err)}\n`);
    process.exit(1);
  }

  process.stdout.write(`✓ PPTX 생성 → ${outPath}  (슬라이드 ${total}개 / 테마 ${themeName})\n`);
}

main().catch((err) => {
  process.stderr.write(`✗ 예기치 못한 오류:\n  ${String(err?.stack ?? err)}\n`);
  process.exit(1);
});
