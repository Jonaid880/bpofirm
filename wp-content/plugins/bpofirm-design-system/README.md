# BPO Firm — Design System

Foundational design tokens for **Home, About, and Contact** — locked with owner. Uses bpofirm.com's original brand palette (red + blue accents on a light bg) but adopts the section structure, type pairing and animation library from the React portfolio reference. Service pages keep the lighter blocks shipped via `bpofirm-scroll-hero`.

## What it ships

- **Google Fonts** — Inter (300–700) + Instrument Serif (italic 400)
- **Brand tokens**
  - `--bpo-brand` `#ef494b` (primary accent — CTAs, highlights, custom cursor)
  - `--bpo-brand-dark` `#b91c1c` (paired darker stop for the accent gradient)
  - `--bpo-brand-blue` `#0a58ca` (secondary accent — links, cursor trail)
  - `--bpo-accent-gradient` `linear-gradient(90deg, #ef494b, #b91c1c)`
- **Page surface tokens (HSL components)** — `--bg`, `--surface`, `--text`, `--muted`, `--stroke`
- **Type utilities** — `.bpo-display`, `.bpo-eyebrow`, `.bpo-muted`, `.bpo-surface`, `.bpo-brand-red`, `.bpo-brand-blue`
- **Accent utilities** — `.bpo-accent-gradient`, `.bpo-accent-gradient-text`, `.bpo-accent-ring`, `.bpo-accent-glow`
- **Custom keyframes** — `bpo-scroll-down`, `bpo-role-fade-in`, `bpo-gradient-shift` with matching `.bpo-animate-*` classes
- **Dark-section utility** — `.bpo-section-dark` flips a single block to dark within an otherwise light page (for the occasional CTA band / footer)
- Honours `prefers-reduced-motion`

## Scoping

All theme rules live inside `.bpo-page`. The plugin auto-adds this class to the `<body>` on:

```
home, front-page, about, about-us, contact, contact-us
```

Filterable via `bpofirm_dark_page_slugs` (legacy hook name — renaming would break opt-ins, kept as-is). To opt-in any other page, drop:

```text
[bpofirm_brand_theme]
```

## Install

1. Upload `bpofirm-design-system/` to `wp-content/plugins/`.
2. **Plugins → Activate** "BPO Firm Design System".
3. Visit Home — body picks up `class="… bpo-page"` and starts rendering with the token system.

## Token reference

`preview/design-tokens.html` renders every token side-by-side. Run `node preview/screenshot.js` to regenerate the snapshot.
