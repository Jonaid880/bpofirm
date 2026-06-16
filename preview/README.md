# Preview harness

Standalone HTML page + Playwright screenshot script so every change to the
`bpofirm-scroll-hero` WP plugin can be visually verified without spinning up
WordPress.

`index.html` mirrors the markup the plugin's shortcodes emit and links the
plugin's actual `assets/*.css` / `*.js`. Asset URLs (hero bg/fg + carousel
icons) are inline SVG data URIs because this sandbox blocks external image
hosts (403 from Flaticon / bpofirm CDN) — the live plugin still references
the real URLs.

## Run locally

```bash
NODE_PATH=/opt/node22/lib/node_modules node preview/screenshot.js
# screenshots land in preview/screenshots/
```

## What it captures

| File | Showing |
|---|---|
| `{desktop,mobile}-hero-initial.png` | Banner at progress=0 (card 300×400, scroll prompt visible) |
| `{desktop,mobile}-hero-mid-expand.png` | progress=0.5 (card grown, title sliding off) |
| `{desktop,mobile}-hero-expanded.png` | progress=1 (full-bleed card, bg faded) |
| `{desktop,mobile}-integrations-default.png` | Carousel rolling at default state |
| `{desktop,mobile}-integrations-hover.png` | Leftmost chip with brand-red hover lift + ring |

Add new states by extending the `states` array in `screenshot.js`.
