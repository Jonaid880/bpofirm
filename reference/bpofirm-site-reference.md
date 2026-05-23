# bpofirm.com — Complete Site Reference

> Source-of-truth notes for the existing bpofirm.com website, to use as the content / structural blueprint for the new theme.
> Direct fetching of bpofirm.com from this sandbox returns HTTP 403 `host_not_allowed`, so the site owner is pasting page HTML and screenshots URL-by-URL.

---

## 1. Brand identity

| Field | Value |
|---|---|
| Public brand | **BPO Firm** (also styled **BPO FIRM**, **BPO FirM**) |
| Legal entity | **BPO FM SMC PVT LTD** |
| Tagline (homepage H1) | "Outsourced Operations Teams, Live in 7 Business Days" |
| Sub-tagline (H2) | "Call Centre, Back Office, Factoring & Digital Marketing — Fully Managed by BPO Firm" |
| Site description (Schema) | "BPO Firm is revenue-driven BPO partner" |
| Domain | https://bpofirm.com/ |
| Email | **info@bpofirm.com** |
| Phone | **+92 304 8444422** |
| Office address | Block H Gulberg 2, Lahore, 55050, Pakistan |
| Hours | 24 / 7 (Mon–Sun, 00:00–23:59) |
| Areas served | US, UK, AU, EU |
| Languages | English |
| Founded / since | 2000 (used in copy) |
| Site verification | google-site-verification: `n8sUuiVuRN3VSIFzqd89TfpDhSGkWBbtZnNuMqhi3G4` |

### Logos / favicon (URLs)
- Primary 3D logo: `https://bpofirm.com/wp-content/uploads/cropped-3d-logo.png` (204×179)
- Alt logo (webp): `https://bpofirm.com/wp-content/uploads/cropped-BPO-FIRM-Logo.webp`
- Older logo (PNG): `https://bpofirm.com/wp-content/uploads/2024/11/bpofirm-logo.png`
- Favicon 32: `…/2026/01/cropped-cropped-Final-BPO-Logo-png-01-32x32.png`
- Favicon 192: `…/2026/01/cropped-cropped-Final-BPO-Logo-png-01-192x192.png`
- Apple-touch-icon 180: `…/2026/01/cropped-cropped-Final-BPO-Logo-png-01-180x180.png`
- MS tile 270: `…/2026/01/cropped-cropped-Final-BPO-Logo-png-01-270x270.png`

### Social media (verified from live HTML)
- LinkedIn: https://www.linkedin.com/company/110216707/
- YouTube: https://www.youtube.com/@BPO-Firm
- Facebook: https://www.facebook.com/profile.php?id=61572473010176
- Instagram: https://www.instagram.com/bpofirm/

> Note: the live footer LinkedIn link points to a `/admin/page-posts/published/` URL — that's an admin URL accidentally pasted. The new theme should link to the public profile above.

---

## 2. Current tech stack (for migration reference)

| Layer | Tool |
|---|---|
| CMS | WordPress 6.9.4 |
| Theme | Hello Elementor 3.4.7 |
| Page builder | Elementor 4.0.9 + Elementor Pro 4.0.4.2 |
| SEO | Yoast SEO 27.6 |
| Caching | LiteSpeed Cache 7.8.1 |
| Analytics | Google Site Kit, GA4 tag `GT-K4TCBH8B`, Google Ads `AW-17543711833` |
| Tag manager | `GTM-PQ2D3Z64` |
| Fonts | Roboto, Roboto Slab, Poppins (Google Fonts) |

---

## 3. Design system

### Colors
- **Primary accent / brand red:** `#ef494b` (used in heading highlights, CTAs, custom cursor)
- **Cursor trail blue:** `rgba(10, 88, 202, 0.25)`
- Body backgrounds: white + dark sections; CTA band uses red/dark background with white text

### Typography
- Heading: Roboto Slab (h1, h2 likely use this) / Poppins
- Body: Roboto / Poppins

### Animations / interactions used
- Hero: container `slideInLeft`, headings `rotateInDownLeft`
- Section headings: `slideInDown` (animated-fast)
- Footer: `slideInUp`
- Cards: flip-box (front shows title + body, flips on hover/focus)
- World map: animated hotspot with soft-beat pulse + flag tooltip
- **Custom cursor:** 10px solid red dot (`#ef494b`) with a 30px blurred blue trail that lags behind (desktop only — removed on mobile UA)

### Buttons / CTAs (used site-wide)
- "Book a Discovery Call" → `/contact-us/`
- "Book a Service" → `/services/` *(note: this URL is referenced but wasn't in the supplied sitemap — may be a placeholder / 404)*
- "Contact Us" → `/contact-us/` (header)

---

## 4. Authoritative sitemap (corrected from live nav)

> Important: the URL list previously supplied used flat slugs (e.g. `/customer-support/`). The **live navigation uses nested URLs** (e.g. `/call-services/inbound-call-services/customer-support/`). These nested URLs are authoritative.

Status: ⬜ URL known · 🟨 partial content · ✅ full content

### 4.1 Top-level / corporate

| Status | URL | Page |
|---|---|---|
| ✅ | https://bpofirm.com/ | Home |
| ⬜ | https://bpofirm.com/about-us/ | About Us |
| ⬜ | https://bpofirm.com/pricing/ | Pricing |
| ⬜ | https://bpofirm.com/contact-us/ | Contact Us |
| ⬜ | https://bpofirm.com/services/ | Services hub *(referenced by CTAs)* |
| ⬜ | https://bpofirm.com/privacy-policy/ | Privacy Policy |
| ⬜ | https://bpofirm.com/terms-and-conditions/ | Terms & Conditions |

### 4.2 Insights (`/insights/`)
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/insights/ | Insights (hub) |
| ⬜ | https://bpofirm.com/insights/news/ | News |
| ⬜ | https://bpofirm.com/insights/blog/ | Blog |
| ⬜ | https://bpofirm.com/insights/case-study/ | Case Study |

### 4.3 Career (`/career/`)
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/career/ | Career |
| ⬜ | https://bpofirm.com/career/assessment-portal/ | Assessment Portal |

### 4.4 Digital Marketing (`/digital-marketing/`)
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/digital-marketing/ | Digital Marketing (hub) |
| ⬜ | https://bpofirm.com/digital-marketing/search-engine-optimization/ | SEO |
| ⬜ | https://bpofirm.com/digital-marketing/pay-per-click/ | Pay-Per-Click (PPC) |
| ⬜ | https://bpofirm.com/digital-marketing/social-media-marketing/ | Social Media Marketing (SMM) |
| ⬜ | https://bpofirm.com/digital-marketing/content-marketing/ | Content Marketing |
| ⬜ | https://bpofirm.com/digital-marketing/email-marketing/ | Email Marketing |
| ⬜ | https://bpofirm.com/digital-marketing/conversion-rate-optimization/ | Conversion Rate Optimization (CRO) |
| ⬜ | https://bpofirm.com/digital-marketing/marketing-analytics-and-reporting/ | Marketing Analytics & Reporting |
| ⬜ | https://bpofirm.com/digital-marketing/website-ux-support/ | Website & UX Support |
| ⬜ | https://bpofirm.com/digital-marketing/e-commerce-marketing-support/ | E-commerce Marketing Support |
| ⬜ | https://bpofirm.com/digital-marketing/online-reputation-management/ | Online Reputation Management (ORM) |
| ⬜ | https://bpofirm.com/digital-marketing/app-development/ | App Development |
| ⬜ | https://bpofirm.com/digital-marketing/graphic-designing/ | Graphic Designing |

### 4.5 Call Services (`/call-services/`)
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/call-services/ | Call Services (hub) |

**Inbound Call Services**
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/call-services/inbound-call-services/ | Inbound (hub) |
| ⬜ | …/inbound-call-services/customer-support/ | Customer Support |
| ⬜ | …/inbound-call-services/technical-support/ | Technical Support |
| ⬜ | …/inbound-call-services/help-desk-services/ | Help Desk Services |
| ⬜ | …/inbound-call-services/order-processing/ | Order Processing |
| ⬜ | …/inbound-call-services/appointment-scheduling/ | Appointment Scheduling |
| ⬜ | …/inbound-call-services/receptionist-virtual-front-desk/ | Receptionist / Virtual Front Desk |

**Outbound Call Services**
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/call-services/outbound-call-services/ | Outbound (hub) |
| ⬜ | …/outbound-call-services/telemarketing/ | Telemarketing |
| ⬜ | …/outbound-call-services/lead-generation/ | Lead Generation |
| ⬜ | …/outbound-call-services/sales-calls/ | Sales Calls |
| ⬜ | …/outbound-call-services/follow-up-calls/ | Follow-Up Calls |
| ⬜ | …/outbound-call-services/debt-collection-payment-reminders/ | Debt Collection & Payment Reminders |
| ⬜ | …/outbound-call-services/market-research-surveys/ | Market Research & Surveys |

**Omnichannel Support Services**
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/call-services/omnichannel-support-services/ | Omnichannel (hub) |
| ⬜ | …/omnichannel-support-services/live-chat-support/ | Live Chat Support |
| ⬜ | …/omnichannel-support-services/email-support/ | Email Support |
| ⬜ | …/omnichannel-support-services/social-media-support/ | Social Media Support |
| ⬜ | …/omnichannel-support-services/whatsapp-messaging-support/ | WhatsApp & Messaging Support |

**Industry-Specific BPO Call Services**
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/call-services/industry-specific-bpo-call-services/ | Industry-Specific (hub) |
| ⬜ | …/industry-specific-bpo-call-services/healthcare/ | Healthcare |
| ⬜ | …/industry-specific-bpo-call-services/real-estate/ | Real Estate |
| ⬜ | …/industry-specific-bpo-call-services/e-commerce/ | E-Commerce |

**Specialized High-End BPO Services**
| Status | URL | Page |
|---|---|---|
| ⬜ | https://bpofirm.com/call-services/specialized-high-end-bpo-services/ | Specialized High-End (hub) |
| ⬜ | …/specialized-high-end-bpo-services/multilingual-call-center/ | Multilingual Call Center |
| ⬜ | …/specialized-high-end-bpo-services/executive-assistant-support/ | Executive Assistant Support |
| ⬜ | …/specialized-high-end-bpo-services/ai-augmented-call-services/ | AI-Augmented Call Services |
| ⬜ | …/specialized-high-end-bpo-services/common-bpo-service-packages/ | Common BPO Service Packages |
| ⬜ | …/specialized-high-end-bpo-services/industries-that-frequently-outsource-bpo-services/ | Industries That Frequently Outsource BPO Services |
| ⬜ | …/specialized-high-end-bpo-services/high-demand-bpo-niches-in-2026/ | High-Demand BPO Niches in 2026 |

**Total confirmed pages: 56** (1 home + 6 corporate + 4 insights + 2 career + 13 digital marketing + 6 inbound + 7 outbound + 5 omnichannel + 4 industry + 7 specialized + 1 services hub).

---

## 5. Header / global navigation (verified from live HTML)

```
[Logo]   About Us   Digital Marketing ▾   Call Services ▾   Career ▾   Insights ▾          [Contact Us]
                    ├─ SEO                  ├─ Inbound Call Services ▸  ├─ Assessment Portal   ├─ News
                    ├─ PPC                  │   ├─ Customer Support                            ├─ Blog
                    ├─ SMM                  │   ├─ Technical Support                           └─ Case Study
                    ├─ Content Marketing    │   ├─ Help Desk Services
                    ├─ Email Marketing      │   ├─ Order Processing
                    ├─ CRO                  │   ├─ Appointment Scheduling
                    ├─ Marketing Analytics  │   └─ Receptionist / Virtual Front Desk
                    ├─ Website & UX Support ├─ Outbound Call Services ▸
                    ├─ E-commerce Mktg      │   ├─ Telemarketing
                    ├─ ORM                  │   ├─ Lead Generation
                    ├─ App Development      │   ├─ Sales Calls
                    └─ Graphic Designing    │   ├─ Follow-Up Calls
                                            │   ├─ Debt Collection & Payment Reminders
                                            │   └─ Market Research & Surveys
                                            ├─ Omnichannel Support ▸
                                            │   ├─ Live Chat / Email / Social / WhatsApp
                                            ├─ Industry-Specific ▸
                                            │   ├─ Healthcare / Real Estate / E-Commerce
                                            └─ Specialized High-End ▸
                                                ├─ Multilingual Call Center
                                                ├─ Executive Assistant Support
                                                ├─ AI-Augmented Call Services
                                                ├─ Common BPO Service Packages
                                                ├─ Industries That Frequently Outsource
                                                └─ High-Demand BPO Niches in 2026
```

Header layout: fixed-position, hidden on tablet/mobile (replaced by burger). Logo left, menu center, "Contact Us" button right.

> **Missing from header (recommend adding to new theme):** Pricing, Services hub link. They appear in the footer Quick Links but not in the top nav.

---

## 6. Global footer (verified from live HTML)

Layout: 5 columns (logo, Services, Quick Links, Social Links, Map embed) + bottom strip (copyright + legal links).

**Column — Services**
- Search Engine Optimization → `/digital-marketing/search-engine-optimization/`
- Pay-Per-Click (PPC) → `/digital-marketing/pay-per-click/`
- Digital Marketing Services → `/digital-marketing/`
- eCommerce Support Service → `/digital-marketing/e-commerce-marketing-support/`
- App Development → `/app-development/`  *(broken link — should be `/digital-marketing/app-development/`)*

**Column — Quick Links**
- About Us → `/about-us/`
- Services → `/services/`
- Pricing → `/pricing/`
- Blog → `/insights/blog/`

**Column — Social Links**
- LinkedIn → *(currently a broken admin URL — fix to `https://www.linkedin.com/company/110216707/`)*
- YouTube → `https://www.youtube.com/@BPO-Firm`
- Facebook → `https://www.facebook.com/profile.php?id=61572473010176`
- Instagram → `https://www.instagram.com/bpofirm/`

**Column — Map**
- Google Maps embed of "BPO FM SMC PVT LTD" at Lahore (lat 31.531317, lng 74.350238). 600×150.

**Bottom strip**
- `© Copyright BPO FIRM 2026`
- Privacy Policy · Terms and conditions

---

## 7. Per-page content log

### 7.1 ✅ Home — `/`

**SEO**
- `<title>`: *BPO Firm — Outsourced Call Centre & Back Office in 7 Days*
- Meta description: *Outsourced call centre, back office & digital marketing teams — built, trained and live in 7 business days. Cut operational cost 30-70%. Pilot risk-free. Trusted by SMEs globally.*
- Canonical: https://bpofirm.com/
- OG image: `https://bpofirm.com/wp-content/uploads/Partner-with-BPO-Firm.webp` (1024×576, alt "Partner with BPO Firm")
- Schema: WebPage + Organization + LocalBusiness + ProfessionalService + WebSite (full JSON-LD captured in `reference/raw/home-jsonld.json` if needed)

**Section 1 — Hero**
- Background: looping muted video `https://bpofirm.com/wp-content/uploads/2026/01/191684-891315375_small.mp4` (plays on mobile too)
- H1: **Outsourced Operations Teams, Live in 7 Business Days**
- H2: Call Centre, Back Office, Factoring & Digital Marketing — Fully Managed by BPO Firm
- Body: Cut operational cost 30-70% without an in-house hire. Vetted teams, trained to your SOPs, in production in 7 business days. Trusted by SMEs and mid-market firms in the US, UK, AU and EU.
- Primary CTA: **Book a Discovery Call** → `/contact-us/`
- Animations: container slideInLeft; H1 + H2 rotateInDownLeft

**Section 2 — Our Core Services** *(4 flip cards, 2×2 grid)*
- H2: <span style="color:#ef494b">Our Core</span> services
- Lede: BPO Firm delivers specialized Business Process Outsourcing (BPO) and Knowledge Process Outsourcing (KPO) across customer experience, back-office, and high-value data analytics. Our service model utilizes a **"Human-in-the-Loop" architecture**, where AI automates routine tasks while our specialists handle complex, high-stakes decision-making to ensure 99.9% accuracy and enhanced brand loyalty.
- CTA: **Book a Service** → `/services/`

  **Card 1 — Back Office Services**
  > Work Smarter Behind the Scenes. From data entry and document management to administrative support and reporting, our back-office teams keep your operations running smoothly — without the cost of building an in-house department. We handle the details so you can focus on the big picture.

  **Card 2 — Call Center Services**
  > Every Call Handled. Every Customer Valued. Our inbound and outbound call center teams are trained to represent your brand with professionalism and empathy. Whether it's customer support, lead generation, appointment setting, or order management — we deliver seamless voice and non-voice experiences that keep your customers coming back.

  **Card 3 — Digital Marketing Services**
  > Grow Your Brand. Drive Real Revenue. From SEO and PPC to social media management and content marketing, our digital marketing specialists create data-driven strategies that generate measurable results. We don't just build campaigns — we build pipelines that convert.

  **Card 4 — Factoring Support Services**
  > Streamline Your Financial Operations. Our factoring support team assists freight brokers, staffing agencies, and financial companies with invoice processing, debtor management, and collections follow-ups. We help you maintain healthy cash flow without the administrative burden.

**Section 3 — Why Teams Switch to BPO Firm** *(text left, image right)*
- H2: Why Teams Switch to <span style="color:#ef494b">BPO</span> Firm
- Body: In-house operations roles cost $52,000–$78,000 fully loaded in the US, take 47 days to fill, and lose 24% of staff within 12 months. We replace that cycle with a managed team: vetted on day one, trained to your SOPs by day five, in production by day seven. You pay a flat per-seat monthly rate. We handle hiring, training, attrition, payroll, equipment and floor management. Serving SMEs and mid-market firms across the US, UK, AU and EU. GDPR and HIPAA-aligned workflows.
- CTA: **Book a Service** → `/services/`
- Image: `Partner-with-BPO-Firm.webp` (800×450), alt "Partner with BPO Firm"

**Section 4 — Global Market Integration**
- H2: <span style="color:#ef494b">Global</span> Market Integration
- World-map illustration `vecteezy_dotted-world-map_1198050.png` with one animated hotspot pinned over Pakistan (offset 67%/36%) — tooltip displays the Pakistan flag SVG

**Section 5 — CTA band** *(red/dark background, white text)*
- H2: **READY TO OUTSOURCE?** Book a 20-Minute Discovery Call Today
- CTA: **Book a Discovery Call** → `/contact-us/`

**Section 6 — FAQs** *(H2: FAQ's, with red apostrophe; two columns of 3 accordions each, "max 1 expanded" mode)*

Left column:
1. **What is Business Process Outsourcing (BPO) and how can it benefit my company?**
   Business Process Outsourcing (BPO) means delegating specific business operations – such as customer support, finance, HR, or data management – to a specialized third-party provider like BPO Firm. By outsourcing non-core functions, your business can significantly reduce operational costs, improve efficiency, access specialized expertise, and scale faster without the burden of in-house hiring and management.
2. **How quickly can BPO Firm deploy a team for my business?**
   We pride ourselves on speed without compromising quality. Once your requirements are confirmed and onboarding is complete, BPO Firm can have a fully trained, dedicated team operational within 7 business days. This rapid deployment model is designed to give businesses an immediate competitive advantage.
3. **Is my business data safe with BPO Firm?**
   Absolutely. Data security is at the heart of everything we do. BPO Firm operates in full compliance with GDPR and HIPAA regulations. We implement strict access controls, data encryption, and confidentiality protocols across all processes to ensure your sensitive business information and customer data remain completely secure.

Right column:
4. **What industries does BPO Firm serve?**
   BPO Firm serves a wide range of industries including healthcare, insurance, finance and accounting, e-commerce, logistics, real estate, and more. Our diverse team of specialists brings deep domain knowledge to every engagement, ensuring industry-specific accuracy and compliance.
5. **How does the Human-in-the-Loop model work?**
   Our Human-in-the-Loop architecture combines the speed and efficiency of AI automation with the judgment and expertise of trained human specialists. AI handles high-volume, repetitive tasks such as data extraction, classification, and routing — while our specialists manage complex decisions, quality checks, and exception handling. This hybrid model delivers 99.9% accuracy and superior outcomes compared to fully automated or purely manual processes.
6. **Can I scale my outsourced team up or down based on seasonal demand?**
   Yes, and this flexibility is one of BPO Firm's greatest strengths. Whether you're experiencing a seasonal surge or need to downsize temporarily, we offer fully flexible engagement models that let you adjust your team size with minimal lead time and no penalties.

**Visual / asset inventory used by the home page**
- Hero video: `…/uploads/2026/01/191684-891315375_small.mp4`
- "Partner with BPO Firm" hero/why image: `…/uploads/Partner-with-BPO-Firm.webp`
- World map: `…/uploads/2026/01/vecteezy_dotted-world-map_1198050-1024x491.png`
- Pakistan flag SVG: `…/uploads/Flag_of_Pakistan.svg.svg`
- Logo (header + footer): `…/uploads/cropped-3d-logo.png`

**Internal links emitted by this page**
- `/contact-us/` (hero CTA + bottom CTA band)
- `/services/` (twice — "Book a Service" buttons; **target URL not in current sitemap — verify**)
- All nav links (see §5)
- All footer links (see §6)

**Issues spotted (worth fixing in new theme)**
1. Footer LinkedIn link uses an admin URL — replace with public profile.
2. Footer "App Development" goes to `/app-development/` but the canonical URL is `/digital-marketing/app-development/`.
3. Hero "Book a Service" CTA points to `/services/` — this page wasn't supplied in the sitemap; either build it or change the CTA target.
4. Two near-duplicate JSON-LD blocks (Yoast + a custom one) — keep only one in the new build.

---

## 8. Items still to verify / capture from live site

- [ ] Pricing model (Pricing page content)
- [ ] Existing testimonials / client logos
- [ ] Awards / certifications (ISO, Clutch, GoodFirms?)
- [ ] Hi-res logo source files (SVG preferred)
- [ ] Brand color secondary / neutrals
- [ ] Whether the new theme must keep the Elementor stack or migrate to a different builder
- [ ] Newsletter provider — none visible on home; confirm if used elsewhere
- [ ] Live chat widget — none visible on home; confirm if used elsewhere
- [ ] WhatsApp click-to-chat number for floating button (since they offer WhatsApp support service)
- [ ] Existing blog post URLs under `/insights/blog/`
- [ ] Existing case study URLs under `/insights/case-study/`

---

## 9. Environment limitation

Direct outbound fetch of `bpofirm.com` (and `web.archive.org`, `google.com`) is blocked from this sandbox by the network policy (`x-deny-reason: host_not_allowed`). Page content is therefore being captured by paste (URL + body HTML / text / screenshot) from the site owner.
