# CitedRealty — Complete Handoff & Decision Log

**Site:** https://citedrealty.com · **Repo:** github.com/jonathandkennedy/citedrealty (public, `main`) · **Host:** Vercel (auto-deploys on push) · **Last updated:** 2026-07-23

This document records not just *what* the site is, but *why every non-obvious decision was made*, so anyone (including future-you or another dev/marketer) can extend it without re-litigating settled choices or breaking the strategy.

---

## 0. The one-paragraph summary

CitedRealty is a full digital-marketing agency for **realtors and real-estate brokers** whose wedge is **Generative Engine Optimization (GEO)** — getting agents *cited and recommended by AI assistants* (ChatGPT, Gemini, Perplexity, Google AI Overviews) rather than fighting Zillow/Redfin for classic SEO. Tagline: **"When buyers ask AI, you're the answer."** The site is a static HTML/CSS/JS build (no framework, no build step) plus two Vercel serverless functions for the interactive tools. It is deliberately a *proof of its own product*: it practices the GEO it sells (schema, TL;DR answers, neighborhood-style architecture, honest citable content), so that when someone asks an AI about real-estate marketing agencies, CitedRealty is what gets cited.

---

## 1. Positioning decisions (the strategic core — do not drift from these)

| Decision | Why |
|---|---|
| **Lead with AI citations (GEO), not classic SEO** | Zillow/Redfin/Realtor.com own portal SEO; an agent cannot win "homes for sale in [city]". The AI-answer layer names *individual agents* and nobody owns it yet. This is the entire reason the company exists. |
| **ICP = realtors & brokers needing seller AND buyer leads** | Modeled on lucrativelegal.com (which does this for lawyers). Every page speaks to agents, never to consumers/home-shoppers. |
| **Public pricing ($999 / $3,999 / $6,999)** | Luxury Presence and most competitors demo-gate pricing. Public pricing is (a) a trust wedge and (b) an AI-answer advantage — assistants can actually answer "how much does CitedRealty cost," competitors' can't. **Keep pricing public.** |
| **"You own everything" ownership angle** | The core differentiator vs. Luxury Presence's rented SaaS. Websites, content, profiles, citations are assets the client keeps if they leave. This is the emotional spine of the whole site (see the "Why CitedRealty" homepage section). |
| **Radical honesty as a citation strategy** | Every comparison/CRM/course post genuinely says when NOT to buy, names competitors fairly, and discloses our bias. This is not softness — fair, honest content is what AI systems cite and skeptical agents trust. It is a deliberate GEO tactic. Never write self-serving fluff. |
| **"Eat our own cooking"** | The site itself runs the full GEO playbook. This is both the product demo and the reason the blog exists. |

**Three pricing tiers (user-decided, do not change without the user):**
- **Local Presence — $999/mo:** GBP + local SEO + AI citations + blog + 5 neighborhoods. Website build available as add-on project.
- **Local Hero — $3,999/mo** *(flagged "Most Popular"):* everything + **custom website build included** + 15 neighborhoods + social guidance + AI visibility tracking.
- **Market Authority — $6,999/mo:** everything + 30 neighborhoods + full done-for-you social + weekly 1-hr consultation.
- The "30 neighborhoods" figure was the AI's read of the user's shorthand "last 3)"; **confirm with user** if ever revisited. Website-build inclusion (Local Hero+) was an explicit user decision.

---

## 2. Brand & design system

- **Name/logo:** CitedRealty with a superscript **[1]** citation marker — the brand's signature motif (appears in the logo `CitedRealty[1]`, service numbering, pricing tiers, section eyebrows). The `[1]` is *the* brand device; use it purposefully, never sprinkle it. Logo mark = an AI answer bubble containing a house + spark (the "answer bubble"), chosen from 4 concepts explored at project start (design exploration lives in `../citedrealty/`).
- **Palette:** dark ink `#0B0B14`, panel `#12121D`, hairline `#23233A`; **gradient accent** indigo→violet→lilac `#4F46E5 → #8B5CF6 → #C084FC` (the one hot accent — everything else stays quiet). Light-mode tokens: ground `#FAF9FC`, panel `#FFFFFF`, ink `#14142B`.
- **Type:** **Sora** (display/headings, 700-800 weight), **Inter** (body). **Instrument Serif italic** is used *only* for the gradient words inside `h1`/`h2` (`<span class="grad">`) — the editorial serif counterpoint that gives the site its "expensive" feel and fits the citation/editorial brand. Wrap any headline phrase in `.grad` to get the treatment automatically. Loaded via Google Fonts on every page.
- **Why the serif accent:** requested "6-figure website" feel. The bold-geometric-sans against italic-serif contrast is the signature of high-end editorial brands, and a serif literally suits a company named after citations. One CSS rule restyled the whole site because headlines already wrapped gradient phrases in `.grad`.
- **Light/dark mode:** **LIGHT is the default** for new visitors (user decision — "day mode"; agents browse in daylight offices, light reads as trust). Dark is the toggle (the brand's original look). Implemented as CSS-token overrides under `:root[data-theme="light"]` + `assets/theme.js` loaded **synchronously in `<head>`** so the saved choice (localStorage `cr-theme`) applies before first paint (no flash). Both themes get equal design care.
- **Material layer:** `--shadow-card` token (flat/none in dark, layered violet-tinted soft shadow in light) on all cards; button lift+glow on hover with an inset top highlight; brand-violet `::selection`; light nav goes glassy with a shadow on scroll. These make light mode feel premium rather than flat.
- **Motion:** floating pill nav blurs solid on scroll; scroll-reveal on sections; homepage marquee ticker. All respect `prefers-reduced-motion`.

---

## 3. Technical architecture & WHY

- **Static HTML/CSS/JS, no framework, no build step.** Reasons: (1) fastest possible pages = Core Web Vitals win, which is part of what we sell; (2) trivially portable/ownable — the client-ownership ethos applies to our own site; (3) anyone can edit it; (4) it's what we'd build for a client.
- **Three Python generators** produce the repetitive pages from data (edit the data list, run the script, commit):
  - `gen_services.py` → the 7 `services/*.html` pages (SERVICES list)
  - `gen_audiences.py` → the 4 `audiences/*.html` pages (AUDIENCES list)
  - `gen_blog.py` → `blog/index.html` + all 40 `blog/*.html` articles (POSTS list, newest first)
  - **Why generators:** consistent nav/footer/schema across dozens of pages; change a shared component once and regenerate. **The homepage `index.html` is hand-authored and self-contained** (inline CSS/JS) — it's the one page different enough to justify not templating.
- **Interior pages share** `assets/styles.css` + `assets/app.js`. Homepage inlines its own copy of the CSS/JS (intentional — keeps the homepage a single self-contained file).
- **Two Vercel serverless functions** in `api/` (auto-deployed by Vercel from the repo, no config):
  - `api/check.js` — the AI Visibility Checker. Calls Gemini **with Google Search grounding** to test whether an agent is named/recommended in their market.
  - `api/generate.js` — shared endpoint for the 4 AI content tools (review-reply, listing-description, social-hook, attention-anchor) via a `mode` param.
- **Model:** both functions call **`gemini-flash-latest`** (an alias). **CRITICAL LESSON:** we originally used `gemini-2.5-flash`, which Google **retired for new API users** mid-2026 → caused 502s. The `-latest` alias auto-tracks the current model so this can't recur. If you ever hardcode a version, expect it to get retired.
- **Gemini "thinking" gotcha:** newer Gemini models return reasoning as parts with `thought:true`. **Both endpoints filter these out** (`.filter(p => !p.thought)`) or the tools leak their own chain-of-thought into output. Keep that filter.
- **Checker "named" detection:** we ask the model for an explicit `VERDICT: FOUND / NOT_FOUND` token and regex that, because naive string-matching the agent's name gave false positives (the model repeats a name even while saying it was *not* found). Also strips `[n.n]` grounding markers from display text.
- **Env var:** `GEMINI_API_KEY` in Vercel → Settings → Environment Variables (must be checked for **Production**). If absent, every tool degrades gracefully to a friendly "warming up" 503 that routes to the human audit form — nothing looks broken. (Debugging note: it took several deploys for the var to take; the fix was confirming the exact name + Production scope.)
- **Guardrails on the functions:** per-IP rate limits (5/hr checker, 10/hr generator — per warm instance, MVP-grade), input sanitization (`clean()` strips `<>{}\`), token caps, CORS locked to `https://citedrealty.com`. Each call costs a fraction of a cent.

---

## 4. Lead capture (LIVE) — Formspree

- Both the homepage `#leadForm` **and every tool** POST to **Formspree** (`https://formspree.io/f/mykrpold`). Submissions are **emailed AND stored in the Formspree dashboard** (a browsable lead list).
- We switched from FormSubmit.co → Formspree because Formspree stores + emails (FormSubmit was email-only) and needs no activation dance. Honeypot field is `_gotcha`; there's a mailto fallback if the request fails.
- **Every tool run is a lead.** Subjects self-triage, e.g. `Checker lead: Jane Rivera (Scottsdale) — NOT NAMED — sales opportunity`. The "NOT NAMED" ones are the call list — agents who just learned AI ignores them. **This is disclosed** on each tool page and in the privacy policy (capturing silently would be a trust landmine for an honesty brand).
- **Watch the Formspree free-tier submission cap** (≈50/mo). With the contact form + every tool feeding one endpoint, a busy month could hit it — upgrade Formspree or split tools onto a second form if volume grows.

---

## 5. Cookie/pixel consent + theme + preferred-source (shared JS)

- `assets/consent.js` self-injects a themed banner on every page (Accept all / Essentials only; choice in localStorage `cr-consent`). **Marketing pixels load ONLY after "Accept all."** Pixel IDs are configured at the top of `consent.js` (`META_PIXEL_ID`, `GA4_ID`, `GTM_ID` — all empty until the user adds them; GA4 gets `anonymize_ip`). Footer "Cookie preferences" link reopens the choice.
- `assets/theme.js` — the light/dark switch (see §2), synchronous in `<head>`.
- Every footer has a **"★ Make us a preferred source on Google"** link → `google.com/preferences/source?q=citedrealty.com`. Lets logged-in Google users star the brand as a Preferred Source (weights our articles in their Top Stories — most relevant to the Industry News posts). User must be logged into Google for the page to work; that's Google's behavior, not a bug.

---

## 6. Page inventory (as of 2026-07-21)

- **Homepage** (`index.html`): nav → hero (tagline + mock AI answer citing an example agent with "This becomes you" pill) → marquee → "portal trap" problem → flywheel bento (Cited→Found→Known→Trusted→Chosen) → 7 services → rent-vs-own compare → 4 audiences → pricing → 5-step process → "Why CitedRealty" ownership promises → FAQ → contact form → footer + sticky mobile CTA.
- **7 service pages** (`services/`): ai-citations `[1]` (flagship), website-design `[2]`, google-business-profile `[3]`, local-seo `[4]`, content `[5]`, social-media `[6]`, reviews `[7]`. (Website Design was added after launch as service [2] — the Luxury Presence competitive response; everything renumbered.)
- **4 audience pages** (`audiences/`): solo-agents, teams, brokerages, listing-agents.
- **7 free tools** (`tools/`) + hub `tools/index.html`: ai-visibility-checker, review-reply-generator, listing-description-generator, marketing-budget-calculator (client-side), gbp-grader (client-side, 11 weighted questions), social-hook-generator, attention-anchor-generator.
- **40 blog posts** (`blog/`) across 9 categories (Industry News, How-To Guides, Agent Q&A, Websites, Seller Leads, Buyer Leads, AI Search, Local SEO, Strategy).
- **Landing page** (`method.html`): "The GEO Method" — a long-form direct-response conversion page for paid/direct traffic (modeled on a LandersRX-style "free offer" funnel: plain-English "what is GEO" explainer → reframe → 3-step method → free offer → qualification → urgency → timeline → close). **Opens by teaching the concept, not selling** — agents don't know GEO, so the page leads with a mock AI chat (a buyer asking AI for an agent, naming someone else, with a "This becomes you" pill), a one-sentence definition ("GEO = being the agent AI recommends = the new #1 on Google"), and a word-of-mouth → phone book → Google/Zillow → AI evolution strip. Jargon (schema, "citations") is translated to plain language throughout. Sells the existing **free AI Visibility Audit** as the hook → public plans as the upsell. `noindex, follow` and **excluded from sitemap.xml** (it overlaps the homepage; flip both if you ever want it organic). Self-contained but links the shared `styles.css`/`theme.js`/`consent.js` and POSTs to the same Formspree endpoint with a hidden `_source: method-landing-page` field so its leads self-triage. **Honesty rules honored:** no fabricated stats/logos/testimonials — the "proof" leans on the mechanism, the "eat our own cooking" argument, and the free audit itself. The month-to-month scarcity line ("limited spots each month") is a soft, editable offer term — confirm/adjust to a real number if you want.
- **Legal:** privacy.html, terms.html (both `noindex`, attorney-review templates).
- **SEO infra:** robots.txt, sitemap.xml (61 URLs — every indexable page; privacy/terms are noindex and excluded).

---

## 7. Content strategy & the rules behind it

**Why a blog at all:** it's the GEO engine. When an agent asks ChatGPT "how do I get seller leads," a CitedRealty article should be the cited source — proving the product by being the product.

**Every post follows a fixed anatomy** (enforced by `gen_blog.py`): question-first title, a **TL;DR block** (60-130 words, written to be liftable by an AI as a snippet), H2 sections, a sticky "On this page" TOC (auto-built from H2s), an **FAQ** section, a branded hero image, and **BlogPosting + FAQPage + BreadcrumbList schema**. This structure is *itself* the GEO tactic — it's what makes posts citable.

**Content rules (do not break — they are the brand):**
1. **Honest or don't publish.** Every comparison names competitors fairly and says when not to buy. The CRM post says "you don't need a CRM if your problem is lead-gen"; the courses post says "we'd rather be the resource you trust than sell you a course." This honesty is why the content earns citations.
2. **No fabricated stats, quotes, testimonials, or `aggregateRating`.** Real numbers only, each attributed to its primary source with an outbound link. The stats roundup was built from a deep-research pass that verified 24 of 120 claims and *published which ones failed* — that transparency section is a feature, not a bug.
3. **Contextual internal links** with descriptive anchor text from every post to relevant service/audience pages (mapped in `gen_blog.py`). New posts should include 1-2. This was a deliberate internal-linking-architecture fix (see §8).
4. **Compliance hedging** on legal/news posts: "reporting, not legal advice," no unverified penalty figures.
5. **Images:** generated via `gen_blog_images_gemini.sh` (Gemini `gemini-2.5-flash-image`, preferred) or `gen_blog_images.sh` (OpenAI, older). Prompts request the brand palette + a warm amber accent, "NO text/letters/watermarks" (Gemini occasionally sneaks in a hex-code watermark — regenerate if so). Downscale to 1200w JPEG with `sips` before committing.

**How the content was built (chronology, so you understand the clusters):**
- Core launch set (buyer/seller leads, AI visibility, neighborhood pages, local SEO).
- **Luxury Presence gap analysis** (`CONTENT-GAP-luxurypresence.md`) → website-design service + comparison posts (best-website-companies, LP-alternatives, website-cost, do-you-need-a-website) + the verified stats roundup.
- **Agent Q&A** batch (Reddit-perennial questions: door knocking, open houses, cold calling, postcards, first clients) — the forum-question format LP doesn't do.
- **Industry News** batch (newsjacking, links back to source): CT SB 340 private-listings ban, CA AB 723 AI-photo law, NAR coming-soon statement. This is a repeatable rhythm — send any industry article, it becomes a fact-checked source-linked post.
- **How-To Guides** batch (closing the Stridec/GEO-agency gap): GBP step-by-step, reviews playbook, what-data-AI-uses, schema walkthrough, E-E-A-T, neighborhood-page template, DIY audit, IDX.
- **TopicalMap.ai diff batch:** from a 1,120-keyword export we extracted only 6 on-ICP, non-duplicative posts (AI-tools-vs-cited, 3-3-3 rule, mistakes, ROI, best-CRM, courses) and ignored ~1,000 rows of padding + the off-ICP courses pillar.
- **Local-SEO map diff:** wrote only 2 genuinely-new comprehensive pages (GBP Posts, on-page SEO — which absorbed 5 micro-topics) and skipped ~18 thin <10/mo topics. **Lesson for future maps:** these keyword tools are worth ~2-6 real posts each after filtering for overlap and micro-volume; writing one-post-per-keyword is the doorway-page mistake our own content warns against. Filtering IS the value.

---

## 8. Internal-linking architecture (deliberate, audited)

An audit was run (money pages = 11: 7 services + 4 audiences). Decisions:
- **URLs left flat and unchanged.** URL depth/slashes are **not** a Google ranking factor (Google-confirmed). We never restructure healthy URLs or add 301s to fix a non-problem. The levers are click depth, navigation, and the link graph — those we fixed instead.
- **Server-rendered header dropdowns** (Services + Who-we-help) list all 11 money pages → every money page is 1 click from every page. Pure HTML/CSS, no JS injection (so crawlers see them).
- **30+ contextual body links** from blog posts to services/audiences with descriptive anchors.
- **Homepage ItemList schema** for services.
- Result: inbound links per money page went from 4-10 → 33.

---

## 9. How to do common tasks

- **Add a blog post:** append a dict to `POSTS` in `gen_blog.py` (newest first) with slug, img, img_alt, cat, title, date, excerpt, tldr, sections `[(h2, html)…]`, faqs `[(q,a)…]`. Include 1-2 contextual links to service/audience pages in the body (use **single-quoted** HTML attrs inside the double-quoted Python strings, e.g. `<a href='../services/x.html'>`). Add the image prompt to `gen_blog_images_gemini.sh`, run it, downscale, run `python3 gen_blog.py`, add to `sitemap.xml`, commit, push. **After the deploy is live, ping IndexNow** for the new URL (see below).
- **Ping IndexNow after publishing/changing pages:** `python3 submit_indexnow.py https://citedrealty.com/blog/your-new-post.html` (pass any changed URLs), or `python3 submit_indexnow.py` with no args to resubmit the whole `sitemap.xml`. Use `--dry-run` to preview. This pushes the pages to Bing/Yandex/etc. instantly — and Bing indexing is a prerequisite for ChatGPT's web-search citations (§10). **Run it only after the page is live** (the engines verify ownership by fetching the public key file `78f577…​.txt` at the site root). That key file is public *by design* — commit it; it is NOT a secret like the Gemini/OpenAI keys.
- **Edit a service/audience page:** edit the data list in the generator, run it.
- **Edit pricing/homepage:** hand-edit `index.html`. If pricing changes, also update the OfferCatalog in the homepage JSON-LD.
- **VALIDATE JSON-LD before every push.** A single missing brace in hand-authored schema made the entire homepage graph unparsable (Google Search Console flagged it within hours of launch). Generated pages can't have this bug; hand-edits can. Run `json.loads` on every `<script type="application/ld+json">` block. Also validate `sitemap.xml` XML (a stray `</locs>` typo was caught pre-push once).
- **Deploy:** `git push` → Vercel auto-deploys in ~30-60s. Committing straight to `main` (no PR flow, by default). Everything is verified with a live crawl after each push.

---

## 10. Pre-launch / open items (things only the user can do)

- [ ] **Rotate the API keys** — the OpenAI and Gemini keys were pasted in chat during the build; treat as exposed. New values go in `../citedrealty/.env` (local, gitignored) and the Vercel env var.
- [ ] **Google Search Console:** the homepage FAQ-schema bug is fixed; re-request indexing of `/`. Submit `sitemap.xml`. (There was a "Couldn't fetch" cosmetic delay on the brand-new property — normal.) An indexing priority list was provided (homepage + money pages + citation-bait posts first, ~10/day).
- [ ] **Bing Webmaster Tools** — imports from Search Console in 2 clicks. **Matters more than usual:** ChatGPT web search runs on Bing's index, so Bing indexing is a prerequisite for some of the AI citations we sell. **IndexNow is now wired up** (key file `78f577…​.txt` at root + `submit_indexnow.py`) so pages get pushed to Bing instantly on publish — but still claim the property in Bing Webmaster Tools for the reporting/coverage view (IndexNow submits; it doesn't report).
- [ ] **Attorney review** of privacy.html + terms.html before relying on them.
- [ ] **Pixel IDs** into `assets/consent.js` if/when running Meta/Google ads.
- [ ] **Real NAP** (phone/address) into the homepage `#business` schema `sameAs`/`telephone`/`address` once the Google Business Profile exists — must match GBP exactly.
- [ ] **`hello@citedrealty.com`** — used in copy; set it up (or swap to a real address).
- [ ] Consider making the repo **private** or stripping the strategy docs (`CONTENT-GAP-luxurypresence.md`, this file) — they're the competitive playbook and the repo is public. Vercel works identically with private repos.
- [ ] **Watch Formspree submission cap** (§4).

---

## 11. Roadmap / ideas parked (not built)

- **Content:** agent-website teardowns (recurring format), best-lead-gen-companies listicle, more Industry News as laws/news drop, email/scheduling/video *tools* comparisons (each needs a research pass for real vendor facts).
- **Product:** an **email newsletter** (the last unbuilt item from the Stridec gap — owned audience + nurture). Case-studies + design-portfolio + testimonials sections — **all gated on real clients; never fabricate.** Treat the first 2-3 clients as documented case studies from day one.
- **The real remaining gap is proof, not content or product.** The content and tool gaps vs. every competitor are closed; what can't be built is client results. That closes one client at a time.

---

## 12. Where things live outside this repo

- Design exploration (logo concepts, alternates, the OpenAI-generated concept board): `../citedrealty/`
- API keys (local, gitignored): `../citedrealty/.env`
- This project's running memory/decisions: the user's Claude memory (`project_citedrealty.md`).
- The TopicalMap.ai export analyzed: session scratchpad `topicalmap/`.
</content>
