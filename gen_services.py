#!/usr/bin/env python3
"""CitedRealty service-page generator.
Edit SERVICES below, then run:  python3 gen_services.py
Regenerates every services/<slug>.html from the shared template.
"""
import html as h
import pathlib

BRAND_URL = "https://citedrealty.com"
OUT = pathlib.Path(__file__).parent / "services"

SERVICES = [
    {
        "slug": "ai-citations",
        "cite": "[1]",
        "nav": "AI Citations (GEO)",
        "title": "AI Citation Building (GEO) for Realtors | CitedRealty",
        "desc": "Get named by ChatGPT, Gemini, Perplexity, and Google AI Overviews when sellers and buyers ask who to work with. Generative Engine Optimization for real estate agents.",
        "tag": "Flagship service",
        "h1": "Be the name AI gives <span class='grad'>your market.</span>",
        "lede": "When sellers and buyers ask ChatGPT, Gemini, Perplexity, or Google's AI who to work with, those systems name <b>specific agents</b> and cite the sources they trust. We build the sources — and make you the name.",
        "features": [
            ("Entity building", "One consistent, machine-readable identity — name, brokerage, markets, specialties — across every profile and data source AI learns from."),
            ("Citable content", "Pages and articles structured the way answer engines quote: direct answers, clear sourcing, real local expertise."),
            ("Structured data", "RealEstateAgent schema, sameAs graphs, and service markup so AI systems can parse exactly who you are and where you work."),
            ("Third-party mentions", "Local press, directories, and community sites — the independent mentions AI treats as evidence, not advertising."),
            ("AI visibility tracking", "Monthly reports on who gets named across ChatGPT, Gemini, Perplexity, and AI Overviews for your market's key questions."),
            ("Answer-gap targeting", "We find the questions AI currently answers weakly in your market — the fastest citations to win."),
        ],
        "steps": [
            ("Audit", "We ask every major AI your market's questions and map who gets named, cited, and why."),
            ("Align", "Your entity gets fixed: profiles, schema, and citations all telling the same story."),
            ("Publish", "Citable sources go live — neighborhood pages, answers, mentions."),
            ("Track", "Visibility is measured monthly; we expand into every gap that opens."),
        ],
        "outcome_h2": "Sellers interview two or three agents. AI writes the shortlist.",
        "outcome_p": "Our job is making sure the shortlist starts with you — in every assistant your market asks.",
        "related": ["local-seo", "content", "reviews"],
    },
    {
        "slug": "website-design",
        "cite": "[2]",
        "nav": "Website Design",
        "title": "Real Estate Website Design for Agents & Teams | CitedRealty",
        "desc": "Custom, AI-citable website design for realtors and teams: schema-first architecture, neighborhood pages built in, fast, SEO- and GEO-ready — and you own it outright.",
        "tag": "Agent & team websites",
        "h1": "A website AI can <span class='grad'>actually cite.</span>",
        "lede": "Most agent websites are pretty brochures machines can't read — or rented templates that rank for nothing and vanish when you stop paying the platform. We design custom sites for agents and teams that are fast, schema-first, and built around neighborhood architecture. <b>And you own it outright.</b>",
        "features": [
            ("Custom design, your brand", "Designed around your market, brand, and listings in a 1-on-1 process — not a theme with your headshot dropped in."),
            ("Schema-first build", "RealEstateAgent, place, and FAQ structured data wired in from day one, so search engines and AI parse exactly who you are and where you win."),
            ("Neighborhood architecture", "Your 5, 15, or 30 farm areas built into the site's structure — the page framework every ranking and citation hangs on."),
            ("Fast by construction", "Lean, static-fast pages that pass Core Web Vitals without plugins fighting each other."),
            ("IDX & listing pages", "Optional MLS search, plus a dedicated page for every listing that markets you to the next seller — not just the house."),
            ("Built to capture", "Audit- and valuation-style lead forms, call tracking ready, and clean handoff into whatever CRM you run."),
        ],
        "steps": [
            ("Design consult", "Your brand, market position, and territories — mapped into a site plan, 1-on-1."),
            ("Build", "Custom design and copy, reviewed with you at every pass."),
            ("Wire", "Schema, internal links, analytics, and forms — the invisible layer that does the ranking."),
            ("Launch & grow", "The content engine and neighborhood pages plug straight in. The site compounds from day one."),
        ],
        "outcome_h2": "Not a brochure. A citation source.",
        "outcome_p": "Your website becomes the hub every other channel feeds — the source Google ranks and AI assistants quote. Custom builds are included with Local Hero and Market Authority, and available as a standalone project on Local Presence.",
        "related": ["local-seo", "ai-citations", "content"],
    },
    {
        "slug": "google-business-profile",
        "cite": "[3]",
        "nav": "Google Business Profile",
        "title": "Google Business Profile Management for Realtors | CitedRealty",
        "desc": "GBP optimization, posts, Q&A, photos, and review strategy that put realtors in the Google map pack for agent-intent searches — and keep them there.",
        "tag": "Local visibility",
        "h1": "Own the map pack for <span class='grad'>agent searches.</span>",
        "lede": "The map pack is the one piece of Google real estate portals can't own. Your Business Profile is your storefront for \"realtor near me\" and every agent-intent search — <b>we run it like it matters.</b>",
        "features": [
            ("Profile optimization", "Categories, services, attributes, and descriptions tuned to how Google actually matches agent-intent searches."),
            ("Weekly posts", "Listings, closings, market notes, and neighborhood spotlights — a profile that reads alive, because it is."),
            ("Review strategy", "A systematic ask-and-respond rhythm that grows reviews mentioning your neighborhoods and specialties."),
            ("Q&A management", "The questions prospects ask, answered by you before a stranger answers them wrong."),
            ("Photo & video cadence", "Fresh, geotagged visual proof of you working your market."),
            ("Spam defense", "Keyword-stuffed competitors and fake listings reported and pursued — the map pack seats you deserve, defended."),
        ],
        "steps": [
            ("Audit & clean", "Duplicates, wrong categories, weak sections — found and fixed."),
            ("Optimize", "Every field, service, and attribute rebuilt against what ranks."),
            ("Cadence", "Posts, photos, Q&A, and review responses on a weekly rhythm."),
            ("Defend & expand", "Spam reported, justifications engineered, insights reviewed monthly."),
        ],
        "outcome_h2": "Calls from people who already chose you.",
        "outcome_p": "A worked profile turns map-pack impressions into calls, direction requests, and listing appointments — no shared leads, no bidding.",
        "related": ["reviews", "local-seo", "ai-citations"],
    },
    {
        "slug": "local-seo",
        "cite": "[4]",
        "nav": "Local SEO & Neighborhoods",
        "title": "Local SEO & Neighborhood Pages for Realtors | CitedRealty",
        "desc": "Technical SEO foundations plus dedicated neighborhood pages that win the local searches Zillow underserves — and give AI a citable local expert.",
        "tag": "Foundations",
        "h1": "Own the neighborhoods <span class='grad'>portals fly over.</span>",
        "lede": "You'll never outrank Zillow for \"homes for sale in [city]\" — and you don't need to. <b>\"[Neighborhood] realtor\"</b>, <b>\"selling a home in [neighborhood]\"</b> — those are winnable, valuable, and exactly what AI wants a citable local expert for.",
        "features": [
            ("Technical foundations", "Speed, crawlability, canonicals, and clean architecture — the unglamorous work everything else stands on."),
            ("Neighborhood pages", "A dedicated, genuinely useful page for every community you farm — 5, 15, or 30 by plan."),
            ("Real estate schema", "RealEstateAgent, place, and FAQ markup wired together so search and AI parse your expertise."),
            ("Internal link architecture", "Neighborhoods, services, and content linked the way crawlers understand authority."),
            ("Citation consistency", "Your name, brokerage, and markets identical across every directory that matters."),
            ("Market-update content", "Quarterly refreshes with real local data, so pages stay current and re-citable."),
        ],
        "steps": [
            ("Territory", "Pick the neighborhoods worth owning — your farm, your data, our search analysis."),
            ("Build", "Pages written and designed as real local resources, not doorway pages."),
            ("Wire", "Schema, internal links, and citations connect it into one entity."),
            ("Refresh", "Market data updates keep every page alive and earning."),
        ],
        "outcome_h2": "Your name, attached to your neighborhoods, everywhere it counts.",
        "outcome_p": "In Google results, in the map pack, and in AI answers — the neighborhoods you farm become searches you win.",
        "related": ["ai-citations", "content", "google-business-profile"],
    },
    {
        "slug": "content",
        "cite": "[5]",
        "nav": "Blog & Content",
        "title": "Real Estate Blog & Content Engine | CitedRealty",
        "desc": "Question-first articles, TL;DR answer blocks, and local market content written to be cited by AI and genuinely useful to sellers and buyers.",
        "tag": "Content engine",
        "h1": "Answer what your market <span class='grad'>already asks.</span>",
        "lede": "Sellers search \"should I sell now or wait.\" Buyers ask \"how much do I need to buy in [city].\" We publish genuinely useful, question-first answers under <b>your</b> name — the raw material AI recommendations are made of.",
        "features": [
            ("Question-first articles", "Titles that match real questions, mined from what your market actually asks AI and Google."),
            ("Liftable answers", "Every post opens with a concise TL;DR block an answer engine can quote — with your name on it."),
            ("Local market updates", "Monthly takes on your market's numbers that portals' national content can't match."),
            ("Buyer & seller guides", "Evergreen cornerstone guides that earn links, rankings, and citations year-round."),
            ("Schema on everything", "BlogPosting + FAQ markup so both search engines and LLMs parse every answer."),
            ("Seasonal calendar", "Planned around rate moves, school calendars, and listing seasons — never content for content's sake."),
        ],
        "steps": [
            ("Mine", "Real questions from your market — AI prompts, search data, and what clients ask you."),
            ("Write", "Genuinely useful answers in your voice; no filler, no scraped fluff."),
            ("Publish", "Structured, schema'd, and internally linked into your neighborhood pages."),
            ("Measure", "Track rankings, citations, and which answers turn into conversations."),
        ],
        "outcome_h2": "A library that keeps earning after you stop paying for it.",
        "outcome_p": "Every answer published is an asset: it ranks, it gets cited, and it pre-sells the client before the first call.",
        "related": ["ai-citations", "local-seo", "social-media"],
    },
    {
        "slug": "social-media",
        "cite": "[6]",
        "nav": "Social Media",
        "title": "Social Media for Realtors — Guidance to Full Management | CitedRealty",
        "desc": "Strategy, calendars, and coaching for agents — or fully done-for-you social management. Presence that makes the AI recommendation feel inevitable.",
        "tag": "Presence",
        "h1": "Show up where your <span class='grad'>market scrolls.</span>",
        "lede": "Social won't rank you — but it's where your market decides you're <b>real</b>. When AI or a friend names you, your feed is the background check. We make sure it closes.",
        "features": [
            ("Strategy & positioning", "What you post, where, and why — matched to your market and personality, not a generic agent template."),
            ("Content calendar", "A month of posts planned at a time: listings, neighborhoods, market takes, proof."),
            ("Listing & sold templates", "Launch and close every listing with content that markets you, not just the house."),
            ("Neighborhood spotlights", "The same neighborhoods you farm on your site, shown as lived-in local knowledge."),
            ("Short-form video coaching", "Scripts and structures for the video your market actually watches."),
            ("Full management", "On Market Authority: created, posted, and managed for you — you approve, we run it."),
        ],
        "steps": [
            ("Position", "Audit your presence and define the angle only you can own."),
            ("Plan", "Calendar built; templates and scripts delivered."),
            ("Produce", "You post with coaching — or we run it end to end, by plan."),
            ("Scale", "Double down on formats your market responds to."),
        ],
        "outcome_h2": "The background check that closes the deal.",
        "outcome_p": "Recommendation → profile check → DM. A worked feed turns the name they heard into the agent they contact.",
        "related": ["content", "reviews", "google-business-profile"],
    },
    {
        "slug": "reviews",
        "cite": "[7]",
        "nav": "Reviews & Reputation",
        "title": "Review Generation & Reputation for Realtors | CitedRealty",
        "desc": "Systematic review generation, responses, and monitoring for real estate agents — the trust signal AI, Google, and sellers all check.",
        "tag": "Trust signals",
        "h1": "The proof every <span class='grad'>recommendation checks.</span>",
        "lede": "AI weighs reviews. Google weighs reviews. And every seller who hears your name reads them within minutes. We make review generation <b>systematic</b> instead of occasional.",
        "features": [
            ("Post-closing system", "Every closing triggers a review ask at the moment clients are happiest — automatically, politely, repeatably."),
            ("Multi-platform", "Google first, then Zillow, Facebook, and the platforms your market reads — reviews on portals work for you, not them."),
            ("Response writing", "Every review answered in your voice — because responses are read by the next seller, and by AI."),
            ("Justification engineering", "Reviews that mention your neighborhoods and specialties become the snippets Google shows under your name."),
            ("Reputation monitoring", "New reviews and mentions surfaced weekly, everywhere they appear."),
            ("Negative review protocol", "A calm, tested playbook for the bad one — response, context, and recovery."),
        ],
        "steps": [
            ("Systemize", "Ask timing, links, and templates set up around your closing workflow."),
            ("Route", "Happy clients guided to the platform where their words work hardest."),
            ("Respond", "Every review answered; key phrases reinforced."),
            ("Monitor", "Weekly watch, monthly reporting, protocol ready if anything turns."),
        ],
        "outcome_h2": "A review base that makes choosing you feel safe.",
        "outcome_p": "The AI's recommendation, the map-pack snippet, and the seller's gut check all read the same reviews. Make them count.",
        "related": ["google-business-profile", "ai-citations", "social-media"],
    },
]

BY_SLUG = {s["slug"]: s for s in SERVICES}

NAV_LINKS = """      <li><a href="../index.html#services" aria-haspopup="true">Services</a>
        <ul class="dd">
          <li><a href="../services/ai-citations.html">AI Citations (GEO)</a></li>
          <li><a href="../services/website-design.html">Website Design</a></li>
          <li><a href="../services/google-business-profile.html">Google Business Profile</a></li>
          <li><a href="../services/local-seo.html">Local SEO &amp; Neighborhoods</a></li>
          <li><a href="../services/content.html">Blog &amp; Content</a></li>
          <li><a href="../services/social-media.html">Social Media</a></li>
          <li><a href="../services/reviews.html">Reviews &amp; Reputation</a></li>
        </ul>
      </li>
      <li><a href="../index.html#who" aria-haspopup="true">Who we help</a>
        <ul class="dd">
          <li><a href="../audiences/solo-agents.html">Solo Agents</a></li>
          <li><a href="../audiences/teams.html">Teams</a></li>
          <li><a href="../audiences/brokerages.html">Brokerages</a></li>
          <li><a href="../audiences/listing-agents.html">Listing Agents</a></li>
        </ul>
      </li>
      <li><a href="../index.html#pricing">Pricing</a></li>
      <li><a href="../blog/index.html">Resources</a></li>
      <li><a href="../index.html#faq">FAQ</a></li>"""

FOOT_SERVICES = "\n".join(
    f'          <li><a href="{s["slug"]}.html">{s["nav"]}</a></li>' for s in SERVICES
)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="/assets/icon-square.svg">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{brand}/assets/icon-512.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/styles.css">
<script src="../assets/theme.js"></script>
<script type="application/ld+json">
{schema}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<nav class="nav" id="nav" aria-label="Main">
  <div class="nav-inner">
    <a class="brand" href="../index.html" aria-label="CitedRealty home">
      <img src="../assets/icon-square.svg" alt="" width="34" height="34">
      <span>Cited<span class="r">Realty</span><sup>[1]</sup></span>
    </a>
    <ul class="nav-links">
{nav_links}
    </ul>
    <a class="nav-cta" href="../index.html#contact">Free AI visibility audit</a>
    <button class="theme-toggle" aria-label="Switch to light mode">☀</button>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false">☰</button>
  </div>
</nav>
<div class="mobile-menu" id="mobileMenu">
  <button class="mobile-close" id="mobileClose" aria-label="Close menu">✕</button>
  <a href="../index.html#services">Services</a>
  <a class="mm-sub" href="../services/ai-citations.html">AI Citations (GEO)</a>
  <a class="mm-sub" href="../services/website-design.html">Website Design</a>
  <a class="mm-sub" href="../services/google-business-profile.html">Google Business Profile</a>
  <a class="mm-sub" href="../services/local-seo.html">Local SEO &amp; Neighborhoods</a>
  <a class="mm-sub" href="../services/content.html">Blog &amp; Content</a>
  <a class="mm-sub" href="../services/social-media.html">Social Media</a>
  <a class="mm-sub" href="../services/reviews.html">Reviews &amp; Reputation</a>
  <a href="../index.html#who">Who we help</a>
  <a class="mm-sub" href="../audiences/solo-agents.html">Solo Agents</a>
  <a class="mm-sub" href="../audiences/teams.html">Teams</a>
  <a class="mm-sub" href="../audiences/brokerages.html">Brokerages</a>
  <a class="mm-sub" href="../audiences/listing-agents.html">Listing Agents</a>
  <a href="../index.html#pricing">Pricing</a>
  <a href="../blog/index.html">Resources</a>
  <a href="../index.html#faq">FAQ</a>
  <a href="../index.html#contact" class="grad">Free AI visibility audit →</a>
</div>

<main id="main">
<header class="page-hero">
  <div class="wrap">
    <p class="crumb"><a href="../index.html">Home</a> / <a href="../index.html#services">Services</a> / {nav}</p>
    <span class="cite-tag">{cite} {tag}</span>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="ctas">
      <a class="btn btn-primary" href="../index.html#contact">Get your free AI visibility audit</a>
      <a class="btn btn-ghost" href="../index.html#pricing">See pricing</a>
    </div>
  </div>
</header>

<section class="alt">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">What's included</p>
      <h2>What we do, <span class="grad">specifically.</span></h2>
    </div>
    <div class="feat-grid">
{features}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">How it works</p>
      <h2>Four moves, <span class="grad">repeated monthly.</span></h2>
    </div>
    <div class="steps">
{steps}
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="outcome reveal">
      <h2>{outcome_h2}</h2>
      <p>{outcome_p}</p>
      <a class="btn btn-primary" href="../index.html#contact">Start with a free audit</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Related services</p>
      <h2>Stronger <span class="grad">together.</span></h2>
    </div>
    <div class="rel-grid">
{related}
    </div>
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <a class="brand" href="../index.html"><img src="../assets/icon-square.svg" alt="" width="34" height="34"><span>Cited<span class="r">Realty</span><sup>[1]</sup></span></a>
        <p>Full digital marketing for realtors &amp; brokers, built for the AI answer era. When buyers ask AI, you're the answer.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
{foot_services}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="../index.html#who">Who we help</a></li>
          <li><a href="../index.html#pricing">Pricing</a></li>
          <li><a href="../blog/index.html">Resources &amp; News</a></li>
          <li><a href="../index.html#faq">FAQ</a></li>
          <li><a href="../index.html#contact">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-legal">
      <span>© 2026 CitedRealty · <a href="../privacy.html">Privacy</a> · <a href="../terms.html">Terms</a> · <a href="#" data-cookie-prefs>Cookie preferences</a> · <a href="https://www.google.com/preferences/source?q=citedrealty.com" target="_blank" rel="noopener" title="Add CitedRealty as a preferred source in Google Search"><span style="color:#F59E0B">★</span> Make us a preferred source on Google</a></span>
      <span>When buyers ask AI, you're the answer.<sup>[1]</sup></span>
    </div>
  </div>
</footer>

<div class="sticky-cta"><a href="../index.html#contact">Get your free AI visibility audit</a></div>
<script src="../assets/app.js"></script>
<script src="../assets/consent.js" defer></script>
</body>
</html>
"""


def strip_tags(s: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", s)


def build(svc: dict) -> str:
    url = f"{BRAND_URL}/services/{svc['slug']}.html"
    features = "\n".join(
        f'      <div class="feat reveal"><div class="k">0{i+1}</div><h3>{h.escape(t)}</h3><p>{h.escape(d)}</p></div>'
        for i, (t, d) in enumerate(svc["features"])
    )
    steps = "\n".join(
        f'      <div class="stepc reveal"><div class="n">0{i+1}</div><h3>{h.escape(t)}</h3><p>{h.escape(d)}</p></div>'
        for i, (t, d) in enumerate(svc["steps"])
    )
    related = "\n".join(
        f'      <a class="rel reveal" href="{r["slug"]}.html"><div class="k">{r["cite"]}</div><h3>{h.escape(r["nav"])}</h3>'
        f'<p>{h.escape(strip_tags(r["lede"]))[:110]}…</p><span class="more">Learn more →</span></a>'
        for r in (BY_SLUG[s] for s in svc["related"])
    )
    import json
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": url + "#service",
                "name": strip_tags(svc["nav"]),
                "serviceType": strip_tags(svc["nav"]) + " for real estate agents",
                "description": svc["desc"],
                "url": url,
                "provider": {"@id": BRAND_URL + "/#business"},
                "areaServed": {"@type": "Country", "name": "United States"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BRAND_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Services", "item": BRAND_URL + "/#services"},
                    {"@type": "ListItem", "position": 3, "name": strip_tags(svc["nav"]), "item": url},
                ],
            },
        ],
    }, indent=2)
    return PAGE.format(
        title=h.escape(svc["title"]), desc=h.escape(svc["desc"]), url=url, brand=BRAND_URL,
        schema=schema, nav=h.escape(svc["nav"]), cite=svc["cite"], tag=h.escape(svc["tag"]),
        h1=svc["h1"], lede=svc["lede"], features=features, steps=steps,
        outcome_h2=h.escape(svc["outcome_h2"]), outcome_p=h.escape(svc["outcome_p"]),
        related=related, nav_links=NAV_LINKS, foot_services=FOOT_SERVICES,
    )


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for svc in SERVICES:
        path = OUT / f"{svc['slug']}.html"
        path.write_text(build(svc))
        print("wrote", path.name)
