#!/usr/bin/env python3
"""CitedRealty audience-page generator.
Edit AUDIENCES below, then run:  python3 gen_audiences.py
Regenerates every audiences/<slug>.html.
"""
import html as h
import json
import pathlib
import re

BRAND_URL = "https://citedrealty.com"
OUT = pathlib.Path(__file__).parent / "audiences"

AUDIENCES = [
    {
        "slug": "solo-agents",
        "nav": "Solo Agents",
        "tag": "Solo agents",
        "title": "Marketing for Solo Real Estate Agents | CitedRealty",
        "desc": "How solo realtors win seller and buyer leads without a team's budget: 5 neighborhoods, an optimized Google Business Profile, and AI citations. From $999/mo.",
        "h1": "Your name. Your neighborhoods. <span class='grad'>Your leads.</span>",
        "lede": "You don't need a team's ad budget to be the agent AI and Google recommend. You need <b>five neighborhoods, worked properly</b> — and a name every system agrees on.",
        "pains": [
            ("Outspent by teams", "Every portal and ad auction favors whoever burns the most cash. That's a game solo agents shouldn't play."),
            ("Shared leads", "The Zillow lead you paid for went to four other agents. The fastest thumb wins, and the portal wins either way."),
            ("Sphere-only pipeline", "Referrals are gold, but they're feast-or-famine. You need demand that arrives while you're at closings."),
        ],
        "plays": [
            ("Win “realtor near me”", "An optimized, worked Google Business Profile puts you in the map pack where agent-intent searches actually happen."),
            ("Five neighborhood pages", "Pick the communities you know cold. We build the pages that make you their answer — in Google and in AI."),
            ("AI citations for your niche", "First-time buyers? Condos? A specific school district? We make AI name you for the questions you want."),
            ("Monthly answers, published", "Blog content that answers what your market asks — every post another reason to cite you."),
        ],
        "plan_name": "Local Presence",
        "plan_price": "$999/mo",
        "plan_line": "Built for exactly this: GBP + local SEO + AI citations + blog + 5 neighborhoods.",
        "related": ["ai-citations", "website-design", "google-business-profile"],
    },
    {
        "slug": "teams",
        "nav": "Teams",
        "tag": "Real estate teams",
        "title": "Marketing for Real Estate Teams | CitedRealty",
        "desc": "Inbound seller and buyer demand for real estate teams: 15 neighborhoods, social guidance, and AI visibility tracking. Stop scaling portal spend linearly.",
        "h1": "Inbound demand worthy of <span class='grad'>your production.</span>",
        "lede": "Referrals built the team. Referrals won't scale it. <b>Fifteen neighborhoods and a compounding engine</b> will — without renting more leads per agent every month.",
        "pains": [
            ("Rainmaker dependency", "When lead flow depends on one person's sphere, every hire dilutes it and every vacation dents it."),
            ("Agent churn", "Agents leave teams that can't feed them. Portal leads per seat is an expense that scales exactly as fast as headcount."),
            ("Linear spend", "Double the agents, double the ad budget, same margins. Rented demand never compounds."),
        ],
        "plays": [
            ("Fifteen neighborhoods", "Divide your market into territories and own them by name — pages, citations, and map-pack presence per area."),
            ("A brand AI can recommend", "Entity building for the team and its producers, so “best team in [city]” has one obvious answer."),
            ("Social guidance", "Strategy, calendar, and coaching so the team brand and every agent's feed pull in the same direction."),
            ("Visibility tracking", "Monthly reporting on who AI names across your market's questions — and where you're gaining."),
        ],
        "plan_name": "Local Hero",
        "plan_price": "$3,999/mo",
        "plan_line": "The most popular plan: everything in Local Presence, a custom website build included, 15 neighborhoods, social guidance, AI tracking.",
        "related": ["website-design", "local-seo", "social-media"],
    },
    {
        "slug": "brokerages",
        "nav": "Brokerages",
        "tag": "Brokerages",
        "title": "Marketing for Real Estate Brokerages | CitedRealty",
        "desc": "Full-market visibility for brokerages: 30 neighborhoods, done-for-you social, weekly strategy, and AI citations that power both deal flow and recruiting.",
        "h1": "Own the market layer <span class='grad'>above every agent.</span>",
        "lede": "When AI answers “best brokerage in [city]”, that one answer is <b>brand, deal flow, and recruiting at once</b>. Somebody's name will be in it. Decide whose.",
        "pains": [
            ("Fragmented marketing", "Every agent runs their own thing; the brokerage brand is the sum of nobody's priority."),
            ("Invisible to AI", "Ask an assistant about brokerages in your market — if the answer is national franchises, your local authority isn't landing."),
            ("Recruiting wars", "Producers join brokerages that make them more visible. Visibility is now a recruiting benefit you can put on the table."),
        ],
        "plays": [
            ("Thirty neighborhoods", "Full-market coverage: every community your agents work gets a page tying it to your brand."),
            ("Done-for-you social", "Created, posted, and managed — the brokerage feed becomes proof of market ownership."),
            ("Weekly strategy hour", "A standing 1-hour consultation with your leadership: what moved, what's next, what agents need."),
            ("Entity building at two levels", "The brokerage and its top producers, both made citable — AI answers name firms and people."),
        ],
        "plan_name": "Market Authority",
        "plan_price": "$6,999/mo",
        "plan_line": "Everything in Local Hero, 30 neighborhoods, full social management, weekly strategy.",
        "related": ["ai-citations", "social-media", "reviews"],
    },
    {
        "slug": "listing-agents",
        "nav": "Listing Agents",
        "tag": "Listing agents",
        "title": "Seller Lead Generation for Listing Agents | CitedRealty",
        "desc": "Win listings before the interview: neighborhood authority, seller-intent content, and reviews that make you the pre-decided choice. For listing-focused agents.",
        "h1": "Win the listing <span class='grad'>before the interview.</span>",
        "lede": "Sellers shortlist two or three agents based on what Google, AI, and their neighbors say — <b>then</b> they book interviews. We get you on the shortlist while the postcard agents wait for a callback.",
        "pains": [
            ("Decided pre-interview", "By the time you're presenting, the seller has usually already ranked you. The CMA rarely changes the order."),
            ("Ignored farming", "Postcards into a neighborhood that's never heard of you is expensive wallpaper."),
            ("Buyer-heavy pipeline", "Buyer leads are everywhere; listings are the business. The marketing that earns them is different."),
        ],
        "plays": [
            ("Neighborhood authority", "Pages for the areas you farm that prove — not claim — local expertise, with real market data."),
            ("Seller-intent content", "“Should I sell now?” “What's my home worth?” Answered under your name, cited by AI."),
            ("Reviews that sell listings", "A review system that surfaces seller stories, sale results, and your neighborhoods — the words Google shows under your name."),
            ("Cited for the seller question", "When someone asks AI who should sell their home in your area, the citations point to you."),
        ],
        "plan_name": "Local Hero",
        "plan_price": "$3,999/mo",
        "plan_line": "Most listing agents start here: 15 neighborhoods of seller-side authority plus social guidance.",
        "related": ["local-seo", "reviews", "ai-citations"],
    },
]

SVC_NAMES = {
    "ai-citations": ("[1]", "AI Citations (GEO)", "Get named by ChatGPT, Gemini, and AI Overviews when your market asks who to work with."),
    "website-design": ("[2]", "Website Design", "Custom, AI-citable sites for agents & teams — schema-first, neighborhood-ready, and yours outright."),
    "google-business-profile": ("[3]", "Google Business Profile", "Map-pack visibility for agent-intent searches, worked weekly."),
    "local-seo": ("[4]", "Local SEO & Neighborhoods", "Dedicated pages for every neighborhood you farm — searches portals underserve."),
    "content": ("[5]", "Blog & Content", "Question-first articles written to be cited by AI and read by humans."),
    "social-media": ("[6]", "Social Media", "From guidance to fully done-for-you — presence that closes the recommendation."),
    "reviews": ("[7]", "Reviews & Reputation", "Systematic review generation — the trust signal every recommendation checks."),
}

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon-32.png">
<link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
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
      <li><a href="../index.html#services">Services</a></li>
      <li><a href="../index.html#who">Who we help</a></li>
      <li><a href="../index.html#pricing">Pricing</a></li>
      <li><a href="../blog/index.html">Resources</a></li>
      <li><a href="../index.html#faq">FAQ</a></li>
    </ul>
    <a class="nav-cta" href="../index.html#contact">Free AI visibility audit</a>
    <button class="theme-toggle" aria-label="Switch to light mode">☀</button>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false">☰</button>
  </div>
</nav>
<div class="mobile-menu" id="mobileMenu">
  <button class="mobile-close" id="mobileClose" aria-label="Close menu">✕</button>
  <a href="../index.html#services">Services</a>
  <a href="../index.html#who">Who we help</a>
  <a href="../index.html#pricing">Pricing</a>
  <a href="../blog/index.html">Resources</a>
  <a href="../index.html#faq">FAQ</a>
  <a href="../index.html#contact" class="grad">Free AI visibility audit →</a>
</div>

<main id="main">
<header class="page-hero">
  <div class="wrap">
    <p class="crumb"><a href="../index.html">Home</a> / <a href="../index.html#who">Who we help</a> / {nav}</p>
    <span class="cite-tag">{tag}</span>
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
      <p class="eyebrow">Sound familiar?</p>
      <h2>The problem, <span class="grad">named.</span></h2>
    </div>
    <div class="feat-grid">
{pains}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">The plays</p>
      <h2>What we run <span class="grad">for you.</span></h2>
    </div>
    <div class="feat-grid">
{plays}
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="outcome reveal">
      <h2>Your plan: {plan_name} — {plan_price}</h2>
      <p>{plan_line} Month-to-month, no long-term contracts.</p>
      <a class="btn btn-primary" href="../index.html#pricing">See what's included</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Where to start</p>
      <h2>The services doing <span class="grad">the heavy lifting.</span></h2>
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
        <h4>Who we help</h4>
        <ul>
{foot_aud}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="../index.html#services">Services</a></li>
          <li><a href="../index.html#pricing">Pricing</a></li>
          <li><a href="../blog/index.html">Resources &amp; News</a></li>
          <li><a href="../index.html#faq">FAQ</a></li>
          <li><a href="../index.html#contact">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-legal">
      <span>© 2026 CitedRealty · <a href="../privacy.html">Privacy</a> · <a href="../terms.html">Terms</a> · <a href="#" data-cookie-prefs>Cookie preferences</a></span>
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
    return re.sub(r"<[^>]+>", "", s)


def build(aud: dict) -> str:
    url = f"{BRAND_URL}/audiences/{aud['slug']}.html"
    pains = "\n".join(
        f'      <div class="feat reveal"><div class="k">✕</div><h3>{h.escape(t)}</h3><p>{h.escape(d)}</p></div>'
        for t, d in aud["pains"]
    )
    plays = "\n".join(
        f'      <div class="feat reveal"><div class="k">0{i+1}</div><h3>{h.escape(t)}</h3><p>{h.escape(d)}</p></div>'
        for i, (t, d) in enumerate(aud["plays"])
    )
    related = "\n".join(
        f'      <a class="rel reveal" href="../services/{slug}.html"><div class="k">{SVC_NAMES[slug][0]}</div>'
        f'<h3>{h.escape(SVC_NAMES[slug][1])}</h3><p>{h.escape(SVC_NAMES[slug][2])}</p>'
        f'<span class="more">Learn more →</span></a>'
        for slug in aud["related"]
    )
    foot_aud = "\n".join(
        f'          <li><a href="{a["slug"]}.html">{a["nav"]}</a></li>' for a in AUDIENCES
    )
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url,
                "name": strip_tags(aud["title"]),
                "description": aud["desc"],
                "url": url,
                "about": {"@id": BRAND_URL + "/#business"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BRAND_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Who we help", "item": BRAND_URL + "/#who"},
                    {"@type": "ListItem", "position": 3, "name": aud["nav"], "item": url},
                ],
            },
        ],
    }, indent=2)
    return PAGE.format(
        title=h.escape(aud["title"]), desc=h.escape(aud["desc"]), url=url, brand=BRAND_URL,
        schema=schema, nav=h.escape(aud["nav"]), tag=h.escape(aud["tag"]),
        h1=aud["h1"], lede=aud["lede"], pains=pains, plays=plays,
        plan_name=h.escape(aud["plan_name"]), plan_price=aud["plan_price"],
        plan_line=h.escape(aud["plan_line"]), related=related, foot_aud=foot_aud,
    )


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for aud in AUDIENCES:
        path = OUT / f"{aud['slug']}.html"
        path.write_text(build(aud))
        print("wrote", path.name)
