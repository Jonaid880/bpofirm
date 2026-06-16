# Service-page rollout — `[bpofirm_scroll_hero]` + `[bpofirm_integrations]`

> Scope locked with owner: **service pages only** (Digital Marketing tree + Call Services tree). 44 pages total. Not Home, About, Career, Insights, Pricing, Contact, or legal pages.
>
> For each page below:
> 1. Open in Elementor.
> 2. Add a Section at the top with a **Shortcode** widget containing the first snippet (banner).
> 3. Add a second Section right below it with another **Shortcode** widget containing the integrations snippet.
> 4. Update.
>
> Placeholder media is intentionally identical across pages — owner will swap `media_src` and `bg_src` per page when imagery is ready.

> **Recommendation on scroll-hijack scope.** The dynamic scroll-expand effect is signature on first impression but irritating on repeat visits — and forcing it on every sibling-page navigation (e.g. SEO → PPC → Email) is rough. Suggested split:
> - **7 hub pages** (Digital Marketing + Call Services + the 5 group hubs) → dynamic `[bpofirm_scroll_hero …]` (scroll hijack on).
> - **37 leaf pages** (every individual service) → add `static="1"` to switch to a non-hijacking banner. Page scrolls normally; the same visual identity, no forced interaction.
>
> Both forms accept identical attributes — just add or remove `static="1"`. Owner override welcome; defaults below leave it off so each page matches the original brief.

---

## Progress tracker

| # | URL | Banner added | Integrations added |
|---|---|---|---|
| 1 | `/digital-marketing/` | ☐ | ☐ |
| 2 | `/digital-marketing/search-engine-optimization/` | ☐ | ☐ |
| 3 | `/digital-marketing/pay-per-click/` | ☐ | ☐ |
| 4 | `/digital-marketing/social-media-marketing/` | ☐ | ☐ |
| 5 | `/digital-marketing/content-marketing/` | ☐ | ☐ |
| 6 | `/digital-marketing/email-marketing/` | ☐ | ☐ |
| 7 | `/digital-marketing/conversion-rate-optimization/` | ☐ | ☐ |
| 8 | `/digital-marketing/marketing-analytics-and-reporting/` | ☐ | ☐ |
| 9 | `/digital-marketing/website-ux-support/` | ☐ | ☐ |
| 10 | `/digital-marketing/e-commerce-marketing-support/` | ☐ | ☐ |
| 11 | `/digital-marketing/online-reputation-management/` | ☐ | ☐ |
| 12 | `/digital-marketing/app-development/` | ☐ | ☐ |
| 13 | `/digital-marketing/graphic-designing/` | ☐ | ☐ |
| 14 | `/call-services/` | ☐ | ☐ |
| 15 | `/call-services/inbound-call-services/` | ☐ | ☐ |
| 16 | `…/inbound-call-services/customer-support/` | ☐ | ☐ |
| 17 | `…/inbound-call-services/technical-support/` | ☐ | ☐ |
| 18 | `…/inbound-call-services/help-desk-services/` | ☐ | ☐ |
| 19 | `…/inbound-call-services/order-processing/` | ☐ | ☐ |
| 20 | `…/inbound-call-services/appointment-scheduling/` | ☐ | ☐ |
| 21 | `…/inbound-call-services/receptionist-virtual-front-desk/` | ☐ | ☐ |
| 22 | `/call-services/outbound-call-services/` | ☐ | ☐ |
| 23 | `…/outbound-call-services/telemarketing/` | ☐ | ☐ |
| 24 | `…/outbound-call-services/lead-generation/` | ☐ | ☐ |
| 25 | `…/outbound-call-services/sales-calls/` | ☐ | ☐ |
| 26 | `…/outbound-call-services/follow-up-calls/` | ☐ | ☐ |
| 27 | `…/outbound-call-services/debt-collection-payment-reminders/` | ☐ | ☐ |
| 28 | `…/outbound-call-services/market-research-surveys/` | ☐ | ☐ |
| 29 | `/call-services/omnichannel-support-services/` | ☐ | ☐ |
| 30 | `…/omnichannel-support-services/live-chat-support/` | ☐ | ☐ |
| 31 | `…/omnichannel-support-services/email-support/` | ☐ | ☐ |
| 32 | `…/omnichannel-support-services/social-media-support/` | ☐ | ☐ |
| 33 | `…/omnichannel-support-services/whatsapp-messaging-support/` | ☐ | ☐ |
| 34 | `/call-services/industry-specific-bpo-call-services/` | ☐ | ☐ |
| 35 | `…/industry-specific-bpo-call-services/healthcare/` | ☐ | ☐ |
| 36 | `…/industry-specific-bpo-call-services/real-estate/` | ☐ | ☐ |
| 37 | `…/industry-specific-bpo-call-services/e-commerce/` | ☐ | ☐ |
| 38 | `/call-services/specialized-high-end-bpo-services/` | ☐ | ☐ |
| 39 | `…/specialized-high-end-bpo-services/multilingual-call-center/` | ☐ | ☐ |
| 40 | `…/specialized-high-end-bpo-services/executive-assistant-support/` | ☐ | ☐ |
| 41 | `…/specialized-high-end-bpo-services/ai-augmented-call-services/` | ☐ | ☐ |
| 42 | `…/specialized-high-end-bpo-services/common-bpo-service-packages/` | ☐ | ☐ |
| 43 | `…/specialized-high-end-bpo-services/industries-that-frequently-outsource-bpo-services/` | ☐ | ☐ |
| 44 | `…/specialized-high-end-bpo-services/high-demand-bpo-niches-in-2026/` | ☐ | ☐ |

---

## Per-page shortcodes

The integrations snippet is identical for every service page — copy this once and paste it on all 44 pages:

```text
[bpofirm_integrations]
```

The banner snippet differs by `title`. For each page below, copy the line shown.

### Digital Marketing tree

```text
[bpofirm_scroll_hero title="Digital Marketing"]
[bpofirm_scroll_hero title="Search Engine Optimization"]
[bpofirm_scroll_hero title="Pay-Per-Click"]
[bpofirm_scroll_hero title="Social Media Marketing"]
[bpofirm_scroll_hero title="Content Marketing"]
[bpofirm_scroll_hero title="Email Marketing"]
[bpofirm_scroll_hero title="Conversion Rate Optimization"]
[bpofirm_scroll_hero title="Marketing Analytics & Reporting"]
[bpofirm_scroll_hero title="Website & UX Support"]
[bpofirm_scroll_hero title="E-commerce Marketing Support"]
[bpofirm_scroll_hero title="Online Reputation Management"]
[bpofirm_scroll_hero title="App Development"]
[bpofirm_scroll_hero title="Graphic Designing"]
```

### Call Services — hubs

```text
[bpofirm_scroll_hero title="Call Services"]
[bpofirm_scroll_hero title="Inbound Call Services"]
[bpofirm_scroll_hero title="Outbound Call Services"]
[bpofirm_scroll_hero title="Omnichannel Support Services"]
[bpofirm_scroll_hero title="Industry-Specific BPO Call Services"]
[bpofirm_scroll_hero title="Specialized High-End BPO Services"]
```

### Inbound Call Services — leaves

```text
[bpofirm_scroll_hero title="Customer Support"]
[bpofirm_scroll_hero title="Technical Support"]
[bpofirm_scroll_hero title="Help Desk Services"]
[bpofirm_scroll_hero title="Order Processing"]
[bpofirm_scroll_hero title="Appointment Scheduling"]
[bpofirm_scroll_hero title="Receptionist & Virtual Front Desk"]
```

### Outbound Call Services — leaves

```text
[bpofirm_scroll_hero title="Telemarketing"]
[bpofirm_scroll_hero title="Lead Generation"]
[bpofirm_scroll_hero title="Sales Calls"]
[bpofirm_scroll_hero title="Follow-Up Calls"]
[bpofirm_scroll_hero title="Debt Collection & Payment Reminders"]
[bpofirm_scroll_hero title="Market Research & Surveys"]
```

### Omnichannel Support — leaves

```text
[bpofirm_scroll_hero title="Live Chat Support"]
[bpofirm_scroll_hero title="Email Support"]
[bpofirm_scroll_hero title="Social Media Support"]
[bpofirm_scroll_hero title="WhatsApp & Messaging Support"]
```

### Industry-Specific — leaves

```text
[bpofirm_scroll_hero title="Healthcare BPO"]
[bpofirm_scroll_hero title="Real Estate BPO"]
[bpofirm_scroll_hero title="E-Commerce BPO"]
```

### Specialized High-End — leaves

```text
[bpofirm_scroll_hero title="Multilingual Call Center"]
[bpofirm_scroll_hero title="Executive Assistant Support"]
[bpofirm_scroll_hero title="AI-Augmented Call Services"]
[bpofirm_scroll_hero title="Common BPO Service Packages"]
[bpofirm_scroll_hero title="Industries That Frequently Outsource"]
[bpofirm_scroll_hero title="High-Demand BPO Niches in 2026"]
```

---

## When the real imagery is ready

For each page, extend its banner shortcode with the per-page assets. Example:

```text
[bpofirm_scroll_hero
  title="Lead Generation"
  media_type="image"
  media_src="https://bpofirm.com/wp-content/uploads/2026/06/lead-generation-hero.webp"
  bg_src="https://bpofirm.com/wp-content/uploads/2026/06/lead-generation-bg.webp"
  scroll_label="Scroll to Expand"]
```

For a video hero:

```text
[bpofirm_scroll_hero
  title="AI-Augmented Call Services"
  media_type="video"
  media_src="https://bpofirm.com/wp-content/uploads/2026/06/ai-augmented-call.mp4"
  poster="https://bpofirm.com/wp-content/uploads/2026/06/ai-augmented-call-poster.webp"
  bg_src="https://bpofirm.com/wp-content/uploads/2026/06/ai-augmented-call-bg.webp"]
```

If a particular page needs different integration icons (e.g. healthcare-specific tools on `/healthcare/`):

```text
[bpofirm_integrations
  title="Plays nicely with your healthcare stack"
  description="HIPAA-aligned hand-offs with Epic, Cerner, Athenahealth, NextGen and more."
  icons_row1="https://example.com/epic.png,https://example.com/cerner.png,..."
  icons_row2="https://example.com/athenahealth.png,https://example.com/nextgen.png,..."]
```
