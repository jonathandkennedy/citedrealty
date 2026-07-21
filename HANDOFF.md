# CitedRealty — Website Handoff

Last updated: 2026-07-19

A full marketing site for **CitedRealty** (citedrealty.com) — AI search marketing for
**realtors and real estate brokers** who need more seller and buyer leads. Static
HTML/CSS/JS, no build step; open the files in a browser or serve the folder.

Tagline: **"When buyers ask AI, you're the answer."**

---

## 1. What's in this package

```
citedrealty.com/
├── index.html                  # homepage (all styles + scripts inline)
├── HANDOFF.md                  # this file
├── assets/
│   ├── styles.css              # shared stylesheet for interior pages (services/audiences/blog)
│   ├── app.js                  # shared JS (nav blur, mobile menu, scroll reveal)
│   ├── icon-square.svg         # bubble-house mark on gradient tile (used in nav/footer)
│   ├── icon-512.png            # social/OG image + avatar source
│   ├── apple-touch-icon.png    # 180px
│   ├── favicon-32.png / favicon-16.png
│   └── citedrealty-lockup-dark.svg / -light.svg   # full logo lockups
├── services/                   # 6 pages, generated
│   ├── ai-citations.html       # flagship: GEO / AI citation building
│   ├── google-business-profile.html
│   ├── local-seo.html          # local SEO + neighborhood pages
│   ├── content.html            # blog & content engine
│   ├── social-media.html
│   └── reviews.html
├── audiences/                  # ICP landing pages, generated
│   ├── solo-agents.html  ├── teams.html
│   ├── brokerages.html   └── listing-agents.html
├── blog/                       # Resources & News (GEO content hub; see §8)
│   ├── index.html              # filterable card grid (category chips)
│   └── <slug>.html             # 6 articles (generated)
├── robots.txt                  # allows all crawlers, points at sitemap
├── sitemap.xml                 # all 18 URLs
├── gen_services.py             # service-page generator
├── gen_audiences.py            # audience-page generator
└── gen_blog.py                 # blog generator (index + articles)
```

> The **homepage** is fully self-contained (inline CSS/JS). Interior pages share
> `assets/styles.css` + `assets/app.js` — edit a component once, every page updates.

## 2. How to view / run

- Quickest: open `index.html` in a browser.
- Local server (recommended):
  ```
  cd citedrealty.com
  python3 -m http.server 4601
  # http://localhost:4601
  ```
  (A `citedrealty` entry exists in the repo's `.claude/launch.json` for Claude Code previews.)

Fonts (Sora + Inter) load from Google Fonts; offline they fall back to system fonts.

## 3. Design system

- **Palette:** ink `#0B0B14`, panel `#12121D`, hairline `#23233A`, text `#F0F0F8`,
  muted `#9494AE`, gradient accent indigo→violet→lilac `#4F46E5 → #8B5CF6 → #C084FC`.
- **Type:** Sora (display/headings), Inter (body).
- **Brand motif:** the `[1]` citation marker — in the logo (`CitedRealty[1]`), service
  numbering, pricing tiers, and pillar headings. Keep it purposeful, not sprinkled.
- **Logo:** bubble-house mark (AI answer bubble + house + spark). Source SVGs in
  `assets/` and the design exploration in `../citedrealty/` (concept board, alternates).
- **Motion:** nav blurs solid on scroll, scroll-reveal sections, marquee ticker on the
  homepage. All respect `prefers-reduced-motion`.
- **Light/dark mode:** LIGHT ("day mode") is the default for new visitors; a sun/moon
  toggle in every nav switches to dark (the brand's original look). Implemented as token
  overrides (`:root[data-theme="light"]` in `assets/styles.css` and the homepage's inline
  CSS) + `assets/theme.js` (loaded synchronously in `<head>` so the saved choice —
  localStorage `cr-theme` — applies before first paint). The consent banner themes
  automatically via CSS variables. If you add new colors, use the existing tokens.
- **Premium type accent:** gradient words inside `h1`/`h2` (`<span class="grad">`) render
  in *Instrument Serif italic* — the editorial counterpoint to Sora. Loaded from Google
  Fonts on every page. Wrap any headline phrase in `.grad` to get the treatment.
- **Material layer:** `--shadow-card` token (flat in dark, layered violet-tinted soft
  shadow in light) applied to all cards; button lift/glow hovers; `::selection` in brand
  violet; light nav goes glassy with shadow on scroll.

## 4. Homepage sections (top to bottom)

1. Floating pill nav (blurs on scroll) + mobile menu
2. Hero — tagline headline + mock AI answer citing an example agent ("This becomes you")
3. Marquee — services ticker
4. The portal trap — why classic SEO loses to Zillow, why AI answers are winnable
5. The CitedRealty system — bento flywheel (Cited → Found → Known → Trusted → Chosen)
6. Services — 6 cards linking to service pages
7. Rent vs. own compare
8. Who we help — 4 audience cards
9. Pricing — $999 Local Presence / $3,999 Local Hero (most popular, website build included) / $6,999 Market Authority
10. Process — 5 steps · 11. Why CitedRealty — the four promises (ownership manifesto)
12. FAQ accordion · 13. Contact/lead form · 14. Footer (Privacy/Terms/Cookie preferences) + sticky mobile CTA

## 5a. Cookie & pixel consent

`assets/consent.js` runs on every page (self-injecting banner + styles):
- First visit: banner offers **Accept all** / **Essentials only**; choice stored in
  localStorage (`cr-consent` = "all" | "essential").
- Marketing pixels load **only after Accept all** — configure IDs at the top of
  `consent.js` (`META_PIXEL_ID`, `GA4_ID`, `GTM_ID`; empty = never loads). GA4 is
  configured with `anonymize_ip`.
- Every footer has a "Cookie preferences" link (`data-cookie-prefs`) that clears the
  choice and reopens the banner; JS API: `window.crConsent.open()` / `.status()`.
- `privacy.html` and `terms.html` (noindex, linked in all footers) are starting
  templates — **have an attorney review before launch.**

## 5. The contact form (WIRED — one activation step left)

`#leadForm` posts via AJAX to **FormSubmit.co** (no account needed), delivering
submissions by email with a honeypot spam trap and a mailto fallback if the request
fails. Currently pointed at `jondkennedy.com@gmail.com`.

**Before launch:**
1. Submit the form once — FormSubmit emails a one-time activation link; click it.
   Submissions flow after that.
2. When `hello@citedrealty.com` exists, swap the address in the form `action`
   (`https://formsubmit.co/ajax/<email>`) and re-activate.
3. Optional: FormSubmit gives you a random alias string after activation — use it in
   the action URL instead of the raw email to keep the address out of the page source.

## 5b. Free tool: AI Visibility Checker (needs one env var)

`tools/ai-visibility-checker.html` + `api/check.js` (a Vercel serverless function).
Visitor enters name/brokerage/market → the function asks Gemini (with live Google
Search grounding) who AI recommends there and whether the visitor is named →
result shows the verdict, the agents named, and the sources cited, with audit CTAs.

**To activate:** Vercel dashboard → Project → Settings → Environment Variables →
add `GEMINI_API_KEY` (same key as the image scripts) → redeploy. Until then the
tool degrades gracefully ("warming up") and routes to the audit form.
Guardrails: 5 checks/IP/hour (per instance), input sanitization, 900-token cap,
CORS locked to citedrealty.com. Each check costs a fraction of a cent on the key.

## 6. Generators — how to edit pages

- **Service pages:** edit the `SERVICES` list in `gen_services.py`, run
  `python3 gen_services.py`. All six regenerate.
- **Audience pages:** edit `AUDIENCES` in `gen_audiences.py`, run it.
- **Blog:** append a post dict to `POSTS` in `gen_blog.py` (newest first), run it —
  rebuilds `blog/index.html` and every article. Write original answers only.
- **Homepage / pricing:** edit `index.html` directly (pricing cards in `.plans`; also
  update the offer catalog in the homepage JSON-LD if prices change).

## 7. Technical SEO / schema

- Homepage `@graph`: `ProfessionalService`+`Organization` (`#business`) with
  `hasOfferCatalog` (3 retainers), `areaServed`, `knowsAbout`; `WebSite`; `FAQPage`
  matching the on-page FAQ.
- Service pages: `Service` + `BreadcrumbList`. Audience pages: `WebPage` + `BreadcrumbList`.
- Articles: `BlogPosting` + `FAQPage` + `BreadcrumbList`; TL;DR answer block up top
  (60–130 words, liftable by AI), sticky "On this page" TOC, FAQ per post.
- Every page has `<link rel="canonical">`; robots.txt + sitemap.xml cover all URLs.
- No fabricated stats, testimonials, or `aggregateRating` — add real proof as it exists.
- Accessibility: skip links, keyboard-operable nav/menu/FAQ, focus styles,
  reduced-motion support.

## 8. Blog / content workflow (GEO)

Audience: **realtors and brokers asking marketing questions** (not consumers). Goal:
when an agent asks ChatGPT/Google "how do I get seller leads" or "how do agents show up
in ChatGPT", CitedRealty's article is the cited source — the site practices the GEO it
sells. Question-first titles, TL;DR answer up top, FAQs + schema on every post.
Current set: **10 posts** across Seller Leads / Buyer Leads / AI Search / Local SEO / Strategy,
including comparison ("vs"), budget, and ranked-list formats. Comparison posts avoid
hard-coded competitor pricing (it goes stale) — keep them structural and honest.

**Hero images:** every post has a branded illustration in `blog/img/` (1200w JPEG, wired
via each post's `img`/`img_alt` fields — feeds the article figure, card thumbnail,
og:image, and schema image). Two generator scripts:
- `gen_blog_images.sh` — OpenAI gpt-image-1 (used for the first 6 posts)
- `gen_blog_images_gemini.sh` — Gemini `gemini-2.5-flash-image` (used for the 4 newer posts; preferred going forward)
Both read keys from `../citedrealty/.env`; add a slug + prompt to the script, run it, then
downscale: `sips -Z 1200 -s format jpeg <slug>.png --out <slug>.jpg` and re-run `gen_blog.py`.

## 9. Pre-launch checklist

- [x] Lead form wired to FormSubmit (§5) — **activate it with one test submission.**
- [ ] Deploy: the site is fully static — drag the `citedrealty.com/` folder into
      Cloudflare Pages, Netlify, or Vercel (any free tier works), then point the
      citedrealty.com domain's DNS at it. No build step, no server.
- [ ] Confirm pricing and 30-neighborhood count on the Authority tier ("last 3)" was read as 30).
- [ ] Set real social profile URLs in `sameAs` (homepage schema) and footer if added.
- [ ] Add `telephone`/`address` to `#business` schema once the GBP/NAP is set — must match GBP exactly.
- [ ] Point the domain, then verify canonicals/sitemap URLs (already set to https://citedrealty.com).
- [ ] Submit sitemap in Google Search Console; run pages through the Rich Results Test.
- [ ] Have an attorney review privacy.html + terms.html (templates in place, linked in footers).
- [ ] Add real pixel IDs to assets/consent.js (Meta / GA4 or GTM) — they stay dormant until set.
- [ ] Replace the example agent in hero mock ("Jordan Blake") only if a real client agrees to be featured.
- [ ] Rotate the OpenAI key that was used during logo generation (../citedrealty/.env).
