# BPO Firm — Cinematic Hero

Drop-in WordPress shortcode that renders the cinematic intro hero: dark warm atmosphere → animated keypad entering a 4-digit code → "Access Granted" badge → crossfade to interior view → headline + CTAs revealed.

Pure CSS choreography — no JavaScript state machine, no video file. Total cycle is 9 seconds. Default mode plays the intro **once** then holds on the interior view forever.

Inspired by the `@octaboot.lb` real-estate Reel; brand-adapted to BPO Firm (brand-red CTAs + accent, warm golden cinematic atmosphere).

## Shortcode

```text
[bpofirm_cinematic_hero
    title="Welcome inside |BPO Firm|."
    eyebrow="A partnership unlocked"
    lede="Calls. Chats. Social. AI assists. Every channel — orchestrated under one roof."
    cta_primary_label="Book a discovery call"
    cta_primary_url="/contact-us/"
    cta_secondary_label="See our work"
    cta_secondary_url="/services/"
    code="1300"
    bg_exterior="https://bpofirm.com/wp-content/uploads/2026/06/hero-exterior.webp"
    bg_interior="https://bpofirm.com/wp-content/uploads/2026/06/hero-interior.webp"
]
```

### Attributes

| Attribute | Default | Notes |
|---|---|---|
| `title` | `Welcome inside \|BPO Firm\|.` | Wrap any phrase in `\|pipes\|` to render it in italic brand red. Multiple phrases supported. |
| `eyebrow` | `A partnership unlocked` | Small caps label above the headline. Empty string hides it. |
| `lede` | One-liner about channel orchestration | Body copy under the headline. |
| `cta_primary_label` / `_url` | `Book a discovery call` / `/contact-us/` | Solid brand-red CTA. |
| `cta_secondary_label` / `_url` | `See our work` / `/services/` | Outlined ghost CTA. |
| `code` | `1300` | The 4-digit code the keypad enters. Must be exactly 4 numeric digits. |
| `access_label` | `Access Granted` | Text inside the post-entry badge. |
| `bg_exterior` | dark warm gradient (placeholder) | URL of the "closed door / exterior" image. |
| `bg_interior` | warm interior gradient (placeholder) | URL of the "interior reveal" image (this is what visitors look at most of the time, so it matters most). |
| `loop` | `0` | `1` to cycle the intro forever (every 9s); `0` plays it once then holds. |

## Behaviour notes

- **Default = one-shot intro.** Plays through 1×, then settles on the interior view with title/lede/CTAs visible. Avoids the "stuck in a loop" annoyance on returning visits.
- **Loop mode.** Set `loop="1"` if you want the keypad → access-granted → interior reveal to cycle forever. Hypnotic but noisier — usually only worth it on a one-page demo.
- **prefers-reduced-motion.** Honored — the intro is skipped entirely and the interior view + content show instantly.
- **Backgrounds.** Use landscape ~1920×1080. Darker/warmer images hold the brand atmosphere best. The interior image is what's visible most of the time, so pick something with depth.
- **Accessibility.** The keypad stage carries `aria-hidden="true"`; the title + lede + CTAs are the real content.

## Install

1. Upload `bpofirm-cinematic-hero/` to `wp-content/plugins/`.
2. **Plugins → Activate** "BPO Firm Cinematic Hero".
3. On the Home page in Elementor, add a **Shortcode** widget at the very top of the page and paste the shortcode above (with your real image URLs).

## Companion plugins

- **bpofirm-design-system** — shared brand tokens (red, blue, Inter, Instrument Serif). Loads automatically.
- **bpofirm-scroll-hero** — service-page blocks (scroll-expand hero + integrations carousel). Independent.
