# BPO Firm — Design System

Foundational design tokens for the dark-portfolio aesthetic adopted on **Home, About, and Contact**. Service pages keep the lighter design from the `bpofirm-scroll-hero` plugin.

## What it ships

- **Google Fonts** — Inter (300–700) + Instrument Serif (italic 400)
- **CSS custom properties** — `--bg`, `--surface`, `--text`, `--muted`, `--stroke` (HSL components, no `hsl()` wrapper, same pattern as the reference)
- **Brand accent gradient** — `#ef494b → #b91c1c` (BPO Firm red, replacing the reference's blue)
- **Type-scale utilities** — `.bpo-display`, `.bpo-eyebrow`, `.bpo-muted`, `.bpo-surface`
- **Accent utilities** — `.bpo-accent-gradient`, `.bpo-accent-gradient-text`, `.bpo-accent-ring`, `.bpo-accent-glow`
- **Custom keyframes** — `bpo-scroll-down`, `bpo-role-fade-in`, `bpo-gradient-shift` with matching `.bpo-animate-*` classes
- Honours `prefers-reduced-motion`

## How it scopes

All dark-theme styles live inside `.bpo-dark`. The plugin auto-adds this class to the `<body>` on these slugs (filterable):

```
home, front-page, about, about-us, contact, contact-us
```

For any other page you want dark, drop the opt-in shortcode anywhere on the page:

```text
[bpofirm_dark_theme]
```

To change the auto-list:

```php
add_filter( 'bpofirm_dark_page_slugs', function ( $slugs ) {
    return array_merge( $slugs, array( 'pricing', 'careers' ) );
} );
```

## Install

1. Upload `bpofirm-design-system/` to `wp-content/plugins/`.
2. **Plugins → Activate** "BPO Firm Design System".
3. Visit your Home page — body should now have `class="… bpo-dark"` and pages adopt the dark background.

## Companion plugins

- **bpofirm-scroll-hero** — Service-page blocks (scroll-expand hero + integrations carousel). Light theme.
- Coming next — Hero, Selected Works, Journal, Explorations, Stats, Contact/Marquee blocks for the dark pages.

## Token reference (preview)

`preview/design-tokens.html` renders every token side-by-side. Run `node preview/screenshot.js` to regenerate the visual snapshot.
