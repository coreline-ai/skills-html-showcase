# Highlight emphasis patterns for operator manuals

Use this reference when a manual needs inline emphasis that feels like a human reader marked an important phrase with a highlighter. This pattern comes from the provided `highlight-samples.html` and `highlight-combined.html` examples, generalized for the reusable manual design system.

## When to use

Use highlight underline emphasis for:

- a short phrase inside an explanation that the reader must remember;
- a concrete value/check in a review card, e.g. `Submitted`, `Outstanding Amount`, `AUTH_TYPE`, `Health OK`;
- a branch/stop condition that is easy to miss;
- a beginner concept term on first appearance.

Do **not** use it for whole paragraphs, generic decoration, status/progress notes, or every noun in a section. One card/paragraph should normally have 0–2 highlighted phrases.

## Preferred default

The preferred style is the combined sample: thin underline, rounded ends, multi-line safe, optional left-to-right reveal.

```css
.og-hl{
  --og-hl-color:#ffe066;
  background-image:linear-gradient(transparent 76%, var(--og-hl-color) 76%);
  background-repeat:no-repeat;
  background-size:100% 100%;
  padding:1px 7px;
  border-radius:4px;
  box-decoration-break:clone;
  -webkit-box-decoration-break:clone;
}
.og-hl.is-animated{
  background-size:0% 100%;
  animation:og-highlight-in .75s cubic-bezier(.4,0,.2,1) .2s forwards;
}
@keyframes og-highlight-in{to{background-size:100% 100%;}}
.og-hl--yellow{--og-hl-color:#ffe066;}
.og-hl--blue{--og-hl-color:#a5d8ff;}
.og-hl--pink{--og-hl-color:#fcc2d7;}
.og-hl--green{--og-hl-color:#d8f5a2;}
@media (prefers-reduced-motion:reduce){.og-hl.is-animated{animation:none;background-size:100% 100%;}}
```

HTML:

```html
<p>저장 전에 <span class="og-hl og-hl--yellow">거래처와 금액</span>을 먼저 확인합니다.</p>
<p>연결 점검은 <span class="og-hl og-hl--blue">health endpoint</span>와 앱 화면을 분리해서 봅니다.</p>
```

## Variants from the samples

| Variant | CSS idea | Use case |
| --- | --- | --- |
| Basic yellow | `linear-gradient(transparent 62%, #fff176 62%)` | stronger reminder inside a short sentence |
| Thin blue | `linear-gradient(transparent 78%, #a5d8ff 78%)` | calm informational emphasis |
| Thick pink | `linear-gradient(transparent 50%, #ffc9c9 50%)` | one important caution, used sparingly |
| Skew green | `transform:skewX(-3deg); display:inline-block` | hand-marked feel in illustrative callouts; avoid in dense UI copy |
| Rounded orange | `padding:1px 6px; border-radius:3px; box-decoration-break:clone` | multi-line phrase emphasis |
| Animated reveal | `background-size:0% 100%` → `100% 100%` | intro/hero or active focus card only; respect reduced motion |

## Manual-specific rules

- Highlight the **reader's decision/check**, not the implementation detail unless the implementation label is what the reader sees.
- Keep colors semantic but soft:
  - yellow = must-not-miss check;
  - blue = neutral information/evidence;
  - pink/red = caution/risk;
  - green = success/ready state.
- Use `box-decoration-break: clone` so line-wrapped Korean phrases keep rounded ends.
- Avoid hover-only meaning. Hover animation can be decorative, but the highlighted text must still be visibly highlighted without hover on touch/mobile and screenshots.
- For screenshot callouts, use separate callout boxes; do not use inline text highlighting to replace arrows/boxes on images.
- In generated manuals, prefer the `og-hl` namespace to avoid collisions with product CSS.

## QA checklist

- [ ] Highlighted phrases are short and meaningful, not decorative.
- [ ] Highlight is visible in static screenshots and exported views, not only on hover.
- [ ] Multi-line highlighted text preserves rounded ends.
- [ ] Animation is optional and disabled or harmless under `prefers-reduced-motion`.
- [ ] Colors have enough contrast with text and do not imply an unsupported status.

## Source samples

- `assets/highlight-samples.html` — six individual highlighter/underline variations.
- `assets/highlight-combined.html` — preferred combined thin rounded animated style.
