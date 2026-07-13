# Technical Verification Checklist

Run this separately from content verification. Passing this checklist means the manual artifacts work technically; it does not prove the manual teaches the right thing.

## App/System Access

- [ ] The documented environment is reachable.
- [ ] Required account/role/permissions are available.
- [ ] Demo/staging/safe data is used for risky actions.
- [ ] No permission, payment, password, or production-destructive prompt was bypassed without approval.

## Routes and Links

- [ ] All internal links open.
- [ ] All external links open or are intentionally marked unavailable.
- [ ] Documented routes do not 404/redirect unexpectedly.
- [ ] Console/runtime errors are checked when working with web apps.

## Media Assets

- [ ] Images exist at the referenced paths/URLs.
- [ ] Images have non-zero dimensions and are not placeholders unless labeled as such.
- [ ] Videos load metadata, have expected duration, and play from start.
- [ ] Embeds/iframes are reachable and sized correctly.
- [ ] Captions, posters, thumbnails, or review images match the lesson.

## Output Verification

- [ ] Generated PDF/HTML/MD/image/video exports open on a clean viewer/browser.
- [ ] Mobile/desktop viewport assumptions are stated or checked.
- [ ] File names and versions are unambiguous.
- [ ] Final artifact paths are listed in the handoff.
