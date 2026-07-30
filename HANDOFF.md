# CitedRealty — Complete Handoff & Decision Log

**Site:** https://citedrealty.com · **Repo:** github.com/jonathandkennedy/citedrealty (public, `main`) · **Host:** Vercel (auto-deploys on push) · **Last updated:** 2026-07-29

This document records not just *what* the site is, but *why every non-obvious decision was made*, so anyone (including future-you or another dev/marketer) can extend it without re-litigating settled choices or breaking the strategy. **§13 is the forward-looking Content Roadmap** — start there if your job is "what do we write next and why."

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

**Pricing (user-decided, do not change without the user):**
- **One-time projects (added 2026-07-29, PR #9):** a fixed-price lane for agents who want the asset without the retainer — `services/one-time-projects.html`, service `[8]`. Only the **$1,999 Website + Neighborhood Pages** build carries a public number (user-set); the other three projects (Neighborhood Page Pack, GBP Build, Schema & GEO Retrofit) are deliberately "quoted per project" because **we do not invent prices**. Positioned as a *starter* build — 5 neighborhoods, no IDX — so it does not cannibalize Local Hero's "custom website build included." Set the remaining prices by editing the `pricing` list in `gen_services.py` and re-running it.
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
  - `gen_services.py` → the 8 `services/*.html` pages (SERVICES list)
  - `gen_audiences.py` → the 4 `audiences/*.html` pages (AUDIENCES list)
  - `gen_blog.py` → `blog/index.html` + every `blog/*.html` article (POSTS list, newest first)
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

- Both the homepage `#leadForm` **and every tool** POST to **Formspree** (`https://formspree.io/f/mykrpold`). Submissions are **emailed AND stored in the Formspree dashboard** (a browsable lead list). The `method.html` landing page uses the same endpoint with a hidden `_source: method-landing-page` field, and the `strategy-session.html` broker page uses `_source: strategy-session`, so those leads self-triage.
- We switched from FormSubmit.co → Formspree because Formspree stores + emails (FormSubmit was email-only) and needs no activation dance. Honeypot field is `_gotcha`; there's a mailto fallback if the request fails.
- **Every tool run is a lead.** Subjects self-triage, e.g. `Checker lead: Jane Rivera (Scottsdale) — NOT NAMED — sales opportunity`. The "NOT NAMED" ones are the call list — agents who just learned AI ignores them. **This is disclosed** on each tool page and in the privacy policy (capturing silently would be a trust landmine for an honesty brand).
- **Watch the Formspree free-tier submission cap** (≈50/mo). With the contact form + every tool + the landing page feeding one endpoint, a busy month could hit it — upgrade Formspree or split tools onto a second form if volume grows.

---

## 5. Cookie/pixel consent + theme + preferred-source (shared JS)

- `assets/consent.js` self-injects a themed banner on every page (Accept all / Essentials only; choice in localStorage `cr-consent`). **Marketing pixels load ONLY after "Accept all."** Pixel IDs are configured at the top of `consent.js` (`META_PIXEL_ID`, `GA4_ID`, `GTM_ID` — all empty until the user adds them; GA4 gets `anonymize_ip`). Footer "Cookie preferences" link reopens the choice.
- `assets/theme.js` — the light/dark switch (see §2), synchronous in `<head>`.
- Every footer has a **"★ Make us a preferred source on Google"** link → `google.com/preferences/source?q=citedrealty.com`. Lets logged-in Google users star the brand as a Preferred Source (weights our articles in their Top Stories — most relevant to the Industry News posts). User must be logged into Google for the page to work; that's Google's behavior, not a bug.

---

## 6. Page inventory (as of 2026-07-29)

- **Homepage** (`index.html`): nav → hero (tagline + mock AI answer citing an example agent with "This becomes you" pill) → marquee → "portal trap" problem → flywheel bento (Cited→Found→Known→Trusted→Chosen) → 7 services → rent-vs-own compare → 4 audiences → pricing → 5-step process → "Why CitedRealty" ownership promises → FAQ → contact form → footer + sticky mobile CTA.
- **8 service pages** (`services/`): ai-citations `[1]` (flagship), website-design `[2]`, google-business-profile `[3]`, local-seo `[4]`, content `[5]`, social-media `[6]`, reviews `[7]`, one-time-projects `[8]`. (Website Design was added after launch as service [2] — the Luxury Presence competitive response; everything renumbered. One-Time Projects `[8]` was added 2026-07-29; `gen_services.py` gained an optional per-service `pricing` list — renders the project band **and** emits `Offer` schema — plus an optional `steps_h2` override.)
- **4 audience pages** (`audiences/`): solo-agents, teams, brokerages, listing-agents.
- **7 free tools** (`tools/`) + hub `tools/index.html`: ai-visibility-checker, review-reply-generator, listing-description-generator, marketing-budget-calculator (client-side), gbp-grader (client-side, 11 weighted questions), social-hook-generator, attention-anchor-generator.
- **69 blog posts** (`blog/`) across 9 categories (Industry News, How-To Guides, Agent Q&A, Websites, Seller Leads, Buyer Leads, AI Search, Local SEO, Strategy). See §7 for the cluster map. All recent additions carry **photo heroes** generated via `gen_blog_images_gemini.sh` (gemini-3.1-flash-image → Pillow-cropped 1200×800 JPG). The generator supports an optional per-post **`updated`** key → schema `dateModified` (keeps `datePublished` honest on a refresh).
- **Landing page** (`method.html`): "The GEO Method" — a long-form direct-response conversion page for paid/direct traffic (modeled on a LandersRX-style "free offer" funnel: plain-English "what is GEO" explainer → reframe → 3-step method → free offer → qualification → urgency → timeline → close). **Opens by teaching the concept, not selling** — agents don't know GEO, so the page leads with a mock AI chat (a buyer asking AI for an agent, naming someone else, with a "This becomes you" pill), a one-sentence definition ("GEO = being the agent AI recommends = the new #1 on Google"), and a word-of-mouth → phone book → Google/Zillow → AI evolution strip. Jargon (schema, "citations") is translated to plain language throughout. Sells the existing **free AI Visibility Audit** as the hook → public plans as the upsell. `noindex, follow` and **excluded from sitemap.xml** (it overlaps the homepage; flip both if you ever want it organic). Carries a **primary-sourced "by the numbers" block** (NAR 2024 Profile of Home Buyers & Sellers + ~800M weekly ChatGPT users + 1.5B+/mo Google AI Overviews) with **outbound links** to NAR, Wikipedia, and Search Engine Journal — every figure verified against its primary source. **Honesty rules honored:** no fabricated stats/logos/testimonials.
- **Broker landing page** (`strategy-session.html`, added 2026-07-29): "Free 1-hour online marketing strategy session" for **brokers, brokerage owners, and team leaders**. Unlike `method.html` it is **`index, follow` and IS in sitemap.xml** — it targets a distinct query set (broker/brokerage marketing consultation), so it can earn organic traffic and citations. Structure: hero → trust bar → why brokers book → **minute-by-minute agenda** (the differentiator: AI market research happens *before* the call) → what you keep → who should skip → the same primary-sourced NAR/ChatGPT/AI-Overviews numbers as `method.html` → booking form → FAQ. Carries **WebPage + Service (with a $0 `Offer`) + FAQPage + BreadcrumbList** schema — the better GEO template going forward. Booking is form-based (reply-to-schedule); a Calendly URL drops into the CTA/FAQ if self-serve booking is wanted.
- **Legal:** privacy.html, terms.html (both `noindex`, attorney-review templates).
- **SEO infra:** robots.txt, sitemap.xml (**92 URLs** — every indexable page; privacy/terms/method are noindex and excluded), IndexNow key file + submitter (see §10).

---

## 7. Content strategy & the rules behind it

**Why a blog at all:** it's the GEO engine. When an agent asks ChatGPT "how do I get seller leads," a CitedRealty article should be the cited source — proving the product by being the product.

**Every post follows a fixed anatomy** (enforced by `gen_blog.py`): question-first title, a **TL;DR block** (60-130 words, written to be liftable by an AI as a snippet), H2 sections, a sticky "On this page" TOC (auto-built from H2s), an **FAQ** section, a branded hero image, and **BlogPosting + FAQPage + BreadcrumbList schema**. This structure is *itself* the GEO tactic — it's what makes posts citable.

**Content rules (do not break — they are the brand):**
1. **Honest or don't publish.** Every comparison names competitors fairly and says when not to buy. This honesty is why the content earns citations.
2. **No fabricated stats, quotes, testimonials, or `aggregateRating`.** Real numbers only, each attributed to its primary source with an outbound link to a trusted source (NAR, Wikipedia, Search Engine Journal, government/legal primary sources). The stats roundup was built from a deep-research pass that verified 24 of 120 claims and *published which ones failed* — that transparency section is a feature, not a bug.
3. **Contextual internal links** with descriptive anchor text from every post to relevant service/audience pages (mapped in `gen_blog.py`). New posts should include 1-2. Deliberate internal-linking-architecture (see §8).
4. **Compliance hedging** on legal/news posts: "reporting, not legal advice," no unverified penalty figures.
5. **Images:** generated via `gen_blog_images_gemini.sh` (Gemini image model). Prompts request the brand palette + a warm amber accent and **"NO text/letters/watermarks"** — Gemini occasionally sneaks in a letter or hex-code watermark (it has happened twice: an "Open House"/"Market Updates" label and a magnet's "N"/"S" pole letters). **Regenerate if any text appears** — this is a hard brand rule. Output is Pillow-cropped to 3:2 and saved 1200×800 JPEG.

**The cluster map (hub-and-spoke — each post's H2s + FAQ = the fan-out sub-questions an AI generates):**
- **Core launch set:** buyer/seller leads, AI visibility, neighborhood pages, local SEO.
- **AI / GEO cluster:** `how-real-estate-agents-show-up-in-chatgpt` (deepened with a `sameAs` code example + team→Zillow-profile guidance), `ai-tools-for-real-estate-agents`, `ai-tools-vs-getting-cited-by-ai`, `what-data-do-ai-assistants-use`, `real-estate-ai-search-statistics`, `diy-ai-visibility-audit`, `realestateagent-schema-walkthrough`, `eeat-for-real-estate-agents` — plus the **GEO-skepticism trio published 2026-07-29 from the Reddit sweep** (`CONTENT-REDDIT-2026-07.md`): `is-geo-snake-oil` (featured on the blog index; concedes what r/SEO gets right, names which parts of our own service are "just SEO"), `how-to-hire-a-geo-agency` (the $4,200-thread buyer's checklist), `does-ai-search-send-traffic` (traffic-share objection engaged honestly; links the actual threads `rel='nofollow'`, paraphrase-not-quote). This is the brand's home-field cluster (KD mostly 0–30, nobody owns it), and the skepticism trio is its trust spine.
- **Websites cluster (hub + spokes):** `real-estate-agent-websites-guide` (pillar — build/buy/skip, the "pretty but AI-can't-read-it" trap) + spokes `real-estate-website-builders-for-agents` (KD ~12–14), best-website-companies, luxury-presence-alternatives, website-cost, do-you-need-a-website, what-is-idx.
- **Leads cluster (user priority, highest commercial intent):** `real-estate-lead-generation-guide` (pillar — bought-vs-owned, exclusive, best-way, follow-up; *real estate leads / lead generation* ~3,600/mo) + spokes `real-estate-lead-magnets` (the "10 things to do before you sell to maximize value" magnet — **holds the case study**), `exclusive-real-estate-leads` (exclusive-vs-shared, Zillow Flex / Realtor.com / pay-at-closing), `real-estate-niche-marketing` (the niche-down playbook generalizing the case study).
- **Winnable low-KD asset clusters:** `real-estate-postcards-guide` (postcards, KD 0–2, ~1,300/mo) + the older `do-real-estate-postcards-work` (deepened), and `free-real-estate-marketing-templates` (KD 0–2; includes a 100+ social-post-ideas list as the shareable/linkable asset).
- **Agent Q&A** (Reddit-perennial): door knocking, open houses, cold calling, postcards, first clients, `best-real-estate-lead-sources-reddit`, `new-real-estate-agent-playbook` (90-day hub).
- **Industry News** (newsjacking + source links): CT SB 340 private-listings ban, CA AB 723 AI-photo law, NAR coming-soon statement. Repeatable rhythm — any industry article becomes a fact-checked, source-linked post.
- **How-To Guides:** GBP step-by-step, reviews playbook, schema walkthrough, neighborhood-page template, on-page SEO, GBP posts.
- **Strategy / comparisons:** ROI, best-CRM, 3-3-3 rule, mistakes, courses, marketing spend, Zillow Premier vs local SEO, portal-lead comparisons.

**⭐ First real case study (proof — the historical §11 gap):** the `real-estate-lead-magnets` post publishes the user's **real, confirmed** result — a **1-story-homes-for-downsizers** lead campaign (older buyers want single-story living; stairs are hard on knees) that took **an agent from 5–10 leads/month to 35+**. Published honestly and anonymized ("an agent we worked with"), per the user's explicit go-ahead. This is the first proof point; treat future real client wins the same way (documented, specific, anonymized unless permission to name). **Do NOT invent additional numbers** — this one is real because the user confirmed it.

**⭐ Proof asset #2 (2026-07-29, anonymized):** a specialty insurance business in the founder's network got the **first online lead in company history** from a ChatGPT recommendation — the AI named the firm over a larger generalist **because of its dedicated specialization**, and the lead arrived as a phone call (zero recorded AI referral traffic). Used anonymized ("a specialty insurance business we know") in `is-geo-snake-oil` and `does-ai-search-send-traffic`. **Naming the firm, quoting the owner's message, or publishing the screenshot requires the owner's written permission** — with it, this graduates to a named mini-case-study on `strategy-session.html`/`method.html`; without it, it stays out of site pages. Full usage rules in `CONTENT-REDDIT-2026-07.md`.

**Filtering IS the value (keyword-map lesson):** keyword-tool exports (TopicalMap.ai's 1,120 rows, the local-SEO map) are worth ~2–6 real posts each *after* filtering for overlap and micro-volume. Writing one-post-per-keyword is the doorway-page mistake our own content warns against. Extract only on-ICP, non-duplicative, genuinely-searched topics.

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

- **Add a blog post:** append a dict to `POSTS` in `gen_blog.py` (newest first) with `slug, img, img_alt, cat, title, date, [updated], excerpt, tldr, sections [(h2, html)…], faqs [(q,a)…]`. Include 1-2 contextual links to service/audience pages in the body (use **single-quoted** HTML attrs inside the double-quoted Python strings, e.g. `<a href='../services/x.html'>`; `\"` for literal quotes; `&amp;` for `&`; code blocks use `&lt;`/`&quot;` entities). Add the image prompt to `gen_blog_images_gemini.sh` and generate the hero (the scratchpad `gen_heroes_api.py` is the API-key-in-env variant used this session), verify no text snuck in, run `python3 gen_blog.py`, add to `sitemap.xml`, commit, push. **After the deploy is live, ping IndexNow** for the new URL.
- **Ping IndexNow after publishing/changing pages:** `python3 submit_indexnow.py https://citedrealty.com/blog/your-new-post.html` (pass any changed URLs), or `python3 submit_indexnow.py` with no args to resubmit the whole `sitemap.xml`. `--dry-run` previews. This pushes pages to Bing/Yandex/etc. instantly — and Bing indexing is a prerequisite for ChatGPT's web-search citations (§10). **Run it only after the page is live** (engines verify ownership by fetching the public key file at the site root). That key file (`78f577af8eab42e2a0aa8001fe3ffc5d.txt`) is public *by design* — commit it; it is NOT a secret like the Gemini key.
- **Edit a service/audience page:** edit the data list in the generator, run it.
- **Edit pricing/homepage:** hand-edit `index.html`. If pricing changes, also update the OfferCatalog in the homepage JSON-LD.
- **VALIDATE JSON-LD before every push.** A single missing brace in hand-authored schema made the entire homepage graph unparsable (Search Console flagged it within hours). Run `json.loads` on every `<script type="application/ld+json">` block. Also validate `sitemap.xml` XML.
- **Deploy:** `git push` → Vercel auto-deploys in ~30-60s. Everything is verified with a live crawl after each push.

---

## 10. Search-indexing & distribution status (LIVE + open items)

**LIVE now:**
- **IndexNow is wired up and working.** Public key file `78f577af8eab42e2a0aa8001fe3ffc5d.txt` at the site root + `submit_indexnow.py` (stdlib-only; HOST `citedrealty.com`, endpoint `https://api.indexnow.org/indexnow`; same-host guard; treats HTTP 200/202 as success). Last run (2026-07-29) submitted the 8 new/updated leads-cluster URLs → **HTTP 200 OK**. Re-ping after every publish/refresh.

**Open items (only the user can do these):**
- [ ] **Rotate the exposed Gemini API key.** The Gemini key was pasted in chat during this session — **treat as exposed and rotate it.** It was only ever passed inline as an env var to the hero-generation script; it is **not** committed anywhere, and it must never be. New value goes in `../citedrealty/.env` (local, gitignored) + the Vercel `GEMINI_API_KEY` env var (Production scope). The older OpenAI/Gemini keys from the original build are also exposed — rotate those too.
- [ ] **Google Search Console:** re-request indexing of `/` (the FAQ-schema bug is long fixed); confirm `sitemap.xml` is submitted and read the Coverage report to see what's actually indexed vs. discovered. This is the single most important dashboard for a new domain — **"is it indexed?" is a different question from "is it ranking?"**
- [ ] **Bing Webmaster Tools** — imports from Search Console in 2 clicks. Matters more than usual: ChatGPT web search runs on Bing's index, so Bing indexing is a prerequisite for some AI citations we sell. IndexNow submits pages but does NOT report coverage — claim the property for the reporting view.
- [ ] **Backlink / digital-PR plan** — the #1 growth lever right now (see §13.4). Zero backlinks is the ceiling on everything else.
- [ ] **OpenSEO reconnect check** — when the OpenSEO MCP connector is reconnected, run the SERP / AI-Overview citation check for the target keywords and re-pull `get_domain_overview` to watch ranked-keyword count and backlink count climb. **Use the `citedrealty` project (id `f80dafe6-3855-48c9-88b1-1d9fb26060da`), NOT "Default"** (which now maps to retainerreach.com). `whoami`/`list_projects` are free; research tools cost credits (ask before >2,000-credit batches).
- [ ] **Attorney review** of privacy.html + terms.html before relying on them.
- [ ] **Pixel IDs** into `assets/consent.js` if/when running Meta/Google ads.
- [ ] **Real NAP** (phone/address) into the homepage `#business` schema once the Google Business Profile exists — must match GBP exactly.
- [ ] **`hello@citedrealty.com`** — used in copy; set it up (or swap to a real address).
- [ ] Consider making the repo **private** or stripping the strategy docs (`CONTENT-GAP-luxurypresence.md`, this file) — they're the competitive playbook and the repo is public. Vercel works identically with private repos.
- [ ] **Watch Formspree submission cap** (§4).

---

## 11. Tooling & connectors (reference)

- **OpenSEO MCP connector** (hosted, DataForSEO-backed keyword/SERP data). Tools used: `whoami`, `list_projects` (free), `research_keywords`, `get_ranked_keywords`, `get_domain_overview` (credit-costing). **Correct project = `citedrealty` (id `f80dafe6-3855-48c9-88b1-1d9fb26060da`).** Gotchas seen: (1) the connector disconnects intermittently — re-enable in the connector settings; a sandboxed headless browser **cannot** reach `app.openseo.so` (it's isolated from the user's logged-in browser), so drive research through the MCP tools, not the web UI; (2) `research_keywords` output can exceed the token limit — save to a file and parse with Python/jq to extract the winnable rows; (3) always confirm the active project before pulling (early research accidentally ran under "Default" = retainerreach.com).
- **Gemini image generation:** `gemini-3.1-flash-image` (fallback `gemini-2.5-flash-image`) via the REST API. `gen_blog_images_gemini.sh` holds the prompt map (`.env`-sourced key, macOS/`sips` path); the session scratchpad `gen_heroes_api.py` is the portable variant (reads `GEMINI_API_KEY` from env, Pillow crop, never writes the key to disk). Brand rule: **no text/letters/watermarks** — regenerate if any appear.
- **IndexNow:** `submit_indexnow.py` (see §10).
- **Link validator:** when writing a link checker, **strip `#fragment` before testing file existence** (a false-positive flagged `../index.html#services` as broken).

---

## 12. Where things live outside this repo

- Design exploration (logo concepts, alternates, concept board): `../citedrealty/`
- API keys (local, gitignored): `../citedrealty/.env`
- This project's running memory/decisions: the user's Claude memory (`project_citedrealty.md`).
- Keyword-map exports analyzed: session scratchpad (`topicalmap/`, OpenSEO pulls).

---

## 13. CONTENT ROADMAP (forward-looking — read this before writing anything new)

### 13.1 The SEO reality (diagnosis — do not skip)

An OpenSEO pull on the correct `citedrealty` project confirmed the hard truth: as of late July 2026 the domain is **~5–6 weeks old** with **1 ranked keyword, ~0 organic traffic, and 0 backlinks.** There are already **51 genuinely good posts.**

**This is NOT a content-volume problem.** It is three things, in order of impact:
1. **Domain age.** A brand-new domain sits in a trust "sandbox"; rankings lag published content by **months**, not days. Nothing writes its way out of this faster — it is a clock.
2. **Zero authority (0 backlinks).** With no inbound links, even perfect pages have no ranking power. **This is the real ceiling** and the highest-leverage thing to fix.
3. **Targeting terms too competitive for the site's age.** Head terms ("real estate marketing," "real estate leads") are unwinnable for a young, link-less domain regardless of content quality.

**The trap to avoid:** publishing more mid-KD posts feels productive but moves nothing while (1) and (2) are unaddressed. The 51 posts are plenty of *substrate* — the job now is winnability, links, and confirmed indexing.

### 13.2 The strategy (four pillars, run in parallel)

1. **Winnable low-KD long-tail (KD 0–15).** Every new post targets a term a young domain can actually rank for within months. Head terms are off-limits until authority arrives. This is where new *posts* go.
2. **Link-worthy free assets.** Free tools, template packs, data/stats roundups, and calculators earn links *and* rank for zero-KD "free …" queries. These do double duty against pillars 1 and 2. Prefer asset-posts over pure opinion-posts from here forward.
3. **Backlinks / digital PR / distribution (the ceiling — §13.4).** The single highest-leverage work. Without this, pillars 1–2 stay capped.
4. **Confirmed indexing.** IndexNow is live; the remaining gap is confirming Google/Bing have *indexed* (not just discovered) the pages — a GSC/Bing Webmaster job (§10). Ranking is impossible before indexing.

**Golden rule:** for a new domain, prioritize **winnable long-tail + links + confirmed indexing** over volume. Re-pull OpenSEO every few weeks to watch ranked-keyword count and backlinks climb — that's the real scoreboard, not post count.

### 13.3 Clusters already built (coverage map)

Strong / near-complete: **AI-GEO** (home-field, deep — now incl. the GEO-skepticism trust trio), **Prospecting & seller-appointment** (expired playbook, scripts library, listing presentation + CMA — added 2026-07-30), **Brand** (branding, slogans, bio — added 2026-07-30), **Sphere** (closing gifts, newsletters — added 2026-07-30), **Websites** (hub + 6 spokes), **Leads** (hub + 3 spokes + the case study), **Postcards** (guide + deepened Q&A), **Free-templates/tools**, **Agent Q&A**, **Industry News**, **How-To Guides**, **Strategy/comparisons**.

Thin / underbuilt (the roadmap targets these): **Buyer-leads**, **"getting clients / getting started"**, **niche-campaign spokes**, and **proof/case-studies** (blocked on real client results, not writing). (Seller-lead follow-ons largely closed 2026-07-30 by the expired/scripts/listing-presentation batch.)

### 13.4 Backlink & distribution plan (the ceiling — do this first / alongside)

Content without links is capped. Concrete, honesty-safe tactics, roughly in priority order:
1. **Turn existing assets into link bait.** The verified stats roundup (`real-estate-ai-search-statistics`), the 100+ social-post-ideas list, the free tools, and the "10 things before you sell" magnet are all inherently linkable. Pitch them where realtors and real-estate writers gather.
2. **Digital PR / expert quotes.** Respond to journalist requests (HARO/Qwoted/Connectively) on real-estate-marketing, AI-search, and GEO topics — the founder's honest, specific POV earns byline links from real publications. This is the fastest legitimate way to earn early authority.
3. **Community participation (not spam).** Genuinely answer questions on r/realtors, r/realestate, agent Facebook groups, and industry forums; link the relevant deep guide only when it truly answers the question. (This also feeds the Reddit-citation cluster, since Reddit is heavily cited in AI answers.)
4. **NAP / directory citations.** Once the GBP + real NAP exist, get consistent listings (Google Business Profile, Bing Places, industry directories). These are foundational local-SEO links and low effort.
5. **Guest posts / partnerships.** Real-estate coaching sites, CRM/tool vendors, brokerage blogs — offer genuinely useful, non-promotional articles with one contextual link.
6. **Free-tool embeds.** Offer the calculators/generators as embeddable widgets other sites can host (each embed = a link).
> Track backlink growth in OpenSEO's `get_domain_overview` — going from 0 → any real referring domains is the leading indicator that the whole strategy is working.

### 13.5 Prioritized next content (target keyword + KD + why)

Write in this order. All are winnable long-tail for a young domain; each slots into an existing hub for internal-link power. **Confirm live KD/volume in OpenSEO (`citedrealty` project) before committing a batch — the KDs below are the working estimates from prior pulls.**

**Priority 0 — the remaining Reddit-sweep posts (`CONTENT-REDDIT-2026-07.md`):** Tier 1 (the GEO-skepticism trio) shipped 2026-07-29; next up per the plan's publishing order is **"Your clients are already asking ChatGPT about your advice"** (Tier 2, the 222-pt r/realtors thread), then the GBP-reality post (Tier 3) and the sphere post (Tier 4). These are timely — the threads age — so slot them alongside the evergreen priorities below.

**✅ Verified pull 2026-07-30 (live OpenSEO, `citedrealty` project — ~9 new winnable clusters, all numbers are real vol/mo + KD). STATUS: ALL 11 POSTS WRITTEN & PUBLISHED 2026-07-30** — `expired-listings-guide`, `real-estate-scripts`, `real-estate-listing-presentation` (CMA folded in as a section), `closing-gifts-for-realtors`, `real-estate-farming`, `real-estate-branding`, `real-estate-slogans` (75 original examples), `real-estate-agent-bio` (3 example bios), `real-estate-newsletters`, `open-house-ideas-for-realtors`, `real-estate-video-marketing`. Both zero-post refreshes shipped too (templates post now 100+ ideas with `updated` key; local-seo post gained a keywords section + FAQ). Cluster details preserved below for context:

*New clusters found (rough value order; every keyword listed verified KD ≤ 15):*
1. **Closing gifts** — `closing gifts for realtors` **720 KD0** + `closing gifts from realtors` **720 KD0**. Biggest vol-to-KD find of the pull. Angle: closing gifts as sphere/referral *marketing* (ties to the NAR 40%-referral data), honest budget tiers, "reporting not tax advice" hedge on deductibility. List format = linkable.
2. **Expired listings playbook** — `expired listing scripts` 210 KD0, `script for expired listings` 210 KD0, `expired listings zillow` 210 KD0, `mls expired listings` 170 KD0, `how to find expired listings` 110 KD0, `expired listing letter(s)` 90+90 KD0, `expired listing postcards` 70 KD0 (feeds postcards hub), `calling expired listings` 30 KD0. One comprehensive hub (find → call → letter → postcard + honest "are expireds worth it in low inventory"). ~1,300/mo addressable, top seller-lead intent. (Mike Ferry script queries exist at 210 KD0 — reference his system honestly, never republish his scripts.)
3. **Scripts library (free asset, pillar-2 play)** — `real estate cold calling scripts` 320 KD0, `real estate scripts` 210 KD0, `circle prospecting` 210 KD0 (CPC $54!), `circle prospecting scripts` 70 KD0, `fsbo scripts` 90 KD0. ~1,000/mo all KD0; interlinks is-cold-calling-dead, door-knocking, and the expired hub.
4. **Listing presentation guide + free template** — `listing presentation` 390 KD1, `listing presentation template` 260 KD2, `real estate listing presentation` 260 KD0, template/example variants 170+140+90 KD≤4, `listing appointment checklist` 40 KD10. ~1,400/mo addressable; the free template is the linkable asset; routes to `audiences/listing-agents.html`. Spoke: `how to do a cma` 210 KD10.
5. **Branding & slogans** — `real estate branding` **590 KD0**, `real estate slogans` **480 KD0** (+ bio cluster below). Two posts: honest branding guide (entity/consistency = the GEO angle) + slogans list-asset.
6. **Agent bio (+ parked free-tool idea)** — `real estate agent bio` 390 KD0, `bio examples` 260+260 KD≤1, `bio template` 70 KD0, `short new agent bio samples` 70 KD0. ~1,080/mo; the E-E-A-T/entity angle (your bio is machine-read); pairs with the parked bio-generator tool (double-duty).
7. **Geographic farming** — `real estate farming` 260 KD2, `geographic farming real estate` 110 KD0, `real estate farming ideas` 40 KD0 (+ P4's `real-estate-farming-postcards`). Strategic gift: farming IS the neighborhood-domination thesis — the post routes straight to neighborhood pages. (Ignore "farmers national company" rows — that's a land company, navigational noise.)
8. **Newsletter guide** — `real estate newsletters` 260 KD2, `newsletter templates` 210 KD0, `luxury real estate newsletter` 210 KD8, examples/best/monthly/email 110+70+50+50 KD≤7. ~1,000/mo; spoke off the email-marketing post; supports the parked newsletter product.
9. **Open house ideas (realtor-specific)** — `open house ideas` 590 KD0 (mixed intent — most related volume is preschool/graduation noise, filter hard), `open house ideas for realtors` 320 KD9, `open house signs` **6,600 KD0** (commercial — capture with a "signs that work" section, not a standalone), materials/goodie-bags/themes 70+40+30 KD0. How-to companion to the existing are-open-houses-worth-it verdict post.
10. **Video/YouTube spoke** — `real estate video marketing` 260 KD3, `youtube for real estate agents` 90 KD2. Expands the YouTube section of the social-platforms post into a spoke.

*Zero-post refresh wins (✅ done 2026-07-30):* `100 real estate posts for social media` 110 KD0 → expand the free-templates post's 40+ list to 100+ and target the phrase (use the `updated` key). `real estate seo keywords` 70 KD0 → add a section/FAQ to `local-seo-for-real-estate-agents-2026` on a refresh.

**✅ Verified pull #2, 2026-07-30 (broker/team, niches, lead-company reviews, referral economy — 6 seeds + 30 exact hydrations, all real vol/mo + KD). NOT YET WRITTEN — next batch, in this order:**
1. **Referral fees hub** — `real estate referral fee` + `referral fee real estate` **720+720 KD0**, `finders fee real estate` + `real estate finders fee` 480+480 KD≤4, `how much is a referral fee` 210 KD13, `can i pay a referral fee to a non realtor` 140 KD0 (the RESPA question — compliance hedge mandatory), typical/what-is/agreement/how-do-they-work/who-pays/calculator 90+90+50+30+30+30 KD0. **~2,600/mo addressable, one comprehensive hub.** Bonus tool idea: a referral-fee / net-commission calculator (see #5).
2. **Zillow Flex honest explainer** — `zillow flex` **1,900 KD5**, `zillow flex program` 480 KD0, `flex pricing` 320 KD0, `zillow leads cost` 320 KD7, `premier agent cost` 320 KD5, `flex leads` 260 KD0, invited/requirements/reviews/join/become 50+40+40+40+50 KD≤13. ~3,400/mo addressable; extends the existing Zillow posts into the P5 lane. (The `zillow lawsuit` family — 320+210+210+40, KD≤6 — is a separate Industry News candidate **requiring a fact-checking research pass first**, per the news rules.)
3. **Luxury spoke** — `luxury real estate branding` **880 KD0**, `how to become a luxury real estate agent` 210 KD0, salary/make 170+140 KD0 (career-adjacent, fold as FAQs), `luxury home certification` 90 KD14. ~1,500/mo. Also a **zero-post refresh win:** `luxury presence reviews` **480 KD0** (+ pricing 40, reddit 40, examples 30) — add a reviews-focused section/FAQ to `luxury-presence-alternatives` on a refresh.
4. **Teams & recruiting (the broker-funnel content — feeds strategy-session):** post A \"real estate teams: how they work, structure, splits\" — how-do-teams-work 110, team structure 70, splits 50+40+30, build/start 40+40, agreement template 40, all KD≤3; post B \"how to recruit real estate agents\" — `real estate recruiting` 170 KD0, `agent recruiter` 170 KD3, how-to 40 KD3, software 40+40. Plus `real estate isa` **390 KD0 CPC $37** as post C or a section. ~1,400/mo combined.
5. **Free-tool idea (pillar-2 double-duty): commission/referral split calculator** — `real estate commission calculator` **6,600 KD0**, with-broker-split 70, split calculator 40, commercial 40. Consumer-heavy head term, but an agent-framed net-commission calculator (split, cap, referral fee out) is a legitimate agent asset that can own it. The adjacent \"how much do agents make\" career queries (5,400 KD0) stay **off-ICP — skip** per the standing TopicalMap decision.
6. **Names spoke** — `unique real estate name ideas` 210 KD0, `real estate name generator` 140 KD0 (another tool idea), `real estate team names` 110+30 KD0, catchy 70 KD0, name+logo 30 KD0. ~600/mo; links the just-published branding/slogans pair.
7. **Niche spokes verified (P3):** `new construction real estate agent` **1,600 KD9** (the biggest niche), `divorce real estate agent` 170 KD0, `veteran real estate agent` 170 KD0, `probate leads for realtors`/`probate real estate leads` 140+140 KD6 (+ `all the leads reviews` 40 — vendor review angle; the 720-vol head `probate real estate` is KD32, skip the head). Relocation/downsizer exact phrases are ≤30/mo — fold, don't write standalone.
8. **Buyer-agency-agreement post (post-settlement Q&A):** `buyers agreement form` 170 KD12, `refusing to sign buyer agency agreement` 170 KD3, `do i have to sign` 70 KD3, `buyer agent commission agreement` 30 KD11 — agent-facing frame (\"handling the agreement conversation\"), compliance-hedged. ~440/mo.
9. **Small refresh wins:** closing-gifts post → add 2 FAQs (`do realtors give closing gifts to buyers` 90 KD0, `can realtors accept gifts from clients` 50 KD0); websites cluster → target `real estate agent website examples` 210 KD3 with an examples section/FAQ on a refresh; open-house post → a free `open house sign in sheet template` asset (390 KD0, from pull #1's metrics) is the highest-value template still unbuilt.
10. **Skips, with reasons:** `pay at closing real estate leads` **880 KD0 CPC $41** goes IN post 2's lane or its own P5 review (queued — needs a vendor-facts research pass); `best real estate lead generation companies` 210 **KD31** — hold until authority grows; `va loan realtor` 260 **KD33** navigational — skip; `probate real estate` 720 **KD32** head — skip; career-pillar queries (agent income) — off-ICP; noise rows (\"teamos\" = Windows software, \"first team real estate\" = a brokerage, Amazon/lawyer referral-fee rows, Zillow login/dashboard navigationals) — ignore.

*Live corrections to the estimates below:* P1 pillar `how to get real estate clients` confirmed **390 KD0** ✅; `how to get more listings` 50 KD3 ✅ but `how to get listings as a new agent` is only **10/mo** — fold it into the listings spoke, don't write it standalone; P2 pillar `buyer leads for real estate agents` confirmed 110 KD5 / `how to generate buyer leads in real estate` 70 KD14 ✅, but `marketing to first time home buyers` is only **10/mo** — re-phrase or demote; `real estate prospecting ideas` 30 KD0 and `how to get real estate referrals` 30 KD4 are real but modest.

**Priority 1 — "getting clients / getting started" cluster (thin, high-intent, very winnable, KD ~0–9):**
- `how-to-get-real-estate-clients` — *how to get real estate clients* (KD ~0–9). Pillar for the whole "getting started" gap; links the Agent Q&A spokes + the leads hub.
- `how-to-get-listings-as-a-new-agent` — *how to get listings / get more listings* (long-tail, KD low). Seller-side companion.
- `real-estate-prospecting-ideas` — *real estate prospecting ideas* (list-style, linkable, KD low). Routes to postcards + templates + Q&A.
- `how-to-get-real-estate-referrals` — *real estate referral* long-tail; ties to NAR's 40%-referral data already cited on `method.html` and the new-agent playbook.

**Priority 2 — Buyer-leads cluster (currently just 2 posts; mirror the seller/leads depth):**
- `how-to-generate-buyer-leads` — *buyer leads for real estate agents* (KD low-mid). Buyer-side pillar; complements the existing `how-to-get-buyer-leads-without-portals`.
- `first-time-home-buyer-marketing` — *marketing to first-time home buyers* (niche, low-KD). Doubles as a niche-campaign spoke (see P3).
- `real-estate-buyer-lead-magnets` — buyer-side companion to `real-estate-lead-magnets` (e.g. "first-time buyer's closing-cost checklist").

**Priority 3 — Niche-campaign spokes (generalize the case study; each niche = one low-KD, high-conversion post that also demonstrates the product):**
- `marketing-to-downsizers` / expand the 1-story-homes angle — the exact niche behind the real case study; strongest proof-to-content fit.
- `luxury-real-estate-marketing`, `marketing-to-relocation-buyers`, `divorce-real-estate-marketing`, `probate-real-estate-leads`, `veteran-va-buyer-marketing`, `new-construction-buyer-marketing`, `investor-lead-generation`. Each is a low-KD long-tail, and the set collectively owns "real estate niche marketing" (our existing hub).

**Priority 4 — Deepen winnable asset clusters (links + zero-KD "free …" traffic):**
- Postcards spokes: `real-estate-postcard-ideas`, `just-listed-just-sold-postcards`, `real-estate-farming-postcards` (all KD 0–3, feed the postcards hub).
- Templates spokes: `real-estate-flyer-templates`, `real-estate-social-media-post-templates`, `open-house-sign-in-sheet-template`, `real-estate-email-templates` (all "free … template," KD 0–2, each a shareable/linkable asset).
- **New free tool** as a linkable asset (double-duty pillar-2 play): e.g. a "real estate bio / About-page generator," a "listing hashtag generator," or a "farm-area ROI calculator." Tools earn links AND rank for "free …" queries — favor these over another opinion post.

**Priority 5 — Exclusive-leads & seller follow-ons (extend the leads hub):**
- `zillow-flex-review`, `realtor-com-leads-review`, `pay-at-closing-leads` — honest, named comparisons (KD low-mid); each links the `exclusive-real-estate-leads` spoke.
- `best-real-estate-lead-generation-companies` — the listicle format (already parked in the old roadmap); high-intent, must stay honest/fair.

**Priority 6 — Ongoing rhythms (not one-time):**
- **Industry News** as laws/rulings/NAR news drop — repeatable, earns fresh-source links and Preferred-Source weight.
- **Case studies** — publish every *real, confirmed* client result the moment it exists, documented + specific + anonymized unless permission to name. **Proof is the one true remaining gap; it closes one client at a time, never by fabrication.**

### 13.6 Guardrails for every roadmap item (unchanged brand rules)
- Honest or don't publish; name competitors fairly; say when NOT to buy.
- No fabricated stats/quotes/testimonials/ratings — real numbers with outbound links to trusted primary sources.
- Question-first title + TL;DR + H2 fan-out + FAQ + schema (the `gen_blog.py` anatomy).
- 1–2 contextual internal links to the right service/audience/hub.
- Hero via the Gemini script, brand palette, **no text/letters** — regenerate if any appear.
- Ping IndexNow after the page is live.
- Don't chase head terms; verify KD in OpenSEO before a batch; re-pull the domain overview to measure progress.

---

## 14. Roadmap / ideas parked (product, not content)

- **Email newsletter** — the last unbuilt item from the Stridec gap (owned audience + nurture). Highest-value parked product idea.
- **Case-studies + design-portfolio + testimonials sections** — all gated on real clients; never fabricate. Treat the first 2-3 clients as documented case studies from day one (the lead-magnets case study is #1).
- **Agent-website teardowns** as a recurring content format (each needs a real site to critique).
- **The real remaining gap is proof, not content or product.** The content and tool gaps vs. every competitor are closed; what can't be *built* is client results. That closes one client at a time.
