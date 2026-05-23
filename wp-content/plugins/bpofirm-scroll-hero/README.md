# BPO Firm — Service-Page Blocks

WordPress plugin that ships two service-page building blocks for bpofirm.com:

| Shortcode | What it renders |
|---|---|
| `[bpofirm_scroll_hero]` | Scroll-driven expanding media hero (the "main banner"). Hijacks wheel + touch on first paint; expands a 300×400 centered media block to fill the viewport as the user scrolls; reveals inner content once fully expanded. Vanilla-JS port of the React `ScrollExpandMedia` component. |
| `[bpofirm_integrations]` | Two-row infinite icon carousel with brand-red hover lift. Goes directly under the main banner. Vanilla port of the React `IntegrationHero` component. |

Both blocks are styled to match the bpofirm.com brand (accent red `#ef494b`, blue-200 titles on the hero).

## Install

1. Upload the `bpofirm-scroll-hero/` folder to `wp-content/plugins/`.
2. **Plugins → Activate** "BPO Firm Service-Page Blocks".
3. Open any service page in Elementor.
4. Add an **Elementor → Shortcode** widget and paste the snippet for that page from [`reference/scroll-hero-rollout.md`](../../reference/scroll-hero-rollout.md).

## Shortcode reference

### `[bpofirm_scroll_hero]`

| Attribute | Default | Notes |
|---|---|---|
| `title` | `""` | Page title. First word slides left, the rest slide right during expansion. |
| `media_type` | `image` | `image` or `video`. |
| `media_src` | `…/Partner-with-BPO-Firm.webp` | Foreground image / video / YouTube embed URL. Placeholder image is already on the site's CDN. |
| `poster` | `""` | Optional poster for `video`. |
| `bg_src` | `…/vecteezy_dotted-world-map_1198050-1024x491.png` | Full-screen background image. |
| `date` | `""` | Optional small label above the scroll-prompt. |
| `scroll_label` | `Scroll to Expand` | Scroll-prompt label. Set to empty string to hide. |
| `text_blend` | `1` | `1` keeps `mix-blend-mode: difference` on the title (default) — adaptive contrast against both the light page bg and the dark gradient card. Set to `0` to force the flat blue-200 colour. |

Content between the opening / closing tags becomes the post-expand body (hidden until expansion completes):

```text
[bpofirm_scroll_hero title="Search Engine Optimization"]
Your post-expand body here. Plain text or nested shortcodes.
[/bpofirm_scroll_hero]
```

### `[bpofirm_integrations]`

| Attribute | Default | Notes |
|---|---|---|
| `badge` | `⚡ Integrations` | Pill above the title. Empty string hides it. |
| `title` | `Integrate with favorite tools` |  |
| `description` | `250+ top apps are available…` |  |
| `cta_label` | `Get started` |  |
| `cta_url` | `/contact-us/` |  |
| `icons_row1` | Default 7 Flaticon URLs | Comma-separated list of icon image URLs for the top row (scrolls left). |
| `icons_row2` | Default 7 Flaticon URLs | Comma-separated list for the bottom row (scrolls right). |
| `repeat` | `4` | How many times to repeat each list (keeps the loop seamless). Minimum 2. |

Hover an icon to pause its row and see the chip lift with a red-glow ring.

## Behaviour notes

- **Scroll hijack.** The hero blocks page scroll on every page it appears on, until the user finishes expanding it. This is intentional (matches the React reference) but be aware: stacking it on 44 pages means the hijack runs on every navigation.
- **Reverse.** Wheeling / swiping *up* while already expanded and scrolled to the top of the page collapses the hero again.
- **Custom cursor.** The existing global custom cursor on bpofirm.com (red dot + blue blur) sits on top and continues to work.
- **Reduced motion.** Honors `prefers-reduced-motion: reduce` — the carousel stops auto-scrolling and the hero's transitions become instant.
- **Mobile.** Hero sizing uses smaller deltas on screens < 768 px. Custom cursor is removed by the site's existing snippet on mobile UA.

## Where to put the shortcodes in Elementor

For every page in `reference/scroll-hero-rollout.md`:

1. Edit the page in Elementor.
2. **Add a new Section at the very top** → drag a **Shortcode** widget into it → paste the `[bpofirm_scroll_hero …]` line.
3. **Add a second Section right below it** → drag another **Shortcode** widget → paste the `[bpofirm_integrations …]` line.
4. The existing page content lives below those two sections.
5. **Update** and check on desktop + mobile.

## File layout

```
bpofirm-scroll-hero/
├── bpofirm-scroll-hero.php        Plugin bootstrap + both shortcodes
├── assets/
│   ├── scroll-hero.css            Hero styles (drives via CSS vars)
│   ├── scroll-hero.js             Scroll-hijack + progress driver
│   └── integrations.css           Carousel + hover effects
└── README.md                      This file
```
