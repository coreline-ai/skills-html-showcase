# Web Search Fallback Pattern

Use this when direct X collection is unavailable but the user still wants a read-only trend report. This is a fallback, not equivalent to authenticated X/API collection.

## When to use

- `x-cli` or X API credentials are unavailable.
- Browser access to X redirects to login or cannot read current posts.
- The user accepts public web/search evidence as enough for a broad trend scan.

Do **not** use this pattern when the user requires live timeline fidelity, engagement metrics, replies, or complete post text.

## Procedure

1. Search the web with X-focused queries such as:
   - `site:x.com AI OR LLM launch announce`
   - `site:x.com AI paper benchmark research`
   - `site:x.com AI startup funding enterprise`
   - `site:x.com AI agent workflow automation`
2. Collect more candidates than needed, then dedupe by exact URL.
3. Normalize only what is visible from search results/snippets or extractable public pages.
4. Mark unavailable metrics (`views`, `likes`) as `0`; never estimate them from popularity or author reputation.
5. If the content is snippet-derived rather than direct post text, say so in the final answer and avoid overstating precision.
6. Generate `records.json`, then run `scripts/build_outputs.py` as usual.
7. Verify:
   - JSON parses and has the target count.
   - URLs are unique.
   - Excel row count matches merged total.
   - HTML opens and has no obvious JavaScript console errors if browser tools are available.

## Reporting language

Use wording like:

> Direct X/API collection was unavailable, so I used public web-search results pointing to X URLs. Engagement metrics were unavailable and are set to 0 rather than guessed.

Avoid wording like:

> I crawled X directly.
> These are the top X posts by engagement.

unless those claims were actually verified through X/API or an authenticated browser session.
