#!/usr/bin/env python3
"""CitedRealty blog generator — Resources & News (GEO content hub).
Audience: realtors and brokers asking marketing questions. Goal: when an agent
asks ChatGPT/Google "how do realtors get seller leads", CitedRealty's article
is the citable source.

Add a post: append a dict to POSTS (newest first), run  python3 gen_blog.py
Rebuilds blog/index.html and every article. Write original answers only.
"""
import html as h
import json
import pathlib
import re

BRAND_URL = "https://citedrealty.com"
OUT = pathlib.Path(__file__).parent / "blog"

CATS = {
    "news": "Industry News",
    "howto": "How-To Guides",
    "questions": "Agent Q&A",
    "websites": "Websites",
    "seller-leads": "Seller Leads",
    "buyer-leads": "Buyer Leads",
    "ai": "AI Search",
    "seo": "Local SEO",
    "strategy": "Strategy",
}

POSTS = [
    {
        "slug": "connecticut-private-listings-ban",
        "img": "img/connecticut-private-listings-ban.jpg",
        "img_alt": "Illustration of a house stepping out from behind a velvet rope into open public light",
        "cat": "news",
        "title": "Connecticut's Private Listings Ban (SB 340): What Agents Need to Know",
        "date": "2026-07-20",
        "excerpt": "Connecticut just became the biggest state to outlaw hidden listings. What SB 340 requires by October 1, who it applies to, and what it signals about where listing marketing is headed.",
        "tldr": "Connecticut Governor Ned Lamont signed SB 340 on May 27, 2026 — effective October 1, 2026 — requiring that any 1–4 unit residential listing be made available to the general public (via an MLS, consumer portal, or unrestricted platform) at the same time any marketing begins, including social posts, email blasts, yard signs, and brokerage-network promotion. Sellers can still opt out of public marketing by signing a standardized form; violations carry penalties up to $5,000 or license suspension. It's the sharpest state-level answer yet to the growth of private listing networks, New York is weighing a similar bill, and the strategic takeaway for agents is blunt: exclusivity-as-lead-generation is being legislated away — owned visibility is what remains.",
        "sections": [
            ("What SB 340 actually requires",
             "<p>The core rule is simultaneity: the moment an agent markets a residential listing (1–4 units) <i>anywhere</i> — a teaser on Instagram, an email to a buyer list, a lawn sign, a private brokerage network — that listing must also be available to the general public through an MLS, a consumer-facing portal, or another unrestricted online platform. No more marketing to a favored audience first and the public later.</p>"
             "<p>The seller escape hatch is real but deliberate: a homeowner can decline public marketing entirely by signing a standardized opt-out. What's gone is the gray zone where \"the seller wanted privacy\" justified selective exposure that mostly served the brokerage's lead funnel. Penalties reach $5,000 per violation or license suspension. Effective date: <b>October 1, 2026</b>. (Coverage: <a href='https://www.realtor.com/news/real-estate-news/connecticut-private-listings-ban-ned-lamont/' rel='nofollow'>Realtor.com</a>, <a href='https://www.inman.com/2026/06/03/connecticut-restricting-private-listings/' rel='nofollow'>Inman</a>, <a href='https://www.housingwire.com/articles/connecticut-private-listing-law/' rel='nofollow'>HousingWire</a>.)</p>"),
            ("Why states are doing this",
             "<p>Private listing networks grew fast after the industry began fighting over NAR's Clear Cooperation Policy — some large brokerages built \"exclusive inventory\" strategies where listings premiered inside their own walls. Proponents call it seller choice; critics call it demand-hoarding that shrinks exposure (often costing sellers money) and walls off inventory from buyers outside the network.</p>"
             "<p>Connecticut's legislature sided with exposure. New York has a similar bill moving, and several states are watching. Whatever your view of the policy, the direction of travel is consistent: regulators keep choosing the open market over the velvet rope.</p>"),
            ("What Connecticut agents should do before October 1",
             "<ul><li><b>Audit your pre-launch workflow.</b> If your listing launch sequence includes any audience-facing step before MLS/public availability — socials, database emails, sign installs — it now needs the public listing live first or simultaneously.</li>"
             "<li><b>Get the opt-out process right.</b> Sellers who genuinely want privacy need the standardized form signed <i>before</i> any marketing decisions, documented in the file.</li>"
             "<li><b>Brief your team.</b> The $5,000-per-violation exposure lands on licensees; a casual \"sneak peek\" story post by a team member is now a compliance event.</li>"
             "<li><b>Ask your MLS and broker counsel</b> how they're interpreting edge cases — this article is reporting, not legal advice.</li></ul>"),
            ("The bigger signal: exclusivity is dying as a marketing strategy",
             "<p>Here's the strategic read. For a decade, some brokerages recruited agents and captured buyers with a simple pitch: <i>we have inventory nobody else can show you.</i> Laws like SB 340 dismantle that pitch one state at a time. When every listing must be public the moment it's marketed, hoarded inventory stops being a moat.</p>"
             "<p>What can't be legislated away is <b>being the agent people find and trust when everything is public</b> — the map-pack presence, the <a href='../services/local-seo.html'>neighborhood authority</a>, the reviews, and increasingly the <a href='../services/ai-citations.html'>AI citations</a> that make assistants name you. In a fully open market, visibility is the only exclusivity left. Agents who built their pipeline on access should start building it on being found.</p>"),
        ],
        "faqs": [
            ("When does Connecticut's private listings law take effect?",
             "October 1, 2026. SB 340 was signed by Governor Ned Lamont on May 27, 2026, and applies to marketing of residential listings of one to four units."),
            ("Does SB 340 ban office exclusives completely?",
             "No — a seller can still choose no public marketing by signing a standardized opt-out form. What the law bans is selective marketing: promoting a listing to some audience while withholding it from the general public."),
            ("Do social media teasers count as marketing under the law?",
             "Yes — social posts, email campaigns, yard signs, digital ads, and brokerage-network promotion all trigger the requirement that the listing be publicly available at the same time. Confirm specifics with your broker or counsel; this is reporting, not legal advice."),
            ("Will other states pass similar laws?",
             "New York's similar bill was headed to the governor as of mid-2026, and industry coverage reports several states considering the same approach. The trend since the Clear Cooperation fights has been toward mandated exposure, not away from it."),
        ],
    },
    {
        "slug": "california-ai-listing-photo-law",
        "img": "img/california-ai-listing-photo-law.jpg",
        "img_alt": "Illustration of a framed house photo with an AI sparkle wand and a small disclosure tag",
        "cat": "news",
        "title": "California's AI Listing Photo Law (AB 723): What Agents Must Disclose Now",
        "date": "2026-07-20",
        "excerpt": "The first state law on AI-edited listing photos is in effect — and studies suggest most altered listings still aren't complying. What AB 723 requires, what's exempt, and why disclosure is becoming a trust play.",
        "tldr": "California's AB 723, signed October 10, 2025 and effective January 1, 2026, is the first state law specifically governing digitally altered and AI-edited listing photos. It adds Business & Professions Code §10140.8, requiring two things whenever a listing image changes how a property or its surroundings actually look: a clear, conspicuous disclosure on the listing (e.g. \"digitally altered\" or \"virtually staged\"), and access to the original unaltered photo — via link, URL, or QR code when AI is used. Routine edits (lighting, color correction, cropping, sharpening, straightening) are exempt, and virtual staging remains legal with disclosure. The compliance gap is huge: one study found over 90% of digitally altered portal listings carried no disclosure — which makes clean disclosure both a legal necessity in California and an easy trust differentiator everywhere.",
        "sections": [
            ("What AB 723 actually requires",
             "<p>The law is narrow and specific. If a listing photo has been digitally altered — by editing software or AI — in a way that changes how the property or its surroundings actually look, two obligations kick in: the listing must carry a clear, reasonably conspicuous disclosure that the image is altered, and viewers must be able to access the original, unaltered photo. When AI did the altering, that access means a link, URL, or QR code to the original image.</p>"
             "<p>It took effect January 1, 2026 as Business &amp; Professions Code §10140.8. (Coverage: <a href='https://www.sfchronicle.com/realestate/article/california-law-home-listing-photos-21308040.php' rel='nofollow'>San Francisco Chronicle</a>, <a href='https://www.housingwire.com/articles/most-ai-altered-listings-go-undisclosed-california-law-bans-it/' rel='nofollow'>HousingWire</a>, and a useful legal breakdown from <a href='https://barneswalker.com/starting-january-1-2026-california-turns-ai-edited-listing-photos-into-a-legal-compliance-issue-not-just-an-mls-issue-is-florida-next/' rel='nofollow'>Barnes Walker</a>.)</p>"),
            ("What counts as altered — and what doesn't",
             "<ul><li><b>Requires disclosure:</b> virtual staging (furniture that isn't there), removing or adding objects, altering lawns or skies to look better than reality, AI renovations of dated rooms — anything that changes what the place actually looks like.</li>"
             "<li><b>Exempt routine edits:</b> lighting and exposure adjustments, white balance, color correction, sharpening, cropping, and straightening — normal photography workflow is fine undisclosed.</li>"
             "<li><b>Still legal:</b> virtual staging itself. California didn't ban the tool; it banned the pretense. Disclose it, provide the original, and stage away.</li></ul>"),
            ("The 90% problem",
             "<p>Here's the striking part: research cited in HousingWire's coverage found roughly one in nine listing photos on major portals showed digital alterations — and more than 90% of those carried no disclosure. In California, that gap is now a legal exposure. Everywhere else, it's a trust time bomb: buyers who tour a home that doesn't match its photos remember the agent who showed it to them.</p>"
             "<p>Expect the pattern from our <a href='connecticut-private-listings-ban.html'>Connecticut SB 340 coverage</a> to repeat here too — first-state laws in real estate marketing rarely stay single-state, and commentators are already asking whether Florida follows.</p>"),
            ("The marketing takeaway: disclosure is a differentiator now",
             "<p>The agents who treat AB 723 as annoying paperwork are missing the play. In a market where 90% of altered photos hide it, <i>\"virtually staged — original photo here\"</i> reads as integrity, and integrity is precisely what sellers are vetting when they Google you. Clean disclosure practices belong in the same trust stack as your reviews and your <a href='../services/content.html'>published answers</a> — evidence that what you say matches what's real.</p>"
             "<p>Practical workflow, whatever your state: label every virtually staged image in the MLS and on socials, keep originals organized and linkable, brief your photographer and your <a href='../services/social-media.html'>social workflow</a> on which edits cross the line, and when in doubt, disclose. (California agents: confirm specifics with your broker or counsel — this is reporting, not legal advice.)</p>"),
        ],
        "faqs": [
            ("Is virtual staging still legal in California?",
             "Yes — AB 723 doesn't ban virtual staging. It requires that virtually staged or AI-altered images carry a clear disclosure on the listing and that viewers can access the original unaltered photo (via link, URL, or QR code when AI is used)."),
            ("Do I have to disclose basic photo edits like brightness or color correction?",
             "No. Routine adjustments — lighting, exposure, white balance, color correction, sharpening, cropping, straightening — are exempt. The disclosure duty applies to edits that change how the property or its surroundings actually look."),
            ("When did AB 723 take effect, and who does it apply to?",
             "It was signed October 10, 2025 and took effect January 1, 2026, adding §10140.8 to California's Business & Professions Code. It governs California listing marketing; agents elsewhere should watch their own states — legal commentators are already predicting copycat bills."),
            ("Does AI-generated listing photography hurt or help marketing?",
             "Used honestly, it helps: staged visuals demonstrably improve engagement, and disclosure doesn't reduce that. What hurts is the gap between photos and reality — buyers who feel misled at the showing blame the agent, and that reputation cost outlasts any click-through gain."),
        ],
    },
    {
        "slug": "nar-coming-soon-listings-rules",
        "img": "img/nar-coming-soon-listings-rules.jpg",
        "img_alt": "Illustration of a house glowing softly behind a partially lifted curtain",
        "cat": "news",
        "title": "NAR's Statement on Coming-Soon Listings: What the Rules Actually Allow",
        "date": "2026-07-20",
        "excerpt": "NAR clarified where pre-marketing and coming-soon listings stand under Clear Cooperation and the new seller options. The rules are looser than most agents think — and more local.",
        "tldr": "In a March 20, 2026 statement, NAR clarified that the Clear Cooperation Policy does not prohibit pre-marketing approaches like coming-soon listings or office exclusives; CCP requires submitting a listing to the MLS within one business day of public marketing, and the Multiple Listing Options for Sellers policy (March 2025) lets sellers choose delayed-marketing paths with delay periods set by each MLS. NAR also clarified that national policy doesn't mandate tracking days-on-market or price cuts — that's local MLS discretion. Practical translation: coming-soon is a legitimate tool, the controlling rules are your local MLS's, and the pre-launch window is a marketing opportunity most agents waste.",
        "sections": [
            ("What NAR actually said",
             "<p>NAR's <a href='https://www.nar.realtor/news/real-estate-news/law-and-ethics/nar-releases-statement-on-pre-marketing-and-coming-soon-listings' rel='nofollow'>March 2026 statement</a> pushed back on the idea that national policy forbids pre-marketing. The through-line: the MLS system exists to let sellers market \"in accordance with their interest,\" and each MLS has flexibility to set local rules. Coming-soon listings and office exclusives are not prohibited by the Clear Cooperation Policy.</p>"
             "<p>Two clarifications matter most. First, CCP's actual mechanism: once a listing is publicly marketed, it must be submitted to the MLS within one business day — that's a sequencing rule, not a ban. Second, NAR's FAQ confirmed that tracking days-on-market and price reductions is local discretion, not national mandate (though where an MLS does track it, participants may share it with consumers).</p>"),
            ("The policy stack, decoded",
             "<ul><li><b>Clear Cooperation Policy (CCP):</b> public marketing starts a one-business-day clock to MLS submission. Pre-marketing statuses exist within it, not against it.</li>"
             "<li><b>Multiple Listing Options for Sellers (MLOS, March 2025):</b> gives sellers formal delayed-marketing choices — listed in the MLS but with distribution delayed — with each MLS setting its own delay periods.</li>"
             "<li><b>Local MLS rules:</b> the actual controlling document. Coming-soon status mechanics, showing restrictions during pre-market, and DOM tracking all vary by market — read yours before building a launch process. (And note the direction of state law: Connecticut now <i>requires</i> public availability the moment marketing starts — covered in our SB 340 breakdown.)</li></ul>"),
            ("The marketing opportunity hiding in the pre-launch window",
             "<p>Here's what most coverage misses: a coming-soon window is the one phase of a listing where the <b>agent</b> is the only way in. The property isn't browsable on portals yet — so curious neighbors and buyers who hear about it Google <i>you</i>. If that search finds a worked <a href='../services/google-business-profile.html'>Google Business Profile</a>, a real page for that neighborhood, and reviews from nearby sellers, the pre-launch window converts twice: demand for the house, and listing appointments from every neighbor watching how you launch.</p>"
             "<p>Run it with substance: a genuine coming-soon post cadence, the neighborhood page updated with the upcoming listing, and launch-day timing that respects your MLS's one-business-day clock. Pre-marketing done inside the rules is a demand tool; done sloppily it's a compliance complaint.</p>"),
        ],
        "faqs": [
            ("Are coming-soon listings allowed under NAR's Clear Cooperation Policy?",
             "Yes. NAR's March 2026 statement explicitly says CCP does not prohibit pre-marketing approaches like coming-soon listings or office exclusives. CCP's requirement is that once public marketing begins, the listing is submitted to the MLS within one business day. Local MLS rules govern the details."),
            ("Do coming-soon days count toward days on market?",
             "It depends on your MLS. NAR clarified that national policy doesn't require DOM or price-reduction tracking at all — it's local discretion. Where an MLS does track it, participants may share that data with consumers. Check your local rules before promising a seller anything about DOM."),
            ("Can I post a coming-soon listing on social media?",
             "Generally yes — but social promotion is public marketing, which starts CCP's one-business-day MLS submission clock, and in some states (Connecticut, from October 2026) the listing must be publicly available simultaneously. Know both your MLS rules and your state law; this is reporting, not legal advice."),
        ],
    },
    {
        "slug": "optimize-google-business-profile-realtor",
        "img": "img/optimize-google-business-profile-realtor.jpg",
        "img_alt": "Illustration of a glowing map pin above a storefront-style house with checklist marks",
        "cat": "howto",
        "title": "How to Optimize Your Google Business Profile as a Realtor: Step-by-Step",
        "date": "2026-07-20",
        "excerpt": "The complete 2026 walkthrough — categories, hours, reviews, posts — with the current algorithm shift most guides miss: Google now rewards profiles that look alive.",
        "tldr": "To optimize a realtor Google Business Profile in 2026: claim and verify it under your exact real-world name (keyword-stuffed names risk suspension), set \"Real Estate Agent\" as your primary category (the strongest controllable ranking lever), complete every field including accurate hours — being open at search time is now a confirmed ranking factor — then work the profile weekly: posts, fresh photos, review velocity, and responses. The big 2026 shift: Google's local algorithm has moved weight from static prominence toward engagement and activity signals, so an actively worked profile now outranks an established-but-dormant one. Setup is a weekend; ranking is a habit.",
        "sections": [
            ("Step 1: Get the foundation exactly right",
             "<p>Claim the profile at business.google.com and verify. Use your <b>exact real-world name</b> — \"Jane Rivera, Realtor\" not \"Jane Rivera | Scottsdale Homes For Sale Top Agent.\" Keyword-stuffed names are the #1 local spam tactic and a genuine suspension risk. Use a local phone number you answer, and link the website page most relevant to your work (your site's homepage, or your team page — with UTM tags so you can see GBP traffic in analytics).</p>"
             "<p>One 2026 housekeeping note: Google is retiring GBP chat/messaging (fully ends July 31, 2026) — so make the call button and website your conversion paths, not chat.</p>"),
            ("Step 2: Categories — the biggest lever you control",
             "<p>Primary category is the strongest ranking signal after proximity. For most agents that's <b>Real Estate Agent</b>; teams and offices may fit \"Real Estate Agency.\" Then add every legitimately applicable additional category (up to 9) — e.g. \"Real Estate Consultant,\" \"Property Management Company\" only if you actually do it. Aspirational categories hurt relevance; check what the agents actually ranking in your map pack use.</p>"),
            ("Step 3: Fill everything — including hours (yes, hours rank)",
             "<p>Write the 750-character description: what you do, where, for whom, what's different — no keyword stuffing, no phone numbers. List every service with a description (\"Seller representation in [neighborhoods]\", \"First-time buyer guidance\"). Complete every applicable attribute.</p>"
             "<p>Then hours — the ranking factor most agents shrug past: <b>businesses open at the moment of search rank better</b>, and rankings degrade in the final hour before closing. If you genuinely answer your phone evenings and weekends (most agents do), your stated hours should say so. Never fake hours you won't answer — a missed call is its own penalty.</p>"),
            ("Step 4: Photos, posts, and the \"looks alive\" test",
             "<p>Ten to fifteen real photos minimum — you working, your listings, your neighborhoods, your team — then two or three new ones monthly. No stock photography; Google and humans both notice. (Skip the geo-tagging folklore: Google strips photo EXIF data on upload — it has no ranking effect.)</p>"
             "<p>Post weekly: a listing, a closing, a market note, a neighborhood spotlight. This is where the 2026 algorithm shift bites — Google has moved weight toward <i>engagement and activity</i>: clicks, calls, direction requests, post and photo activity, review velocity. A dormant profile with 100 old reviews now loses to a worked profile with 60 fresh ones. The same activity data feeds Google's AI-generated local answers, which is why this step does double duty for <a href='../services/ai-citations.html'>AI visibility</a>.</p>"),
            ("Step 5: Reviews — velocity beats totals",
             "<p>Recent reviews matter more than lifetime count: a steady drip signals a business that's alive. Build a systematic post-closing ask (full playbook in our <a href='get-more-google-reviews-real-estate-agent.html'>review generation guide</a>), and respond to every review — responses are read by the next seller and parsed by AI. One more 2026 note: Google is replacing user Q&A with AI-generated Q&A drawn from your profile, reviews, and website — another reason the underlying data must be complete and accurate.</p>"
             "<p>Then maintain the rhythm: weekly reviews/posts check, monthly photos and insights, quarterly category and competitor audit. Or have us <a href='../services/google-business-profile.html'>run the whole thing</a> — this checklist is literally the service.</p>"),
        ],
        "faqs": [
            ("What's the most important GBP ranking factor for realtors?",
             "After proximity (which you can't control): your primary category, then overall profile completeness and activity. In 2026, engagement signals — calls, clicks, review velocity, posting activity — have gained weight over static factors, per current industry consensus analysis of local rankings."),
            ("Should each agent on a team have their own Google Business Profile?",
             "Individual practitioner profiles are allowed alongside the office profile if the agent is directly contactable at that location. Keep names clean (agent name, not keywords), categories accurate, and never create multiple profiles for the same person."),
            ("How long until GBP optimization improves my map pack ranking?",
             "Foundational fixes (category, completeness) often show movement within weeks; engagement-driven gains build over one to three months of consistent activity. Measure with a geogrid scan rather than searching yourself — your own results are skewed by your location and history."),
        ],
    },
    {
        "slug": "get-more-google-reviews-real-estate-agent",
        "img": "img/get-more-google-reviews-real-estate-agent.jpg",
        "img_alt": "Illustration of five glowing stars rising from a house like lanterns",
        "cat": "howto",
        "title": "How to Get More Google Reviews as a Real Estate Agent (an Ethical Playbook)",
        "date": "2026-07-20",
        "excerpt": "No bought reviews, no gating, no begging — a system that turns closings into a steady review stream, plus the compliance lines you can't cross.",
        "tldr": "The ethical way to get more Google reviews as a realtor: build the ask into your closing workflow (the moment keys change hands is peak goodwill), make leaving a review effortless with a direct link or QR code, ask specifically but honestly (\"would you mind mentioning the neighborhood and what the process was like?\"), and respond to every review — responses are read by future sellers and parsed by AI. Never buy reviews, never incentivize them (against Google policy and FTC rules), and never \"gate\" by filtering unhappy clients away from the ask. Velocity beats totals: a review a month for a year outranks a one-week blast of twelve, and steady recency is what both Google and AI assistants read as a live, trusted business.",
        "sections": [
            ("The system: ask at the moment of maximum goodwill",
             "<p>Reviews don't come from wanting them; they come from a workflow. The trigger is closing day — clients holding keys are at peak gratitude, and a personal ask converts far better than any automated email: <i>\"It would genuinely help my business if you'd share what this was like — I'll text you the link.\"</i> Then send that text within the hour, while the moment is warm.</p>"
             "<p>Make it effortless: your GBP short link (or a QR code on the closing-gift card) straight to the review box. Every extra tap loses reviewers. For past clients you never asked, one honest campaign — \"I'm building my online presence and your words would mean a lot\" — recovers years of goodwill; space those asks out rather than blasting.</p>"),
            ("Ask for specifics — honestly",
             "<p>A five-star \"great agent!\" helps a little. A review mentioning <i>your neighborhood, the service type, and a real moment</i> helps enormously — those phrases become the review snippets Google shows under your name and the evidence AI assistants weigh. The ethical way to get them is a gentle prompt, not a script: \"If you're up for it, mentioning the neighborhood and how the sale went helps other sellers find me.\" You're suggesting topics, never words — the review must be theirs.</p>"),
            ("The lines you cannot cross",
             "<ul><li><b>Never buy reviews</b> — from anyone, ever. It violates Google policy and, in the US, FTC rules on fake reviews carry real penalties.</li>"
             "<li><b>Never incentivize</b> — discounts, gift cards, or raffle entries for reviews are against Google's policy even when the review is genuine.</li>"
             "<li><b>Never gate</b> — surveying clients first and only asking happy ones for public reviews (\"review gating\") violates policy. Ask everyone; earn the outcome.</li>"
             "<li><b>Never review yourself</b> or have family/colleagues pose as clients. Google's detection keeps improving, and a wiped profile costs more than slow-earned reviews ever would.</li></ul>"),
            ("Respond to everything — including the bad one",
             "<p>Every review gets a response in your voice within a few days: specific, warm, brief. The audience isn't the reviewer — it's the next seller reading your profile and the AI summarizing it. For a negative review: respond once, calmly, with facts and an offline path (\"I'd welcome the chance to talk this through\"). Never argue, never reveal client details, and let one measured response sit beside their words. One bad review answered gracefully often builds more trust than ten unanswered five-stars.</p>"
             "<p>The compounding effect ties the whole <a href='../services/reviews.html'>reputation system</a> together: reviews feed your map-pack rank, the snippets under your name, and the evidence behind every <a href='../services/ai-citations.html'>AI recommendation</a>. It's the single highest-leverage habit in agent marketing — and it costs nothing but consistency.</p>"),
        ],
        "faqs": [
            ("Can I ask clients for Google reviews at all?",
             "Yes — asking is completely allowed and expected. What's prohibited is paying or incentivizing reviews, filtering who you ask based on predicted sentiment (gating), or writing/buying fake ones."),
            ("How many Google reviews does a realtor need?",
             "Enough to be credible against your local competitors, arriving steadily. Recency and velocity now matter more than raw totals — a consistent monthly stream signals an active business better than a large stale pile. Check the agents ranking in your map pack for your market's bar."),
            ("What do I do about a fake or malicious review?",
             "Flag it through your Business Profile for policy violation, respond publicly and calmly noting you have no record of the reviewer as a client, and document everything. Persistent attacks can be escalated through Google's review-removal process."),
        ],
    },
    {
        "slug": "what-data-do-ai-assistants-use",
        "img": "img/what-data-do-ai-assistants-use.jpg",
        "img_alt": "Illustration of data streams flowing from documents, stars, and a globe into an AI chat bubble",
        "cat": "howto",
        "title": "What Data Do ChatGPT and Google's AI Actually Use? (And How Realtors Get Into It)",
        "date": "2026-07-20",
        "excerpt": "Demystifying the pipeline: training data vs. live retrieval, why ChatGPT search runs on Bing, and the specific assets that get an agent into AI answers.",
        "tldr": "AI assistants answer from two layers: training data (a frozen snapshot of the web — you can't edit it, only influence the next one) and live retrieval (real-time search the model runs when you ask something current). Retrieval is where realtors can act now: ChatGPT's web search draws on Bing's index, Google's AI Overviews and AI Mode draw on Google's index, and Perplexity runs its own crawl — so being indexed and authoritative in BOTH Google and Bing is the entry ticket. What gets cited from those indexes: pages that answer questions directly, consistent entity data (schema, profiles that agree with each other), reviews, and independent third-party mentions. Being cited matters commercially: brands cited inside AI answers earn roughly 120% more clicks than brands that aren't (Seer Interactive, 2026).",
        "sections": [
            ("The two layers: what's baked in vs. what's fetched live",
             "<p><b>Training data</b> is the web snapshot a model learned from — months old by the time you're talking to it. If your name is well-represented there (consistent profiles, published content, mentions), the model \"knows\" you; if not, you don't exist to it until retrieval saves you. You can't edit training data retroactively — you can only be present enough that the <i>next</i> training run picks you up.</p>"
             "<p><b>Live retrieval</b> is what happens when the assistant searches the web mid-conversation — which local and \"who should I hire\" questions almost always trigger, because they're current. This is the layer you can influence this quarter.</p>"),
            ("Which index feeds which assistant",
             "<ul><li><b>ChatGPT</b> web search draws on <b>Bing's index</b> — which makes Bing Webmaster Tools (free, imports from Search Console in two clicks) quietly one of the highest-leverage registrations in agent marketing.</li>"
             "<li><b>Google AI Overviews / AI Mode</b> draw on Google's index and ranking systems — your classic SEO work feeds them directly.</li>"
             "<li><b>Perplexity</b> maintains its own crawl with an emphasis on citing sources.</li>"
             "<li><b>Gemini</b> draws on Google's index and infrastructure.</li></ul>"
             "<p>Practical consequence: \"AI SEO\" isn't a separate universe — it's being findable and credible in the two indexes that matter, plus structure that makes you quotable.</p>"),
            ("What actually gets cited",
             "<p>Across the systems, the pattern of citable sources is consistent: pages that <b>answer a question directly</b> (a clear question-shaped heading with a concise answer up top), <b>entity consistency</b> (your name, brokerage, and markets identical across your site, GBP, and profiles — contradictions read as noise), <b>structured data</b> (schema that makes facts machine-readable — see our <a href='realestateagent-schema-walkthrough.html'>schema walkthrough</a>), <b>reviews</b> as third-party evidence, and <b>independent mentions</b> — your own site claims, other sites confirm.</p>"
             "<p>The commercial stakes, from our <a href='real-estate-ai-search-statistics.html'>verified statistics roundup</a>: when an AI Overview appears, brands cited inside it earn about 120% more clicks per impression than brands that aren't — while uncited brands lost 67% of their click-through over 2025 (Seer Interactive).</p>"),
            ("The realtor checklist",
             "<ul><li>Verify your site in <b>Google Search Console AND Bing Webmaster Tools</b>; submit your sitemap to both.</li>"
             "<li>Add RealEstateAgent and FAQ schema; keep it valid (test it — even one missing brace makes it unreadable).</li>"
             "<li>Publish direct answers to your market's questions, each opening with a liftable summary.</li>"
             "<li>Align every profile — GBP, site, socials, directories — on identical name/brokerage/market facts.</li>"
             "<li>Build review velocity and pursue genuine third-party mentions (local press, community sites).</li>"
             "<li>Then audit: ask each assistant your market's questions monthly and track who gets named — that measurement loop is the core of our <a href='../services/ai-citations.html'>AI citations service</a>.</li></ul>"),
        ],
        "faqs": [
            ("Does ChatGPT really use Bing for search?",
             "Yes — ChatGPT's live web search capability draws on Bing's index. That's why an agent invisible to Bing is invisible to a large share of AI-assisted research, and why registering with Bing Webmaster Tools is a five-minute task with outsized payoff."),
            ("Can I pay to appear in AI answers?",
             "Not in the organic answers themselves — there's no placement to buy today. Presence is earned through the retrieval layer: indexed, structured, corroborated content. Be skeptical of anyone selling guaranteed AI placement."),
            ("How often do AI models update their training data?",
             "Major models retrain on cycles measured in months, and cutoffs vary by model. That lag is exactly why live retrieval dominates local answers — and why the durable strategy is strong presence in the underlying indexes rather than trying to game any single model."),
        ],
    },
    {
        "slug": "realestateagent-schema-walkthrough",
        "img": "img/realestateagent-schema-walkthrough.jpg",
        "img_alt": "Illustration of a house blueprint transforming into neat code brackets",
        "cat": "howto",
        "title": "How to Add RealEstateAgent Schema to Your Website: A Walkthrough",
        "date": "2026-07-20",
        "excerpt": "Copy-paste JSON-LD for agents, field by field — plus how to validate it and the one-character mistake that silently broke our own homepage.",
        "tldr": "RealEstateAgent schema is JSON-LD structured data that tells search engines and AI systems exactly who you are, where you work, and what you do — in a format machines can quote instead of guess. Implementation: paste a script tag of type application/ld+json into your site's head with your name, brokerage, URL, phone, service areas, and sameAs links to your profiles; match every fact to your Google Business Profile exactly; validate with Google's Rich Results Test before shipping. Validation isn't optional — one missing brace makes the entire block invisible to machines (we know, because we shipped exactly that bug on this site and Google flagged it within hours).",
        "sections": [
            ("What schema does — and why agents specifically need it",
             "<p>Your website says \"Jane Rivera is a Scottsdale realtor\" in prose a human parses instantly. Schema says it in a structure a machine parses <i>reliably</i> — which matters now that your most influential readers are crawlers deciding whether to cite you. For agents, the payoff is entity clarity: search and AI systems can confirm your name, brokerage, service area, and specialties without inference, which is the foundation every <a href='../services/ai-citations.html'>AI citation</a> stands on.</p>"),
            ("The template, field by field",
             "<p>Paste this inside your site's <code>&lt;head&gt;</code>, edited to your facts:</p>"
             "<pre><code>&lt;script type=&quot;application/ld+json&quot;&gt;\n{\n  &quot;@context&quot;: &quot;https://schema.org&quot;,\n  &quot;@type&quot;: &quot;RealEstateAgent&quot;,\n  &quot;@id&quot;: &quot;https://YOURSITE.com/#agent&quot;,\n  &quot;name&quot;: &quot;Jane Rivera&quot;,\n  &quot;url&quot;: &quot;https://YOURSITE.com/&quot;,\n  &quot;image&quot;: &quot;https://YOURSITE.com/headshot.jpg&quot;,\n  &quot;telephone&quot;: &quot;+1-480-555-0100&quot;,\n  &quot;email&quot;: &quot;jane@YOURSITE.com&quot;,\n  &quot;worksFor&quot;: {&quot;@type&quot;: &quot;RealEstateAgency&quot;, &quot;name&quot;: &quot;Rivera Realty Group&quot;},\n  &quot;areaServed&quot;: [\n    {&quot;@type&quot;: &quot;City&quot;, &quot;name&quot;: &quot;Scottsdale&quot;},\n    {&quot;@type&quot;: &quot;City&quot;, &quot;name&quot;: &quot;Paradise Valley&quot;}\n  ],\n  &quot;knowsAbout&quot;: [&quot;Seller representation&quot;, &quot;First-time buyers&quot;, &quot;North Scottsdale&quot;],\n  &quot;sameAs&quot;: [\n    &quot;https://www.google.com/maps/place/YOUR-GBP-LINK&quot;,\n    &quot;https://www.instagram.com/YOURHANDLE&quot;,\n    &quot;https://www.linkedin.com/in/YOURPROFILE&quot;\n  ]\n}\n&lt;/script&gt;</code></pre>"
             "<p>The fields that do the heavy lifting: <b>areaServed</b> (your neighborhoods — the machine-readable version of your farm), <b>sameAs</b> (links your identity across every profile, collapsing you into one unambiguous entity), and <b>worksFor</b> (ties you to your brokerage's entity). Every value must match your Google Business Profile exactly — mismatched facts read as two different Janes.</p>"),
            ("Validate before you ship (a cautionary tale from this very site)",
             "<p>Run the page through Google's <b>Rich Results Test</b> (search.google.com/test/rich-results) or validator.schema.org before and after publishing. This step is not optional, and we're the proof: this website launched with a single missing closing brace in its FAQ schema — one character — which made the <i>entire</i> structured-data graph unparsable. Google Search Console flagged \"unparsable structured data\" within hours of first crawl. The fix took a minute; catching it before launch would have taken thirty seconds.</p>"
             "<p>JSON is unforgiving: every brace opened must close, every property quoted, no trailing commas. If you hand-edit, re-validate every time.</p>"),
            ("Going further",
             "<p>Once the agent entity is in place: add <b>FAQPage</b> schema to pages that answer questions (marking up real on-page Q&amp;A), <b>BreadcrumbList</b> for site structure, and place-level markup on neighborhood pages. If your platform won't let you touch the head, that's a real limitation worth weighing — schema-first architecture is a core reason we build <a href='../services/website-design.html'>agent websites</a> the way we do.</p>"),
        ],
        "faqs": [
            ("Does schema markup directly improve rankings?",
             "Google's guidance treats structured data as enabling eligibility (rich results) and better understanding, not as a direct ranking boost — claims beyond that are correlation or opinion. Its clearest payoff in 2026 is machine-readability for AI systems deciding what to cite, plus rich-result eligibility."),
            ("Where exactly do I paste the JSON-LD?",
             "In your site's <head> (or before the closing body tag — both work). WordPress users can use a header-scripts plugin or an SEO plugin's schema feature; site-builder users should check for a custom-code or head-injection setting."),
            ("Should the schema go on every page or just the homepage?",
             "The RealEstateAgent entity belongs on your homepage or about page (with an @id other pages can reference). Page-specific schema — FAQPage on Q&A pages, place markup on neighborhood pages — goes on the pages it describes."),
        ],
    },
    {
        "slug": "eeat-for-real-estate-agents",
        "img": "img/eeat-for-real-estate-agents.jpg",
        "img_alt": "Illustration of four glowing pillars supporting a house-shaped roof",
        "cat": "howto",
        "title": "What Is E-E-A-T for Real Estate Agents — and Why AI Cares",
        "date": "2026-07-20",
        "excerpt": "Experience, Expertise, Authoritativeness, Trust — what the framework actually is (and isn't), translated into the assets an agent can build this quarter.",
        "tldr": "E-E-A-T — Experience, Expertise, Authoritativeness, and Trustworthiness — is the framework from Google's Search Quality Rater Guidelines for judging content credibility. Important honesty up front: it is not a direct ranking factor or a score; it's the rubric human raters use to evaluate results, which in turn shapes Google's systems. For realtors it translates cleanly: Experience = proof you've done the work (transaction history, client stories, photos of you working); Expertise = demonstrated market knowledge (neighborhood pages with real data, direct answers); Authoritativeness = others vouching for you (mentions, links, citations, profile consistency); Trust = reviews, accurate information, and a secure professional site. The same signals are what AI assistants proxy when deciding which agent to name — E-E-A-T is the closest thing to a shared rubric between Google and the answer engines.",
        "sections": [
            ("What E-E-A-T actually is (evidence-tier honesty first)",
             "<p>E-E-A-T comes from Google's Search Quality Rater Guidelines — the manual human evaluators use to judge whether results are credible, with the second E (Experience) added in 2022. Precision matters here: <b>it is not a ranking factor, a score, or an algorithm input you can directly optimize</b>. Rater judgments inform how Google builds and tunes its systems, so the framework describes what those systems are <i>aiming</i> at. Anyone selling you an \"E-E-A-T score\" is selling weather reports as weather control.</p>"
             "<p>Why bother, then? Because it's the best public documentation of what \"credible\" means to the systems deciding your visibility — including, increasingly, the AI ones.</p>"),
            ("The four letters, translated into agent assets",
             "<ul><li><b>Experience — you've actually done this.</b> Closed-transaction references in your content (\"in the 40+ Scottsdale sales I've handled...\"), real photos of you working, client stories with specifics. First-hand experience is exactly what separates your neighborhood page from a portal's template.</li>"
             "<li><b>Expertise — you know the domain.</b> Market analysis with real numbers, direct answers to buyer/seller questions, content that teaches rather than advertises. Credentials help; demonstrated knowledge helps more.</li>"
             "<li><b>Authoritativeness — others say so.</b> Mentions in local press, community sites and directories, consistent profiles that agree with each other, links from real local organizations. You claim; third parties confirm.</li>"
             "<li><b>Trust — the load-bearing letter.</b> Google calls trust the most important member of the family: reviews and responses, accurate NAP everywhere, HTTPS, a real about page, honest content (see our <a href='california-ai-listing-photo-law.html'>AB 723 coverage</a> for where disclosure law is heading). Weak trust nullifies the other three.</li></ul>"),
            ("Why AI assistants care about the same things",
             "<p>LLM-based systems deciding \"which agent should I recommend?\" don't read the Rater Guidelines — but they proxy the same constructs: corroboration across independent sources (authoritativeness), specificity and first-hand detail (experience/expertise), and review-backed consistency (trust). That overlap is convenient: <b>one asset-building program serves both Google and the answer engines.</b> It's the premise our whole <a href='../services/ai-citations.html'>citation service</a> is built on — and you can start the same program yourself with a worked profile, evidence-rich neighborhood pages, systematic reviews, and a handful of genuine local mentions.</p>"),
        ],
        "faqs": [
            ("Is E-E-A-T a Google ranking factor?",
             "Not directly — Google has been explicit that E-E-A-T itself isn't an algorithm input or score. It's the rubric human quality raters apply, which informs how ranking systems are built and evaluated. The practical move is building the underlying signals (experience proof, expertise content, third-party corroboration, trust markers), not chasing a mythical score."),
            ("What's the fastest E-E-A-T win for a real estate agent?",
             "Trust signals: a complete, accurate, consistent presence — reviews with responses, identical business facts across your site and profiles, HTTPS, and a real about page with your license info. Trust is the component Google's guidelines weight most, and it's mostly housekeeping."),
            ("Does E-E-A-T apply to my blog posts too?",
             "Yes — arguably most there. Real estate content touches major financial decisions (what raters call \"Your Money or Your Life\" topics), which get the strictest credibility scrutiny. First-hand experience, named authorship, and honest sourcing in your content matter more in this industry than almost any other."),
        ],
    },
    {
        "slug": "real-estate-ai-search-statistics",
        "img": "img/real-estate-ai-search-statistics.jpg",
        "img_alt": "Illustration of a rising bar chart made of small glowing houses beside an AI chat bubble",
        "cat": "ai",
        "title": "Real Estate AI Search Statistics for 2026: Only the Verified Numbers",
        "date": "2026-07-20",
        "excerpt": "We fact-checked 120 claims about AI search against their primary sources. 24 survived. Here's every verified stat that matters to realtors — plus the popular ones that didn't check out.",
        "tldr": "The verified picture of AI search for realtors in 2026: consumer use of AI for local business recommendations jumped from 6% to 45% in one year (BrightLocal, n=1,002), and 42% now trust AI recommendations as much as reviews. When a Google AI Overview appears, clicks on traditional results roughly halve (Pew: 8% vs 15%) and the top organic result loses ~58% of its CTR (Ahrefs, 300K keywords) — but brands cited inside the AI answer get about 120% more clicks than brands that aren't (Seer Interactive). The twist: real estate is currently among the least AIO-affected industries (<3% of tracked keywords, Semrush) — while the \"X vs Y\" and question-style queries where agents get recommended trigger AI answers up to 95% of the time. Agents are adopting fast: 69% of Realtors use AI at least monthly (NAR, 2025) and 97% of brokerage leaders say their agents use AI (Delta Media, 2026). Every number below links to its primary source.",
        "sections": [
            ("Why this roundup is different",
             "<p>AI-search statistics get laundered: a vendor survey becomes a blog stat, the blog stat gets rounded up, and three reposts later nobody can find the study. So we ran every claim we could find through adversarial verification — 120 claims extracted from 24 sources, each checked against its primary source by independent review passes. <b>24 survived.</b> This post contains only those, each linked to the original publisher, with sample sizes and caveats attached. At the bottom: the popular claims that failed, because knowing what's false is half the value.</p>"),
            ("Consumers now ask AI for local recommendations",
             "<ul>"
             "<li><b>45% of US consumers</b> used AI tools for local business recommendations in the past year — up from <b>6% the year before</b>. That makes AI the third most popular recommendation source, behind only Google and Facebook. (<a href='https://www.brightlocal.com/research/local-consumer-review-survey/' rel='nofollow'>BrightLocal Local Consumer Review Survey 2026</a>, 1,002 US adults)</li>"
             "<li><b>ChatGPT leads at 31%</b> of consumers using it for local business recommendations, followed by Google's AI Mode at <b>23%</b>, then Gemini. (<a href='https://www.brightlocal.com/research/lcrs-ai-trust/' rel='nofollow'>BrightLocal, 2026</a>)</li>"
             "<li><b>42% trust AI recommendations as much as traditional reviews</b> — though 97% of AI users at least sometimes double-check AI suggestions against real reviews. Reviews remain the substrate AI trust is built on. (<a href='https://www.brightlocal.com/research/local-consumer-review-survey/' rel='nofollow'>BrightLocal, 2026</a>)</li>"
             "<li><b>36% of US consumers use ChatGPT regularly</b> (unchanged 2025→2026), and <b>70% of searchers say they use Google's AI Overviews</b> to get answers — though only 31% use them \"often\" and 23% ignore them. (<a href='https://www.orbitmedia.com/blog/ai-vs-google/' rel='nofollow'>Orbit Media survey of 1,110 US consumers, 2026</a>)</li>"
             "</ul>"),
            ("What AI Overviews do to clicks",
             "<ul>"
             "<li>In Pew's tracking of <b>68,879 real Google searches</b> by 900 US adults: users clicked a traditional result on just <b>8% of searches with an AI summary vs 15% without</b> — roughly half. Only <b>1%</b> of AI-summary visits produced a click on a source inside the summary, and sessions ended entirely on 26% of AI-summary pages vs 16% of traditional ones. (<a href='https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/' rel='nofollow'>Pew Research Center, 2025</a>)</li>"
             "<li>Across 300,000 keywords, an AI Overview's presence correlates with a <b>58% lower CTR for the #1 organic result</b> (December 2025 data) — worse than the 34.5% reduction measured eight months earlier. The cost of invisibility is growing. (<a href='https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/' rel='nofollow'>Ahrefs, 2026</a>)</li>"
             "<li>The stat that matters most for GEO: when an AI Overview appears, brands <b>cited inside it earn ~120% more clicks</b> per impression than brands that aren't cited; uncited brands saw CTR fall <b>67%</b> over 2025. (<a href='https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update' rel='nofollow'>Seer Interactive: 53 brands, 5.47M queries, 2.43B impressions</a>)</li>"
             "<li>The balancing data: Semrush's same-keyword before/after analysis found zero-click rates actually <b>declined slightly</b> (33.75% → 31.53%) after AI Overviews appeared, and AIO trigger rates swung wildly through 2025 (6.49% → 24.61% → 15.69% of queries). The disruption is real but not apocalyptic — and it's volatile. (<a href='https://www.semrush.com/blog/semrush-ai-overviews-study/' rel='nofollow'>Semrush, 10M+ keywords</a>)</li>"
             "</ul>"
             "<p>Google, for its part, disputes the click-loss framing without publishing counter-data. CEO Sundar Pichai's defense:</p>"
             "<blockquote>\"I think more than any other company, we prioritize sending traffic to the web. No one sends traffic to the web in the way we do.\"<cite>— Sundar Pichai, interview with The Verge's Decoder, May 2025 (via <a href='https://searchengineland.com/sundar-pichai-google-ai-search-future-456098' rel='nofollow'>Search Engine Land</a>)</cite></blockquote>"),
            ("The real estate twist: insulated where it doesn't matter",
             "<p>Here's the number agents will quote at each other: <b>real estate is among the industries least affected by AI Overviews — under 3% of tracked real estate keywords trigger one</b> (vs ~26% for the most-affected category). (<a href='https://www.semrush.com/blog/semrush-ai-overviews-study/' rel='nofollow'>Semrush, Nov 2025</a>)</p>"
             "<p>Before you relax, look at <i>which</i> queries do trigger AI answers: <b>95.4% of \"X vs Y\" comparison queries and 85.9% of question-format queries</b> — versus only ~5–8% of transactional ones. (<a href='https://www.seerinteractive.com/insights/aio-impact-on-google-ctr-2026-update' rel='nofollow'>Seer Interactive, 2026</a>)</p>"
             "<p>Translation: listing searches (\"homes for sale in…\") stay classic — Zillow keeps winning those. But <b>\"best listing agent in [city]\", \"should I sell now or wait\", \"Zillow vs local agent\"</b> — the questions that decide who gets hired — are exactly the query shapes AI answers dominate. The insulation covers the portals' turf, not yours.</p>"),
            ("Meanwhile, agents are adopting AI faster than they're being found by it",
             "<ul>"
             "<li><b>69% of Realtors use AI at least monthly</b> (20% daily, 22% weekly, 27% a few times monthly); 32% haven't used it. <b>58% of surveyed Realtors have used ChatGPT</b> — Gemini (20%) and Copilot (15%) trail far behind. 50% report a positive business impact. (<a href='https://www.nar.realtor/newsroom/realtors-embrace-ai-digital-tools-to-enhance-client-service-nar-survey-finds' rel='nofollow'>NAR 2025 Technology Survey</a>, 1,241 respondents)</li>"
             "<li><b>97% of brokerage leaders say their agents now use AI</b>, up from 80% in 2024; 82% report agents use it for listing descriptions, 74% for content creation. (<a href='https://www.globenewswire.com/news-release/2026/01/29/3228775/0/en/Delta-Media-AI-Survey-Shows-Ubiquitous-AI-Use-Across-Real-Estate-Brokerages.html' rel='nofollow'>Delta Media 2026 survey of 100+ brokerage leaders</a>)</li>"
             "</ul>"
             "<p>Notice what's missing from that list: almost every agent is using AI to <i>produce content</i>; almost none are working on being the agent AI <a href='../services/ai-citations.html'><i>recommends</i></a>. Writing listing descriptions with ChatGPT doesn't make ChatGPT cite you. Those are different games — and the second one is nearly empty.</p>"),
            ("What didn't survive verification (read this before quoting stats)",
             "<ul>"
             "<li><b>Refuted:</b> \"More than half of consumers now start their searches in an AI app.\" This circulates widely; adversarial review found it's a misreading of the underlying survey. Don't repeat it.</li>"
             "<li><b>Unverifiable:</b> buyer-side \"X% of home buyers used AI in their home search\" claims. NAR's 2025 Profile of Home Buyers &amp; Sellers press release contains no AI or online-search statistics at all — claims citing it are dressing. The real data lives in the paid full report; treat any unlinked version skeptically.</li>"
             "<li><b>No executive quotes cleared</b> our sourcing bar except the Pichai quote above. The \"Zillow says AI will replace agents\" genre is vibes, not citations.</li>"
             "</ul>"
             "<p>One honest caveat about this roundup itself: outside Pew (behavioral panel) and NAR (trade association), most consumer-side numbers come from marketing-software vendors studying their own space. All survived verification against their primary publications — but that's why every stat here is attributed by name instead of stated as universal fact. Hold us to the same standard.</p>"),
        ],
        "faqs": [
            ("Are AI Overviews killing real estate SEO?",
             "Not yet — under 3% of tracked real estate keywords trigger an AI Overview (Semrush, Nov 2025), the lowest of any industry. But comparison and question queries — the ones that decide which agent gets hired — trigger AI answers up to 95% of the time (Seer), so the agent-selection layer is exactly where AI visibility matters."),
            ("What percentage of consumers use AI for local business recommendations?",
             "45% of US consumers in the past year, up from 6% the year before, per BrightLocal's 2026 Local Consumer Review Survey of 1,002 US adults — making AI the third most popular local recommendation source after Google and Facebook."),
            ("Do most searches now start in ChatGPT instead of Google?",
             "No — that widely shared claim failed fact-checking (it misreads an Orbit Media survey). What's verified: 36% of US consumers use ChatGPT regularly, and 45% used AI for local business recommendations in the past year. Growing fast, but Google is still the front door."),
            ("What's the single most important stat for realtors in this roundup?",
             "Seer Interactive's citation finding: when an AI answer appears, being cited inside it delivers roughly 120% more clicks than being invisible in it — while uncited brands lost 67% of their CTR. Visibility inside AI answers is the new page one."),
        ],
    },
    {
        "slug": "how-do-new-agents-get-first-clients",
        "img": "img/how-do-new-agents-get-first-clients.jpg",
        "img_alt": "Illustration of a small sprouting house held in an open hand",
        "cat": "questions",
        "title": "How Do New Real Estate Agents Get Their First Clients (With No Sphere)?",
        "date": "2026-07-20",
        "excerpt": "The most-asked question in every agent forum, answered without the 'just tell everyone you know' cop-out — a 90-day plan for agents starting from zero.",
        "tldr": "New agents with no sphere get their first clients by manufacturing visibility instead of waiting for referrals: fully work a free Google Business Profile from day one, host other agents' open houses (the best no-cost buyer-lead source available to a new licensee), answer real questions in local online communities as a helpful local — not a salesperson, and pick one neighborhood to know better than anyone. The first deal usually comes from being findable and available where established agents aren't bothering to show up. What doesn't work from zero: buying leads before you can afford to lose the money, and posting listings-style content to an audience of nobody.",
        "sections": [
            ("The honest version of \"work your sphere\"",
             "<p>Every trainer says \"tell everyone you know.\" Fine — but if you're 24, new in town, or switching careers, your sphere is thin and everyone in it already knows an agent. The real question is how to generate <b>stranger trust</b>, and stranger trust comes from being visible and verifiably competent where people actually look.</p>"
             "<p>That's mostly free in year one: a fully completed <a href='../services/google-business-profile.html'>Google Business Profile</a> (most new agents skip it entirely — instant advantage), a simple site with one genuinely useful neighborhood page, and consistent proof-of-work posting. None of it requires budget. All of it requires weeks of consistency, which is the actual price.</p>"),
            ("The 90-day plan that produces a first deal",
             "<ul>"
             "<li><b>Weeks 1–2:</b> GBP claimed and 100% complete, photos included. Domain in your name. One neighborhood chosen — ideally where you live.</li>"
             "<li><b>Every weekend:</b> host open houses for busy listing agents at your brokerage. Their listing, your buyer conversations. This is the single highest-yield activity available to a new agent, and vets happily hand it off.</li>"
             "<li><b>Weekly:</b> answer real questions — in local Facebook groups, neighborhood forums, and yes, Reddit — as a helpful local who happens to be an agent. Never pitch; be findable when they check who answered.</li>"
             "<li><b>Monthly:</b> publish one real answer on your site (\"what $450k buys in [neighborhood] right now\"). Twelve months later that's a citable library; most agents never write one.</li>"
             "</ul>"),
            ("What to skip in year one",
             "<p>Skip bought leads until you can afford to lose the spend — portal leads punish slow, part-time follow-up, and new agents convert them worst. Skip paid social until there's something to retarget. Skip the $3,000 branding package; nobody hires a new agent for their logo.</p>"
             "<p>And know why the free path works: every open-house visitor, group answer, and neighbor conversation ends the same way — <b>they Google you</b>. The profile, reviews, and answers you built are what turn contact into a client. Visibility isn't a marketing channel for new agents; it's the conversion layer under every channel. (Our <a href='../audiences/solo-agents.html'>solo-agent plan</a> exists to build exactly that.)</p>"),
        ],
        "faqs": [
            ("How long until a brand-new agent gets their first client?",
             "Commonly two to six months with consistent activity — usually via open houses or their first few community connections. Agents who only wait on their sphere take longer; agents who buy leads without follow-up systems often spend more and don't get there faster."),
            ("Should new agents join a team for leads?",
             "It's a legitimate fast path: lower splits in exchange for lead flow and training. Just build your own name assets (profile, domain, content) from day one anyway — they're portable; team leads aren't."),
            ("Is Reddit actually a viable source of clients?",
             "As a place to be genuinely helpful, yes — agents have built real pipelines by answering local questions consistently and letting profile-checkers find a credible online presence. As a place to prospect and drop links, no; communities ban it and it reads as desperate."),
        ],
    },
    {
        "slug": "is-door-knocking-worth-it",
        "img": "img/is-door-knocking-worth-it.jpg",
        "img_alt": "Illustration of a glowing front door with soft concentric ripples radiating from it",
        "cat": "questions",
        "title": "Is Door Knocking Still Worth It for Real Estate Agents?",
        "date": "2026-07-20",
        "excerpt": "The forum debate that never dies. The data-free honest answer: it works for a specific personality in a specific setup — and it converts through your online presence either way.",
        "tldr": "Door knocking still produces listings for agents who genuinely enjoy face-to-face prospecting, work a tight geographic farm repeatedly (not once), and bring something of value to the door — a neighborhood market update beats a business card. It fails for agents who hate it, do it sporadically, or knock cold with nothing to say. The overlooked half of the answer: door knocking's conversion happens later, online — homeowners look you up after you leave, so a thin Google presence quietly kills whatever the conversation started. Knock if it suits you; either way, build the online layer the knock gets checked against.",
        "sections": [
            ("When door knocking genuinely works",
             "<p>The agents who make door knocking pay share a pattern: they pick a farm small enough to cover repeatedly (300–500 doors, not 3,000), they show up quarterly so the third visit isn't a cold one, and they carry something worth opening the door for — a one-page neighborhood market update with real numbers beats any script.</p>"
             "<p>It's a repetition-and-familiarity play, not a conversion event. The yield comes in year one-plus, when \"the agent who keeps bringing the market update\" is who a homeowner thinks of at listing time. If you can't commit to the repetition, the first pass is wasted.</p>"),
            ("When it's a waste of your calendar",
             "<p>If the thought of it drains you, skip it guiltlessly — reluctance reads at the door, and the same hours put into open houses, community answering, or content compound just as well. It also underperforms in security-building-heavy areas, gated communities, and no-solicitation neighborhoods, where the math never had a chance.</p>"),
            ("The part every door-knocking thread misses",
             "<p>What happens after a good doorstep conversation? The homeowner looks you up. If they find a bare profile, three reviews, and no evidence you know their neighborhood, the conversation dies online — you paid the hardest marketing cost (showing up in person) and lost the cheapest conversion (being credible when checked).</p>"
             "<p>So the real answer to \"is door knocking worth it\" is: it's a <b>traffic source</b>, and like every traffic source — ads, open houses, referrals — it converts through your name's online layer. Build the <a href='../services/local-seo.html'>neighborhood page</a> for the farm you knock. The postcard-and-doorstep agents who seem unusually lucky almost always have the strongest Google presence in the farm.</p>"),
        ],
        "faqs": [
            ("What's a realistic door knocking conversion rate?",
             "Practitioners commonly describe roughly one listing-side conversation per few hundred doors on a first pass, improving meaningfully with repeat visits to the same farm. Treat any precise industry-wide percentage skeptically — no rigorous public study exists; consistency and follow-up dominate the outcome."),
            ("What should I actually say at the door?",
             "Lead with value, not a pitch: \"I put together this quarter's market update for the neighborhood — wanted to drop one off.\" Leave it even with non-answers. You're building recognition for the next touch, not closing on the doorstep."),
            ("Is door knocking legal everywhere?",
             "Mostly yes for real estate canvassing, but no-solicitation ordinances, posted signs, and HOA rules vary — check your municipality, honor posted signs, and skip do-not-knock lists. One complaint in a small farm costs more than the farm was worth."),
        ],
    },
    {
        "slug": "are-open-houses-worth-it",
        "img": "img/are-open-houses-worth-it.jpg",
        "img_alt": "Illustration of an open door on a glowing house with a welcoming path of light",
        "cat": "questions",
        "title": "Are Open Houses Worth It — or Free Labor for the Listing Agent?",
        "date": "2026-07-20",
        "excerpt": "Half of agent forums call them dead; the other half built careers on them. Both are right — the difference is whether you work the follow-through.",
        "tldr": "Open houses rarely sell that house — and that was never their real function for the hosting agent. They remain one of the best in-person lead sources in real estate: unrepresented buyers walk in pre-sorted by neighborhood and price point, neighbors (future sellers) come to compare, and new agents can host other agents' listings at zero cost. Whether they're 'worth it' is decided entirely by the follow-through: a same-day follow-up, a reason to connect (neighborhood guide, market update), and an online presence that survives the Google check every visitor performs. Hosted and worked, they compound; hosted and hoped on, they're free labor.",
        "sections": [
            ("What an open house actually produces",
             "<p>Selling the listing is the cover story. What the host actually collects: buyers early in their search who don't have an agent yet (they self-selected by showing up in this neighborhood at this price), neighbors quietly benchmarking their own home — which is to say, <b>future listing appointments</b> — and reps at unscripted client conversation that new agents can't get anywhere else.</p>"
             "<p>That's why experienced listing agents hand hosting duty to hungry newer agents so readily: the seller gets showings, the vet gets coverage, and the host gets the most valuable thing in the building — the conversations.</p>"),
            ("Why half the forum says they're dead",
             "<p>Because most hosts do nothing with them. A sign-in sheet that never gets a follow-up, no reason for a visitor to remember the host, and — the silent killer — a host whose name returns nothing credible when a visitor Googles them that evening. Every open house visitor checks; if the check comes up thin, the open house really was free labor.</p>"
             "<p>The \"open houses are dead\" agents are usually describing their follow-through, not the format.</p>"),
            ("The system that makes them compound",
             "<p>Before: promote it (a well-run open house is also content — neighbors see the marketing). During: conversations over sign-in bureaucracy; offer a neighborhood guide, not a business card. After: same-day follow-up with the thing you promised, and add every genuine conversation to a simple nurture rhythm.</p>"
             "<p>And underneath all of it: the online layer. The host with a strong profile, <a href='../services/reviews.html'>real reviews</a>, and a <a href='../services/local-seo.html'>page about <i>that neighborhood</i></a> converts the same foot traffic at a multiple of the host without them. Open houses aren't dead — unGoogleable hosts are.</p>"),
        ],
        "faqs": [
            ("How many open houses should a new agent host?",
             "As many as busy listing agents will give you — weekly if possible. It's the highest-yield no-cost activity in a new agent's calendar, and repetition in one neighborhood builds the local-expert effect faster than anything except living there."),
            ("Do open houses still matter now that buyers start online?",
             "More, not less: by the time someone attends, they've done the online sorting and are physically standing in their target neighborhood and budget. The internet made open house foot traffic *more* qualified, not less."),
            ("Should I ask visitors if they're working with an agent?",
             "Yes, early, casually, and honestly — it's both ethics and efficiency. Represented buyers get great hosting and no pursuit; unrepresented ones get a genuine conversation. Reputation in a farm is built on how you treat both."),
        ],
    },
    {
        "slug": "is-cold-calling-dead-for-realtors",
        "img": "img/is-cold-calling-dead-for-realtors.jpg",
        "img_alt": "Illustration of a vintage telephone handset glowing warmly against a dark field of dots",
        "cat": "questions",
        "title": "Is Cold Calling Dead for Real Estate Agents?",
        "date": "2026-07-20",
        "excerpt": "Answer rates keep falling, regulations keep tightening, and a stubborn minority keeps listing homes off the phone. Here's the honest reconciliation.",
        "tldr": "Cold calling isn't dead, but it has become a specialist's channel: it still books listing appointments for agents with high call volume tolerance, tight compliance (DNC registry, state telemarketing rules, TCPA), and disciplined targeting — mainly expireds, FSBOs, and circle prospecting around real events. For everyone else, plummeting answer rates for unknown numbers and rising spam-labeling make it the most expensive hour in the calendar. The half nobody says out loud: connected calls convert through the callback check — the prospect who Googles you mid-conversation. Warm visibility (being recognizable before you dial) is why the same script books for one agent and burns for another.",
        "sections": [
            ("The case that it still works",
             "<p>Phones still get answered by exactly the people agents most want: homeowners in transition. Expired listings and FSBOs have a known, current reason to talk about selling, and circle prospecting around a genuine event (\"the house on your street just closed over asking\") gives a cold dial a warm pretext. Agents who work these lists daily, at volume, with real skill, still trace listings directly to the phone.</p>"
             "<p>Note what all of that shares: a <i>reason for the call</i>. The pure-cold \"thinking of selling?\" dial into a random farm is the version that's mostly dead.</p>"),
            ("The case that it's dying",
             "<p>Unknown-number answer rates have collapsed as carriers auto-label suspected spam, and the compliance surface keeps growing — the federal Do-Not-Call registry, state-level telemarketing rules, and TCPA exposure around auto-dialers are real liabilities, not paperwork. The hours-to-appointment math that worked a decade ago now only pencils for high-volume specialists.</p>"
             "<p>If calling drains you, the same hours in open houses, community answering, or content produce with none of the regulatory risk. Forcing dread into your calendar five mornings a week is how agents quit the business.</p>"),
            ("The variable the debate ignores",
             "<p>Watch what a prospect does during a decent cold call: they put you on speaker and Google you. Mid-call. The agent with <a href='../services/reviews.html'>reviews</a>, a real site, and a page about the prospect's own neighborhood survives that check; the invisible agent gets the polite brush-off — same script, same list.</p>"
             "<p>So the honest verdict: cold calling is a personality-fit specialist channel that, like every outreach channel, converts through your owned visibility. If you love the phone, work expireds with clean compliance and a strong online layer. If you don't, nothing about 2026 says you have to.</p>"),
        ],
        "faqs": [
            ("Do I have to check the Do-Not-Call registry as a realtor?",
             "Yes — commercial cold calls to numbers on the federal DNC registry carry real penalties, with narrow exceptions (like established business relationships), plus state rules that are often stricter. Scrub lists, keep records, and get compliance guidance from your broker before dialing at volume."),
            ("What's the best list for real estate cold calling?",
             "Expired listings, by a wide margin — a homeowner with a current, failed attempt to sell and a decision to make. FSBOs are second. Both are also the most-called lists in the industry, so differentiation and speed matter more than script polish."),
            ("What should I do instead of cold calling if I hate it?",
             "Pick channels with the same intent quality and no dread: open houses (in-person buyer flow), systematic reviews and neighborhood content (inbound seller trust), and genuinely answering questions where your market gathers. Consistency in a channel you'll actually sustain beats sporadic effort in the 'optimal' one."),
        ],
    },
    {
        "slug": "do-real-estate-postcards-work",
        "img": "img/do-real-estate-postcards-work.jpg",
        "img_alt": "Illustration of a stack of postcards with one glowing card lifting off toward a house",
        "cat": "questions",
        "title": "Do Real Estate Postcards and Mailers Still Work in 2026?",
        "date": "2026-07-20",
        "excerpt": "Every agent forum has the thread: 'thousands spent on postcards, zero calls.' And yet farms keep getting taken with mail. What separates the two outcomes.",
        "tldr": "Postcards still work as a familiarity engine — and almost never as a response engine. Direct response from generic 'Just Listed' cards is famously near-zero; what mail does well is make one agent's name feel inevitable in one neighborhood through relentless, useful repetition (market updates with real numbers beat glamour shots of the agent). The economics only close on a tight farm mailed consistently for a year-plus, and the conversion still happens online: the homeowner who finally decides to sell Googles the name on the card. Mail + thin online presence is the classic 'postcards don't work' story. Mail feeding a strong online layer is how farms actually get taken.",
        "sections": [
            ("Why 'zero calls from 5,000 postcards' is normal",
             "<p>Nobody interrupts dinner to call a postcard. Measured as direct response, real estate mail has always been dismal — the forum horror stories are accurately describing the wrong metric. Mail is a <b>frequency medium</b>: its job is that when a homeowner in your farm reaches the selling moment, your name is the one that feels familiar and local.</p>"
             "<p>That takes a year of consistent presence, which is why the one-and-done spring blast \"proves postcards don't work\" every single spring.</p>"),
            ("The mail that earns the fridge",
             "<p>The glamour headshot with \"#1 Agent\" goes straight to recycling. What survives: a quarterly one-pager of <i>that neighborhood's</i> actual numbers — what sold, for how much, days on market, what it means. Homeowners keep market intelligence about their own street; it's the same content as a <a href='../services/local-seo.html'>neighborhood page</a>, printed.</p>"
             "<p>Which is the efficient secret: one well-built neighborhood update is a mailer, a web page, a social post, and an open-house handout. Agents who farm well don't create four things; they create one thing four ways.</p>"),
            ("The Google check decides the ROI",
             "<p>Follow the fate of a good mailer: months of repetition, the owner decides to explore selling, picks your card off the fridge — and Googles you. Strong profile, <a href='../services/reviews.html'>neighborhood-specific reviews</a>, a page about their community: the mail spend just converted. Thin presence: they interview the agent Google recommended instead, and your postcards funded a competitor's closing.</p>"
             "<p>So: yes, mail still works — as the offline arm of a neighborhood-ownership system. As a standalone tactic, the forums are right about it.</p>"),
        ],
        "faqs": [
            ("What response rate should I expect from real estate postcards?",
             "Measured as direct calls, well under one percent — often effectively zero — and that's normal. Measure instead by farm outcomes over 12+ months: listing appointments in the farm, brand recall at the door, and branded-search upticks after drops."),
            ("How big should a mailing farm be?",
             "Small enough to mail at least quarterly without flinching at the invoice — for most solo agents that's 300–800 homes. A small farm touched eight times beats a big farm touched twice, every time."),
            ("Are postcards better than digital ads for farming?",
             "They do different jobs: mail owns the physical neighborhood moment (nobody's inbox filters the fridge), digital owns the research moment. The strongest farms run both pointed at the same neighborhood page — and let the online layer do the converting either way."),
        ],
    },
    {
        "slug": "facebook-ads-vs-google-lsa-for-realtors",
        "img": "img/facebook-ads-vs-google-lsa-for-realtors.jpg",
        "img_alt": "Illustration of a megaphone on one side and a search bar with a verified badge on the other, house between them",
        "cat": "strategy",
        "title": "Facebook Ads vs. Google Local Services Ads for Realtors: Which Should You Run?",
        "date": "2026-07-20",
        "excerpt": "One captures people searching for an agent right now; the other creates demand you'll nurture for months. The honest comparison, including Meta's housing-ad handcuffs.",
        "tldr": "Facebook ads and Google Local Services Ads do different jobs. LSAs capture existing intent: they sit above all other results with a \"Google Screened\" badge, you pay per lead (not per click), and rank is driven by phone responsiveness, reviews, and proximity — high-intent but lower volume, and only worth it if you reliably answer your phone. Facebook/Instagram ads create demand: cheap reach and strong listing promotion, but housing ads run under Meta's Special Ad Category, which strips age, ZIP, and most interest targeting — so leads skew early-stage and need months of nurture. For most agents: LSAs first for bottom-funnel leads, Facebook for listings and long-game awareness — and both convert better when your profile, reviews, and website give leads something credible to find.",
        "sections": [
            ("Two ads, two completely different jobs",
             "<p>The comparison confuses agents because these products don't compete for the same moment. A Local Services Ad meets someone typing \"real estate agent near me\" — the decision is already in motion; the ad just decides who gets the call. A Facebook ad interrupts someone scrolling who wasn't thinking about real estate at all — it plants a seed that might sprout in six months.</p>"
             "<p>So the real question isn't \"which is better.\" It's \"which moment am I paying for, and do I have the system that moment requires?\" Intent capture requires answering the phone. Demand creation requires nurture. Neither works without its system.</p>"),
            ("Google LSAs for realtors: pay-per-lead, with strings",
             "<p>Real estate agents are an eligible \"Google Screened\" category: pass license verification and a background check, keep your <a href='../services/google-business-profile.html'>Google Business Profile</a> in good standing, and your ad can sit above everything else on the page — you pay only when someone actually contacts you, and you can dispute clearly-invalid leads for credit.</p>"
             "<ul><li><b>Ranking isn't bought, it's earned:</b> responsiveness is the biggest factor — missed calls tank you — followed by review score and count, then proximity. Budget matters least.</li>"
             "<li><b>No keyword control:</b> Google decides what matches; the lead lands on a Google-hosted profile, not your website.</li>"
             "<li><b>The economics only work if you answer:</b> per-lead costs vary widely by market (commonly tens of dollars per lead in real estate; check your market), and an unanswered call is money burned plus a ranking penalty in one.</li></ul>"
             "<p>LSAs quietly reward the same things organic local search rewards: reviews and reliability. An agent with 150 specific reviews wins the LSA box <i>and</i> the map pack with one asset.</p>"),
            ("Facebook ads: reach, with housing-rule handcuffs",
             "<p>Here's what most \"Facebook ads for realtors\" content skips: housing ads run under Meta's <b>Special Ad Category</b>, which removes age, gender, and ZIP-code targeting and most interest/behavior narrowing, and widens location radii. The hyper-targeted campaigns agents imagine are largely not allowed to exist.</p>"
             "<p>What still works within the rules: promoting listings with strong video (the listing itself is the targeting — people who care, engage), open-house and just-sold campaigns in a broad radius, retargeting people who visited your website or engaged with your page, and lead forms for valuation or buyer guides. The catch is stage, not volume: Facebook leads are cheap and plentiful and mostly 6–18 months from transacting. Without a real follow-up system, you're buying a list you'll never work.</p>"),
            ("The verdict: sequence them, and aim both at what you own",
             "<p><b>Run LSAs first</b> if your market has them and you (or someone) reliably answers the phone — they're the closest thing to buying bottom-of-funnel agent-intent, and the setup cost is mostly reviews you should be building anyway. <b>Add Facebook</b> when you have listings to promote and a nurture system (CRM, drip, actual follow-up) to justify early-stage leads. Compare them on cost per <i>closing</i> over six months, never cost per lead — the metric each platform shows you is the one that flatters it.</p>"
             "<p>And remember what happens after either ad works: the lead Googles you. Ads rent the introduction; your profile, reviews, website, and <a href='../services/ai-citations.html'>AI citations</a> decide whether the introduction converts. That owned layer makes every ad dollar work harder — which is why we build it first.</p>"),
        ],
        "faqs": [
            ("Are real estate agents eligible for Google Local Services Ads?",
             "Yes — real estate agents are an eligible professional-services category with the \"Google Screened\" badge, subject to license verification and background checks, with availability varying by market. Check current eligibility for your area at Google's LSA signup."),
            ("Why can't I target my Facebook real estate ads by ZIP code or age?",
             "Housing ads fall under Meta's Special Ad Category (a result of fair-housing enforcement), which removes age, gender, and ZIP targeting and most detailed audience options. It applies to every agent equally — creative and offer, not micro-targeting, are where housing campaigns are won."),
            ("Which is cheaper — Facebook leads or LSA leads?",
             "Facebook leads usually cost far less per lead; LSA leads cost more but arrive with intent. Measured per closing, LSAs often win for solo agents without nurture infrastructure, while Facebook can win for teams with strong follow-up systems. Your answer is in your own six-month math, not a benchmark."),
            ("Should I just do both?",
             "If budget allows and your phone coverage and nurture systems are real, yes — they cover different funnel stages. On a limited budget, pick the one whose system you can actually run today, and put the difference into owned assets (reviews, profile, website) that make both ads convert better later."),
        ],
    },
    {
        "slug": "best-real-estate-website-design-companies",
        "img": "img/best-real-estate-website-design-companies.jpg",
        "img_alt": "Illustration of a row of glowing browser windows, each framing a different house design",
        "cat": "websites",
        "title": "The Best Real Estate Website Design Companies in 2026 (an Honest Comparison)",
        "date": "2026-07-20",
        "excerpt": "Luxury Presence, Agent Image, AgentFire, Sierra Interactive, Real Geeks — and yes, us. Who's actually best for which agent, judged on the questions that matter.",
        "tldr": "The best real estate website company depends on what you're optimizing for. Luxury Presence leads on high-end custom design inside a full SaaS platform (pricing unpublished; third-party reviews report roughly $300–$1,500/month plus setup). Agent Image builds custom WordPress sites you own. AgentFire is the value pick for hyperlocal sites (from about $129/month). Sierra Interactive suits SEO-focused teams wanting IDX + CRM (~$500+/month). Real Geeks is the budget all-in-one (~$299/month). CitedRealty (that's us) builds custom, schema-first sites you own outright, designed to be cited by AI — included with our $3,999/month plan. Decide on two questions first: do you own the site, and can machines read it?",
        "sections": [
            ("How we judged (and our bias, disclosed)",
             "<p>We're on this list, so read us with the same skepticism you'd read anyone ranking themselves. To keep it honest, every company is judged on the same five questions: Is the design actually custom? Do you <b>own</b> the site if you leave? Can search engines and AI systems read it (schema, speed, content architecture)? What does it really cost? And who is it genuinely best for?</p>"
             "<p>Pricing below comes from vendor sites and independent reviews like <a href='https://www.agentadvice.com/luxury-presence-review/' rel='nofollow'>AgentAdvice</a> and <a href='https://www.housingwire.com/articles/best-website-builders-real-estate/' rel='nofollow'>HousingWire</a> as of mid-2026 — always confirm current terms directly.</p>"),
            ("The list",
             "<ul>"
             "<li><b>Luxury Presence — best for luxury branding inside a platform.</b> Genuinely beautiful custom design, IDX, and a full suite (CRM, app, CMAs). Trade-offs: pricing isn't published (reviews report ~$300–$1,500/mo plus $3,500–$5,000 setup), and the site lives on their platform — leave, and you're rebuilding.</li>"
             "<li><b>Agent Image — best custom WordPress you own.</b> Long-running design shop; project-priced builds on the open-source platform, so the site is genuinely yours. You'll assemble SEO/content help separately.</li>"
             "<li><b>AgentFire — best value for hyperlocal sites.</b> From ~$129/mo with no setup fee; strong neighborhood-guide DNA. Lighter on done-for-you marketing.</li>"
             "<li><b>Sierra Interactive — best for SEO-driven teams.</b> IDX + CRM platform (~$500–$700/mo plus setup) with a reputation for search-friendly architecture. Platform lock-in applies.</li>"
             "<li><b>Real Geeks — best budget all-in-one.</b> ~$299/mo for IDX, CRM, valuations, and ad tools. Templated look; you're renting.</li>"
             "<li><b>CitedRealty — best for being found by AI, and for ownership.</b> <a href='../services/website-design.html'>Custom, schema-first sites</a> with neighborhood architecture built in, designed to be the source ChatGPT and AI Overviews cite. Included with our $3,999/mo Local Hero plan (or as a standalone project); you own the site outright. We're new and website design is one piece of our retainer — if you want a website alone with no marketing engine, Agent Image or AgentFire may fit better.</li>"
             "</ul>"),
            ("The two questions that sort the whole market",
             "<p><b>Ownership:</b> platforms (Luxury Presence, Sierra, Real Geeks) rent you a site that vanishes when you churn; builders (Agent Image, CitedRealty) hand you the keys. Renting is fine for speed; just price in the rebuild when you leave.</p>"
             "<p><b>Machine readability:</b> in 2026 your website's biggest audience might be AI systems deciding who to recommend. Ask any vendor: what structured data ships by default? How do neighborhood pages work? Can you show me a site being cited in AI answers? Blank stares are data.</p>"),
        ],
        "faqs": [
            ("What's the best real estate website company for a solo agent on a budget?",
             "AgentFire (from about $129/month) is the strongest value if you'll do your own marketing; Real Geeks if you want IDX + CRM in one bill. If the budget is truly zero, a fully worked Google Business Profile beats a bad cheap website."),
            ("Is Luxury Presence worth the money?",
             "For luxury agents who want premium design and a full platform and accept SaaS economics — often yes; their design work is genuinely strong. Run the math on total cost (reviews report setup plus $300–$1,500/month) versus what a comparable owned site plus marketing retainer would cost."),
            ("Why does owning the website matter?",
             "Rankings and AI citations attach to your domain and its content. If the platform owns the site, your years of accumulated authority reset every time you switch vendors — the equity you built becomes their retention tool."),
        ],
    },
    {
        "slug": "luxury-presence-alternatives",
        "img": "img/luxury-presence-alternatives.jpg",
        "img_alt": "Illustration of one large glowing doorway with several smaller distinct doorways beside it",
        "cat": "websites",
        "title": "Luxury Presence Alternatives in 2026: What Agents Should Actually Compare",
        "date": "2026-07-20",
        "excerpt": "Luxury Presence is good at what it does. Here's why agents still shop around — and the right alternative for each reason, compared fairly.",
        "tldr": "Agents look for Luxury Presence alternatives for four main reasons: unpublished pricing that reviews put around $300–$1,500/month plus $3,500–$5,000 setup; platform lock-in (the site isn't yours if you leave); paying for a full suite when they need only a website; or wanting marketing outcomes, not just software. Match the alternative to your reason: Agent Image for a custom WordPress site you own; AgentFire for affordable hyperlocal sites; Sierra Interactive for SEO-focused team platforms; Real Geeks for budget all-in-one; CitedRealty (us — disclosed bias) for an owned, AI-citable site inside a full marketing retainer with public pricing.",
        "sections": [
            ("First, the fair version: what Luxury Presence does well",
             "<p>Credit where due: Luxury Presence builds some of the best-looking agent websites in the industry, serves 20,000+ real estate businesses, and has genuine luxury-market credibility with major brokerage partnerships. If you want premium design inside one integrated platform and the economics work for you, it's a rational choice.</p>"
             "<p>An alternatives search usually isn't about quality — it's about fit. Four specific fits, below.</p>"),
            ("The four reasons agents shop around",
             "<ul>"
             "<li><b>Price opacity.</b> Pricing requires a sales call; independent reviews (<a href='https://www.agentadvice.com/luxury-presence-review/' rel='nofollow'>AgentAdvice</a>, mid-2026) report roughly $300–$1,500/month plus $3,500–$5,000 setup — real money that deserves a public number.</li>"
             "<li><b>You don't own the site.</b> It's SaaS: churn and the design, pages, and accumulated search equity stay behind.</li>"
             "<li><b>Suite overlap.</b> CRM, app, CMAs are impressive — and redundant if you already run Follow Up Boss and love it.</li>"
             "<li><b>Software ≠ outcomes.</b> A beautiful site doesn't market itself; some agents want the work done, not better tools to do it with.</li>"
             "</ul>"),
            ("Match the alternative to your reason",
             "<ul>"
             "<li><b>Want to own it:</b> Agent Image (custom WordPress, project-priced) — or CitedRealty, where the <a href='../services/website-design.html'>custom build</a> is included with our $3,999/mo plan and the site is yours outright.</li>"
             "<li><b>Want hyperlocal on a budget:</b> AgentFire, from ~$129/mo with real neighborhood-guide tooling.</li>"
             "<li><b>Want an SEO/lead platform for a team:</b> Sierra Interactive (~$500+/mo) — still rented, but strong architecture.</li>"
             "<li><b>Want cheapest all-in-one:</b> Real Geeks (~$299/mo).</li>"
             "<li><b>Want the marketing done, with AI visibility as the goal:</b> that's us — website + GBP + local SEO + AI citations + content in one public-priced retainer. Bias disclosed; compare us as skeptically as anyone.</li>"
             "</ul>"),
            ("If you switch: the 30-minute checklist",
             "<p>Before leaving any platform: export your content and blog posts; inventory which pages rank (Search Console → top pages); set up 301 redirects from old URLs on day one; keep your domain registration in <i>your</i> name, always; and re-verify your site in Search Console after migration. Most \"we switched and rankings died\" stories are missing redirects, not vendor magic.</p>"),
        ],
        "faqs": [
            ("Can I keep my website if I leave Luxury Presence?",
             "The design and platform features don't come with you — it's software-as-a-service. Your domain and your written content are yours; plan a rebuild and redirects. This is the single biggest thing to understand before signing with any platform vendor."),
            ("What's the cheapest serious Luxury Presence alternative?",
             "AgentFire's entry tier (around $129/month, per mid-2026 pricing) is the lowest-cost option that still takes local content seriously. Cheaper template builders exist but tend to be invisible to search and AI alike."),
            ("Is a custom site better than a platform site for SEO and AI visibility?",
             "Not automatically — execution decides. But custom builds make it easier to ship the things that matter (schema, fast pages, real neighborhood architecture), and ownership means the authority you build compounds for you instead of resetting when you change vendors."),
        ],
    },
    {
        "slug": "real-estate-agent-website-cost",
        "img": "img/real-estate-agent-website-cost.jpg",
        "img_alt": "Illustration of a browser window with a price tag, next to stacked gradient coins",
        "cat": "websites",
        "title": "How Much Does a Real Estate Agent Website Cost in 2026?",
        "date": "2026-07-19",
        "excerpt": "From $10/month templates to $20,000 first years — the four price bands, what actually drives cost, and the question that matters more than price.",
        "tldr": "Real estate agent websites in 2026 fall into four bands: DIY builders ($10–$50/month — cheap, invisible to search); template IDX platforms ($100–$300/month, e.g. Real Geeks or AgentFire's entry tiers); premium platforms ($300–$1,500/month plus $1,000–$5,000 setup, e.g. Sierra Interactive or Luxury Presence, where first-year totals commonly reach $7,000–$23,000); and custom builds you own ($3,000–$15,000+ one-time, e.g. Agent Image, or included in a marketing retainer like CitedRealty's $3,999/month plan). The bigger question than price: are you renting or owning — because rented sites reset your search equity every time you switch.",
        "sections": [
            ("The four price bands",
             "<ul>"
             "<li><b>DIY builders ($10–$50/mo):</b> Squarespace/Wix with an IDX widget. Fine as a business card; effectively invisible to search and AI.</li>"
             "<li><b>Template IDX platforms ($100–$300/mo):</b> Real Geeks (~$299/mo), AgentFire entry tiers (from ~$129/mo). Real functionality, shared templates, rented.</li>"
             "<li><b>Premium platforms ($300–$1,500/mo + setup):</b> Sierra Interactive, Luxury Presence. Custom-designed fronts on SaaS backends; independent reviews put typical Luxury Presence first years at $7,000–$23,000 all-in. Still rented.</li>"
             "<li><b>Custom builds you own ($3,000–$15,000+ once):</b> Agent Image and similar shops, or bundled with marketing (our <a href='../services/website-design.html'>builds</a> are included with Local Hero at $3,999/mo, or standalone projects). Highest upfront, only band where the asset is yours.</li>"
             "</ul>"
             "<p>All figures are mid-2026 market ranges from vendor sites and independent comparisons — confirm current quotes.</p>"),
            ("What actually drives the price",
             "<p>Four things: <b>design depth</b> (template reskin vs. real custom work), <b>IDX/MLS integration</b> (live listing search adds platform costs and compliance work), <b>content architecture</b> (neighborhood pages, guides, and schema are labor — and the part that makes a site findable), and <b>who does the marketing after launch</b>. A site is a printing press; most quotes don't include anyone writing the newspaper.</p>"),
            ("The rent-vs-own math nobody shows you",
             "<p>A $500/month platform costs $18,000 over three years and leaves you with nothing portable. A $9,000 owned build costs half that over the same period and leaves you holding a ranking, cited asset — plus every dollar of authority it accumulated. Platforms win on month one; ownership wins on every month after the first year.</p>"
             "<p>The exception: if you genuinely need a full CRM/app suite and will use it, a platform's bundle can pencil out. Just price the exit before you sign — the rebuild-and-redirect cost is part of the platform's true price.</p>"),
            ("What we charge (since we're arguing everyone should publish pricing)",
             "<p>A custom, schema-first, AI-citable site is included with our $3,999/month Local Hero retainer (which also covers GBP, local SEO, 15 neighborhoods, content, and social guidance), available as a standalone project if you're on the $999 plan. You own the site outright either way. That's the whole answer — no discovery call required to hear a number.</p>"),
        ],
        "faqs": [
            ("Is a $20/month Squarespace site good enough to start?",
             "As a link on your Instagram bio, yes. As a lead source, no — it won't rank for neighborhood searches or get cited by AI without the structure and content those systems need. Start cheap if cash demands it, but know what it's for."),
            ("Why do some real estate websites cost $15,000+?",
             "Genuine custom design, IDX integration, content architecture (neighborhood pages, guides, schema), and copywriting are skilled labor. What you're really buying is an asset engineered to be found — the cost scales with how much finding you want."),
            ("Should the website budget come before or after the marketing budget?",
             "Together. A site nobody markets is a brochure; marketing with no owned destination rents someone else's asset. That's the argument for bundling them — the site and the engine that feeds it are one system."),
        ],
    },
    {
        "slug": "do-realtors-need-their-own-website",
        "img": "img/do-realtors-need-their-own-website.jpg",
        "img_alt": "Illustration of a small house standing on its own glowing foundation apart from a large corporate building",
        "cat": "websites",
        "title": "Do Realtors Actually Need Their Own Website in 2026?",
        "date": "2026-07-19",
        "excerpt": "You have a brokerage page, a Zillow profile, and an Instagram. So does every other agent — and that's exactly the problem. The honest answer, including when you can wait.",
        "tldr": "Yes — but the reason changed. It's no longer about looking professional: in 2026 your website is the home base AI systems cite when they recommend agents. A brokerage subpage can't hold neighborhood pages, schema, or content in your name (and disappears when you switch brokerages); portal profiles build the portal's authority, not yours; social feeds aren't citable sources. Agents who can defer it: brand-new agents who should fully work a free Google Business Profile first. Everyone else needs an owned domain with real local content — it's the one marketing asset that compounds under your control.",
        "sections": [
            ("The old reason is dead; the new reason is bigger",
             "<p>The 2015 argument for an agent website — \"look professional when people Google you\" — is mostly handled by your Google Business Profile now. If that were still the whole story, honest advice would be: skip the website, work the profile.</p>"
             "<p>The 2026 argument is different: when ChatGPT, Gemini, or Google's AI recommends an agent, it cites <b>sources</b>. Your website is where those sources live — the neighborhood expertise, the answered questions, the structured data that tells machines exactly who you are. No owned site, nothing to cite; nothing to cite, someone else gets named.</p>"),
            ("Why the free alternatives don't add up",
             "<ul>"
             "<li><b>Brokerage subpage:</b> can't hold your neighborhood pages or schema, shares its authority across every agent in the office — and evaporates the day you switch brokerages.</li>"
             "<li><b>Zillow/portal profiles:</b> every review and sale you add strengthens the portal's domain, which then sells that attention back to you.</li>"
             "<li><b>Social profiles:</b> essential for trust, nearly useless as citations — AI systems don't source \"who's the best listing agent in town\" from an Instagram grid.</li>"
             "</ul>"
             "<p>Each is a fine <i>satellite</i>. None can be the home base, because none is yours.</p>"),
            ("When you can honestly wait",
             "<p>If you're brand-new and cash-constrained, the right sequence is: fully work your free Google Business Profile first (it's the highest-leverage free asset in local search), systematize reviews from your first closings, and buy the domain for your name today even if it just parks. Add the real site when you can do it properly — a thin template site helps almost nothing and false-signals \"done.\"</p>"),
            ("What 'a real website' means now",
             "<p>Not a digital business card: an owned domain with pages for the neighborhoods you actually work, direct answers to the questions your market asks, RealEstateAgent and FAQ schema underneath, and speed that doesn't fight you. That's the checklist whether you build it yourself, hire a design shop, or run it through a <a href='../services/website-design.html'>retainer like ours</a> — the standard is machine-readable local authority, not prettiness.</p>"),
        ],
        "faqs": [
            ("Isn't my Google Business Profile enough?",
             "It's the right first asset, and for a brand-new agent it can be enough for a while. But a GBP can't hold deep neighborhood content or answer-style pages — the things AI cites — and profiles have limited room to differentiate. The profile gets you found; the website gets you chosen and cited."),
            ("Should my website be separate from my brokerage's site?",
             "Yes, on a domain you register and own. Brokerage-provided pages don't travel with you, and real estate careers average several brokerage moves — your search equity shouldn't reset each time."),
            ("What about just buying leads instead?",
             "Buying leads and building presence aren't substitutes — one is spend, the other is investment. Bought leads stop the day you stop; an owned site with real content keeps producing. Most durable businesses run modest paid spend on top of owned assets, not instead of them."),
        ],
    },
    {
        "slug": "zillow-vs-realtor-com-vs-homes-com-leads",
        "img": "img/zillow-vs-realtor-com-vs-homes-com-leads.jpg",
        "img_alt": "Illustration of three portal doorways with an agent comparing paths between them",
        "cat": "strategy",
        "title": "Zillow vs. Realtor.com vs. Homes.com Leads: An Honest Comparison",
        "date": "2026-07-18",
        "excerpt": "The three big portals sell agents very different products. Here's how their lead models actually differ — and the question none of them answer.",
        "tldr": "The major portals monetize agents differently: Zillow leans on share-of-voice advertising and, in many markets, success-fee referral models; Realtor.com sells leads and referral-fee connections; Homes.com has pushed an agent-branding angle where your listings stay yours. Costs vary widely by market and change often, so compare current terms directly. The bigger question is structural: all three are rented demand — shared attention, portal-owned relationships, spend that stops producing the day it stops. Portals can supplement a pipeline, but the durable advantage comes from demand you own: your profile, your neighborhoods, your citations.",
        "sections": [
            ("Three portals, three different products",
             "<p>Agents talk about \"portal leads\" as one thing, but the business models differ. Zillow's flagship programs center on visibility — paying for share of buyer attention in chosen ZIP codes — and in many markets a referral-style model where the fee comes out of closed deals. Realtor.com has historically sold both direct leads and referral connections. Homes.com's recent pitch is agent branding: your listing, your lead, your brand.</p>"
             "<p>Terms, availability, and pricing change frequently and vary by market — treat any specific numbers you read (including in AI answers) as stale until you've confirmed them in a current quote for your ZIP codes.</p>"),
            ("How to actually compare them",
             "<ul><li><b>Effective cost per closing</b> — not per lead. Model conversion honestly; shared or referred leads convert differently than exclusive ones.</li>"
             "<li><b>Exclusivity</b> — is the inquiry yours alone, or are you in a race?</li>"
             "<li><b>Who owns the relationship</b> — some models keep the consumer inside the portal's funnel and hand you a transaction, not a client.</li>"
             "<li><b>Follow-up burden</b> — speed-to-lead contests have a real staffing cost.</li>"
             "<li><b>Exit value</b> — what do you keep if you cancel next quarter? Usually: nothing.</li></ul>"),
            ("The question none of them answer",
             "<p>Every portal comparison quietly assumes the demand must be rented from someone. But the fastest-growing surface — AI assistants answering \"who should I work with?\" — doesn't belong to any portal, and it names individual agents, not marketplaces.</p>"
             "<p>That's the arbitrage this decade: while competitors argue over which rent is cheapest, the agents building <a href='../services/ai-citations.html'>owned visibility</a> (profiles, neighborhood authority, reviews, citations) are being handed the client before the portals see the search.</p>"),
            ("A practical verdict",
             "<p>If a portal program is profitably closing deals for you today at current terms, keep it — profitable rent is still profit. Cap it at a level that doesn't crowd out investment in owned assets, and re-run the cost-per-closing math quarterly as terms change.</p>"
             "<p>If you're choosing between them fresh: get current quotes for your market, weight exclusivity and relationship ownership over raw lead volume, and treat every portal dollar as bridge financing while your owned engine matures.</p>"),
        ],
        "faqs": [
            ("Which portal has the best lead quality?",
             "It varies by market, price point, and program — and changes as portals adjust their models. The consistent pattern isn't which portal wins; it's that exclusive, relationship-owning channels (including your own) convert better than shared-inquiry channels."),
            ("Are portal referral-fee models better than paying per lead?",
             "They shift risk: you pay only on closings, but the fee is typically a meaningful slice of your commission, and the portal owns even more of the relationship. Good for cash flow, expensive at scale — do the math on your actual volume."),
            ("Can I just use all three portals?",
             "You can, but stacking rented channels multiplies cost without compounding. Most agents get further running one profitable portal channel plus a serious owned program than spreading budget across all three."),
        ],
    },
    {
        "slug": "zillow-premier-agent-vs-local-seo",
        "img": "img/zillow-premier-agent-vs-local-seo.jpg",
        "img_alt": "Illustration of a crossroads sign pointing toward a billboard one way and a glowing neighborhood the other",
        "cat": "strategy",
        "title": "Zillow Premier Agent vs. Local SEO + AI Citations: Where Should Your Budget Go?",
        "date": "2026-07-17",
        "excerpt": "One buys placement, the other builds an asset. A fair breakdown of speed, cost curves, and compounding — and when each one wins.",
        "tldr": "Zillow Premier Agent buys immediate visibility next to listings — fast to start, easy to scale, but shared attention with costs that recur forever and nothing kept when you stop. Local SEO plus AI citations builds owned visibility — slower to start (weeks to months), but exclusive, compounding, and increasingly the source AI assistants use when recommending agents. Speed favors Premier Agent; economics over time favor owned. The honest answer for many agents is a phased split: enough portal spend to keep deals flowing now, with a growing share invested in the owned assets that permanently lower acquisition cost.",
        "sections": [
            ("What each dollar actually buys",
             "<p>A Premier Agent dollar buys impressions and inquiries in your chosen ZIPs, at whatever the current auction-style market rate is. It works immediately and stops immediately. A <a href='../services/local-seo.html'>local SEO / GEO</a> dollar buys work product: profile optimization, neighborhood pages, schema, reviews, content — assets that keep producing after the invoice.</p>"
             "<p>Neither is wrong. They're different financial instruments: one is operating expense, the other is capital investment.</p>"),
            ("Speed vs. slope",
             "<p>Premier Agent wins the first 90 days — there's no organic program that outruns paid placement in month one. Owned visibility wins the slope: rankings, citations, and AI mentions accumulate, so year two costs less per closing than year one, and year three less again.</p>"
             "<p>The mistake is judging both on the same clock. Paid should be judged monthly; owned should be judged on the trend of cost per closing across quarters.</p>"),
            ("The AI layer changes the comparison",
             "<p>When buyers and sellers ask AI assistants who to work with, the answers cite profiles, reviews, local content, and independent mentions — the exact outputs of an owned program. Portal ad placements don't feed those answers.</p>"
             "<p>This tilts the long game further toward owned: the same work that ranks you in the map pack is building your presence in the answer layer portals can't buy into.</p>"),
            ("When each one wins",
             "<ul><li><b>Premier Agent (or similar) makes sense:</b> new market entry, immediate cash-flow needs, team seats to feed while owned assets mature.</li>"
             "<li><b>Owned (SEO + GEO) makes sense:</b> defined farm areas, listing-side focus, any agent planning to be in the same market in three years.</li>"
             "<li><b>The usual right answer:</b> a phased split — start owned on day one (the clock only starts when you do), keep paid only where it's provably profitable, shift the ratio quarterly.</li></ul>"),
        ],
        "faqs": [
            ("How long before local SEO + AI citations replace portal spend?",
             "Foundations move in weeks; consistent AI mentions and durable rankings typically build over months, with the crossover on cost per closing commonly inside the first year for territory-focused agents. It depends on market competitiveness and starting point — anyone quoting an exact universal timeline is guessing."),
            ("Is Premier Agent worth it in competitive ZIPs?",
             "Only your math can say: current cost in your ZIP, your realistic conversion, your average commission. In hyper-competitive ZIPs the auction dynamics often push cost per closing above what a serious owned program runs monthly — which is exactly the comparison worth making."),
            ("Can I do both on a small budget?",
             "Yes — that's the phased split. Even a minimal owned program (worked profile, five neighborhood pages, systematic reviews) starts the compounding clock while a small paid budget keeps near-term deals moving."),
        ],
    },
    {
        "slug": "how-much-should-realtors-spend-on-marketing",
        "img": "img/how-much-should-realtors-spend-on-marketing.jpg",
        "img_alt": "Illustration of a house-shaped piggy bank with gradient coins arranged into a rising chart",
        "cat": "strategy",
        "title": "How Much Should Realtors Spend on Marketing in 2026?",
        "date": "2026-07-16",
        "excerpt": "The old 10%-of-GCI rule still works as a starting point — what's changed is where the dollars should go. A budget framework for agents and teams.",
        "tldr": "A useful starting point is the long-standing rule of thumb of roughly 10% of gross commission income on marketing — newer agents building visibility often need more, established referral-heavy agents can run leaner. What matters more in 2026 is allocation: split spend between owned assets (profile, neighborhood pages, content, reviews, AI citations — investments that compound) and rented reach (portal placements, ads — costs that stop producing when they stop). Most agents are over-indexed on rent. A healthy trajectory shifts toward owned every quarter and judges everything on cost per closing, not cost per lead.",
        "sections": [
            ("Start with the rule of thumb, then adjust",
             "<p>The traditional guidance — around a tenth of your gross commission income — remains a sane anchor because marketing spend should scale with production, not with anxiety. Newer agents typically need to spend above the anchor (visibility is being built from zero); veterans with deep referral networks can sit below it.</p>"
             "<p>Whatever the number, make it a deliberate line item. The most common agent budgeting failure isn't overspending — it's reactive spending: a portal invoice here, a boosted post there, no system anywhere.</p>"),
            ("The split that matters: owned vs. rented",
             "<ul><li><b>Owned (build):</b> your website and neighborhood pages, Google Business Profile work, content, reviews, <a href='../services/ai-citations.html'>AI citation building</a>. Compounds; survives budget cuts.</li>"
             "<li><b>Rented (buy):</b> portal placements, PPC, social ads. Immediate; evaporates.</li></ul>"
             "<p>There's no universal correct ratio, but the trajectory should move toward owned as assets mature — many established agents end up majority-owned within a couple of years and keep a tactical rented layer for launches and gaps.</p>"),
            ("What a serious owned program costs",
             "<p>For context, done-for-you owned programs in real estate typically run from around $1,000/month for a solo-agent foundation (profile, a handful of neighborhoods, content) to $4,000–$7,000/month for <a href='../audiences/teams.html'>team- and brokerage-scale coverage</a> with social and strategy included. That's comparable to what many agents already hand portals — with a completely different trajectory. (Our own plans run $999–$6,999, priced on exactly this logic.)</p>"),
            ("Judge everything on cost per closing",
             "<p>Cost per lead is the metric platforms sell; cost per closing is the metric your P&L feels. Track each channel's spend against closings it actually produced, quarterly. Kill or cap what can't prove itself; feed what compounds.</p>"
             "<p>And log the trend line, not just the level: rented channels drift more expensive as competition bids up; owned channels drift cheaper as assets accumulate. The budget follows the slopes.</p>"),
        ],
        "faqs": [
            ("Should new agents spend on marketing before their first closings?",
             "Modestly, yes — the owned clock (profile, neighborhood presence, reviews) should start immediately because it takes months to mature. Keep it lean and start with free-but-effortful assets: a fully worked Google Business Profile costs time, not money."),
            ("Does time count as marketing budget?",
             "Effectively yes. DIY-ing social, content, and profile work is spending your hours instead of dollars. Price your hour honestly against what delegating costs — many agents discover their 'free' marketing is their most expensive."),
            ("How often should I rebalance the budget?",
             "Quarterly. It's slow enough for owned assets to show their trend and fast enough to stop a rented channel that's drifted unprofitable."),
        ],
    },
    {
        "slug": "best-seller-lead-sources-for-listing-agents",
        "img": "img/best-seller-lead-sources-for-listing-agents.jpg",
        "img_alt": "Illustration of a podium of glowing houses ranked first through third",
        "cat": "seller-leads",
        "title": "The Best Seller Lead Sources for Listing Agents, Ranked",
        "date": "2026-07-15",
        "excerpt": "Every listing-side lead source, ranked by exclusivity, cost curve, and compounding — from past-client referrals to AI recommendations to bought lists.",
        "tldr": "Ranked by long-run value for listing agents: (1) past clients and sphere — highest conversion, near-zero cost, but capped by network size; (2) owned local visibility — Google Business Profile, neighborhood pages, reviews, and AI citations that make sellers find you pre-sold; (3) strategic open houses and circle prospecting that feed the online engine; (4) portal and paid leads — fast but shared, rented, and increasingly expensive; (5) bought seller lists and cold predictive data — cheap per name, brutal per closing. The pattern: sources where the seller chooses you outperform sources where you chase the seller.",
        "sections": [
            ("The ranking, and the logic behind it",
             "<ul><li><b>1. Past clients &amp; sphere.</b> Nothing converts like someone who already trusts you. The limit isn't quality — it's quantity and timing.</li>"
             "<li><b>2. Owned local visibility.</b> Map pack, neighborhood pages, reviews, AI recommendations: the seller arrives having chosen you. Exclusive, compounding, and the only source that scales without scaling cost.</li>"
             "<li><b>3. Open houses &amp; circle prospecting.</b> Still excellent — when they feed the online engine (every attendee Googles you) instead of standing alone.</li>"
             "<li><b>4. Portal &amp; paid leads.</b> Real closings happen here, but shared inquiries, speed races, and rising costs make it a supplement, not a strategy.</li>"
             "<li><b>5. Bought lists &amp; cold data.</b> Predictive sellers and FSBO/expired lists are cheap per contact and savage per conversion — viable only for agents who genuinely love prospecting volume.</li></ul>"),
            ("Why 'seller chooses you' beats 'you chase seller'",
             "<p>Listing appointments are trust decisions made mostly before the appointment. Sources where the seller initiated contact — a referral, a map-pack call, an AI recommendation — start you as the presumed choice. Sources where you initiated start you as the salesperson.</p>"
             "<p>That's why conversion rates fall in almost exactly the order above, and why cost per listing rises in the reverse order.</p>"),
            ("The multiplier: sources feed each other",
             "<p>These aren't independent channels. Closings feed reviews; reviews feed the profile; the profile and neighborhood pages feed Google and AI; visibility makes circle prospecting warm and open houses convert. The agents who look effortless are running that loop on purpose.</p>"
             "<p>Practical sequence: systematize past-client follow-up first (cheapest wins), build owned visibility second (the compounding layer), then decide whether paid channels still earn a slot.</p>"),
            ("What we'd build first for a listing agent",
             "<p>A worked <a href='../services/google-business-profile.html'>Google Business Profile</a> with a <a href='../services/reviews.html'>post-closing review system</a>, then a real page for each farm neighborhood, then seller-intent content (\"should I sell now\", \"what's my home worth here\") published monthly. That stack targets every moment a future seller researches — and it's the exact evidence AI assistants cite when someone asks who should sell their home — and the spine of our <a href='../audiences/listing-agents.html'>listing-agent program</a>.</p>"),
        ],
        "faqs": [
            ("Are FSBO and expired listings still worth prospecting?",
             "For agents with genuine prospecting stamina, yes — they're motivated sellers with a known address. But they're the most-contacted people in real estate the week they appear, so differentiation (and thick skin) decides results, not scripts."),
            ("Where do home-valuation landing pages rank?",
             "They're a capture tool, not a source — they convert visibility you already have. Attached to real neighborhood authority they work; run as cold ads they mostly harvest curiosity clicks."),
            ("How many seller lead sources should I run at once?",
             "Two or three, properly: sphere systemization, owned visibility, and at most one paid/prospecting channel you'll actually work. Five half-run sources lose to two compounding ones."),
        ],
    },
    {
        "slug": "how-realtors-get-seller-leads-without-buying-them",
        "img": "img/how-realtors-get-seller-leads-without-buying-them.jpg",
        "img_alt": "Illustration of a home with a for-sale sign sending signal waves to a phone",
        "cat": "seller-leads",
        "title": "How Do Realtors Get Seller Leads Without Buying Them?",
        "date": "2026-07-14",
        "excerpt": "Portal leads are rented, shared, and expensive. Here's the owned-asset playbook listing agents use to make sellers call them first.",
        "tldr": "Realtors get seller leads without buying them by becoming the visible, provable local expert for specific neighborhoods: an optimized Google Business Profile that wins agent-intent searches, dedicated neighborhood pages with real market data, reviews that tell seller stories, and content that answers seller questions — all of which make both Google and AI assistants recommend them by name. Unlike purchased portal leads, these assets are owned, unshared, and compound over time.",
        "sections": [
            ("Why purchased seller leads underperform",
             "<p>Most purchased \"seller leads\" are early-stage homeowners who filled out a home-value form — then got sold to several agents at once. You're paying to enter a speed-dial contest for a person who mostly wanted a Zestimate reality check.</p>"
             "<p>The deeper problem is structural: when you buy leads, the platform owns the demand and rents it back to you. Stop paying and the pipeline stops the same day. Nothing you spent last year makes next year cheaper.</p>"),
            ("Sellers choose the agent they've already heard of",
             "<p>Sellers behave differently from buyers. They interview two or three agents, usually sourced from neighbors, past clients, open houses — and increasingly from what Google and AI assistants say about their specific neighborhood.</p>"
             "<p>That means seller lead generation is really <b>reputation placement</b>: being the name attached to the neighborhood before the seller starts looking. The agent who \"seems to be everywhere\" in a farm area is on the interview list by default.</p>"),
            ("The owned-asset playbook",
             "<ul><li><b><a href='../services/google-business-profile.html'>Google Business Profile</a>, worked weekly.</b> Agent-intent searches (\"realtor near me\", \"listing agent in [area]\") resolve to the map pack — a surface portals can't own.</li>"
             "<li><b><a href='../services/local-seo.html'>Neighborhood pages</a>.</b> A genuinely useful page per farm area — market conditions, recent activity, seller guidance — outranks thin portal pages for neighborhood-level searches and gives AI a citable source.</li>"
             "<li><b>Reviews that tell seller stories.</b> Reviews mentioning your neighborhood, sale results, and process become the snippets Google shows and the evidence AI weighs.</li>"
             "<li><b>Seller-question content.</b> \"Should I sell now or wait?\" \"What's my home worth?\" Publish direct, local answers under your name.</li></ul>"
             "<p>None of this is a hack. It's the work of being findable and provable — done systematically instead of occasionally.</p>"),
            ("Where AI assistants change the game",
             "<p>When a homeowner asks ChatGPT or Google's AI who should sell their home in a given area, the answer names specific agents and cites sources. Those citations come from exactly the assets above: consistent profiles, neighborhood authority, reviews, and published answers.</p>"
             "<p>This is the new part of the playbook — and the least crowded. Most agents haven't noticed that the shortlist is now being written by answer engines. The ones who build citable local authority first get named first.</p>"),
        ],
        "faqs": [
            ("How long does it take to get seller leads organically?",
             "Foundational visibility (map pack, neighborhood searches) typically starts moving within weeks; being consistently recommended — by Google and by AI — usually builds over months. The trade-off for the wait: the pipeline you build is owned and compounds, instead of resetting to zero when spend stops."),
            ("Are Zillow seller leads worth it?",
             "They can produce closings, but the economics are rented: shared leads, response-time races, and rising costs per market. Most listing-focused agents do better treating portals as a supplement while building owned neighborhood authority that lowers their cost per listing every year."),
            ("What's the single highest-leverage first step?",
             "Claim and fully work your Google Business Profile, then build a real page for the one neighborhood where you have the most closings and reviews. Depth in one area beats thin presence in ten."),
        ],
    },
    {
        "slug": "how-real-estate-agents-show-up-in-chatgpt",
        "img": "img/how-real-estate-agents-show-up-in-chatgpt.jpg",
        "img_alt": "Illustration of an AI chat bubble containing a glowing house with a citation marker",
        "cat": "ai",
        "title": "How Do Real Estate Agents Show Up in ChatGPT's Recommendations?",
        "date": "2026-07-07",
        "excerpt": "AI assistants name specific agents and cite their sources. Here's what those systems actually look at — and how to become the name they give.",
        "tldr": "AI assistants like ChatGPT, Gemini, and Perplexity recommend real estate agents based on the sources they can find and trust: consistent business profiles, structured data that identifies who you are and where you work, third-party mentions, reviews, and content that directly answers the questions people ask. Agents show up in AI recommendations by making their identity machine-readable (entity consistency plus schema), earning independent mentions, and publishing genuinely useful local answers that AI can cite. This is called Generative Engine Optimization (GEO).",
        "sections": [
            ("What AI actually does when someone asks for an agent",
             "<p>Ask an assistant \"who's a good realtor in [city]?\" and it doesn't search a secret database of agents. It synthesizes from what it has learned and what it can retrieve: profiles, directories, reviews, local press, and content — then names people and often cites sources.</p>"
             "<p>That means the question \"how do I rank in ChatGPT?\" is really \"what would ChatGPT cite about me — and does it exist?\" For most agents, the honest answer today is: almost nothing. That's the opportunity.</p>"),
            ("The signals that make AI name you",
             "<ul><li><b>Entity consistency.</b> Your name, brokerage, markets, and specialties saying the same thing everywhere AI looks. Contradictions read as noise; consistency reads as fact.</li>"
             "<li><b>Structured data.</b> RealEstateAgent schema and a sameAs graph turn your website from prose into facts a machine can quote.</li>"
             "<li><b>Independent mentions.</b> Local press, community sites, and directories are treated as evidence. Your own website alone is a claim; a third-party mention is a citation.</li>"
             "<li><b>Reviews at volume and specificity.</b> \"Sold our home in [neighborhood] over asking\" teaches AI exactly what to recommend you for.</li>"
             "<li><b>Answerable content.</b> Direct, question-first answers about your market give assistants something liftable — with your name attached.</li></ul>"),
            ("What doesn't work",
             "<p>Keyword-stuffing your bio, spamming \"best realtor\" on your own site, or publishing AI-generated filler about national market trends. Answer engines synthesize across sources — self-praise with no independent corroboration doesn't survive the synthesis.</p>"
             "<p>Be equally skeptical of anyone guaranteeing placement in AI answers. These systems change constantly and nobody controls them. What's durable is the underlying evidence: real expertise, made machine-readable and independently confirmed.</p>"),
            ("How to start this week",
             "<p>Run the audit yourself: ask ChatGPT, Gemini, and Perplexity the questions your clients would ask — \"best listing agent in [your area]\", \"who should I use to buy in [neighborhood]\". Note who gets named and which sources get cited.</p>"
             "<p>Then work the gap: fix your <a href='../services/ai-citations.html'>entity consistency</a>, add schema, deepen your reviews, and publish one genuinely excellent local answer per month. The agents doing this now are building a moat while the shortlist is still short.</p>"),
        ],
        "faqs": [
            ("Can I pay to be recommended by ChatGPT?",
             "No. There's no ad placement inside organic AI recommendations today. Recommendations are synthesized from sources the model trusts, which is why the work is building citable evidence rather than buying position."),
            ("Does this replace SEO?",
             "It extends it. The same foundations — profiles, schema, reviews, content — feed both Google rankings and AI answers. GEO is best understood as SEO's next surface, not its replacement."),
            ("How do I measure AI visibility?",
             "Systematically ask the major assistants your market's key questions on a schedule, log who gets named and cited, and track your share over time. (This is exactly what our monthly AI visibility reports do.)"),
        ],
    },
    {
        "slug": "zillow-leads-vs-owning-your-pipeline",
        "img": "img/zillow-leads-vs-owning-your-pipeline.jpg",
        "img_alt": "Illustration of a balance scale weighing slipping coins against a rooted house",
        "cat": "strategy",
        "title": "Zillow Leads vs. Owning Your Pipeline: The Real Math",
        "date": "2026-06-30",
        "excerpt": "Rented demand versus owned demand isn't a philosophy debate — it's compounding arithmetic. Here's how to think about the split.",
        "tldr": "Portal leads (Zillow, Realtor.com) are rented demand: costs rise with competition, leads are shared, and the pipeline stops the day you stop paying. Owned marketing — your Google Business Profile, neighborhood pages, reviews, content, and AI citations — costs more patience upfront but compounds: each asset keeps producing without per-lead fees, and every closing strengthens it. The practical answer for most agents isn't either/or; it's capping portal spend as a bridge while building owned assets that permanently lower your cost per closing.",
        "sections": [
            ("What you're actually buying from a portal",
             "<p>A portal lead is a moment of intent, auctioned. The portal built its audience with listings — including yours — and sells access back to agents by ZIP code. In competitive markets the same inquiry can go to multiple agents, and the connection fee keeps climbing because the auction rewards whoever tolerates the thinnest margin.</p>"
             "<p>None of this makes portal leads worthless. It makes them <b>rent</b>. Rent can be worth paying — but nobody builds equity paying it.</p>"),
            ("What owned demand looks like",
             "<p>Owned demand is when the seller or buyer finds <i>you</i> — through the map pack, a neighborhood page, a review, an article, or an AI recommendation — and contacts you directly. No auction, no sharing, no per-lead fee.</p>"
             "<p>The defining property is compounding: a <a href='../services/local-seo.html'>neighborhood page</a> written this year still ranks next year; reviews accumulate; every published answer is one more reason for AI to cite you. The work stacks instead of evaporating.</p>"),
            ("The math that matters: cost per closing over time",
             "<p>Compare the trajectories, not the first month. Portal cost per closing is roughly flat-to-rising forever — you re-buy every closing at market price. Owned cost per closing starts high (you're paying for work before it produces) and then falls, because the same assets keep converting without new spend.</p>"
             "<p>The crossover typically arrives within the first year for agents who commit to a defined territory — and after it, every portal-free closing widens the gap. The agents who feel trapped on portals are usually the ones who never started the owned clock.</p>"),
            ("A sane split for most agents",
             "<p>Keep whatever portal spend is genuinely profitable for you today — treat it as bridge financing, not strategy. Redirect the rest into owned assets with a territory focus: one profile worked hard, a handful of neighborhoods, systematic reviews, and monthly answers.</p>"
             "<p>Revisit quarterly. As owned demand grows, portal spend should shrink by choice — not because the leads stopped, but because you stopped needing to rent them.</p>"),
        ],
        "faqs": [
            ("Should new agents buy portal leads?",
             "Sometimes — cash flow is real, and a new agent may need transactions before owned assets mature. The mistake isn't buying leads; it's buying leads *instead of* starting the owned clock. Do both from day one, even if owned starts small."),
            ("How much should I budget for owned marketing?",
             "Less than most agents spend on portals. A serious owned program (profile, neighborhoods, content, reviews) typically runs $1k–$7k/month depending on market coverage — comparable to a modest portal budget, with a completely different trajectory."),
            ("What if my market is dominated by big teams?",
             "Territory focus beats budget breadth. A big team can outspend you everywhere; it can't out-know you in the five neighborhoods you actually farm. Owned marketing rewards depth, which is the one dimension where solo agents can win."),
        ],
    },
    {
        "slug": "local-seo-for-real-estate-agents-2026",
        "img": "img/local-seo-for-real-estate-agents-2026.jpg",
        "img_alt": "Illustration of a neighborhood map with one glowing map pin above a block of homes",
        "cat": "seo",
        "title": "Local SEO for Real Estate Agents: What Actually Works in 2026",
        "date": "2026-06-23",
        "excerpt": "You will not outrank Zillow for listing searches — and it doesn't matter. The searches that win clients are agent-intent, and they're very winnable.",
        "tldr": "In 2026, local SEO for real estate agents works when it targets agent-intent and neighborhood-level searches instead of listing searches. Portals own \"homes for sale in [city]\"; agents can own \"realtor in [neighborhood]\", \"listing agent near me\", and \"selling a home in [area]\" through an optimized Google Business Profile, dedicated neighborhood pages, RealEstateAgent schema, consistent citations, and reviews. The same work now feeds AI answers (ChatGPT, AI Overviews), which increasingly sit above or replace traditional results.",
        "sections": [
            ("Stop competing for listing searches",
             "<p>\"Homes for sale in [city]\" returns Zillow, Redfin, Realtor.com, and their IDX shadows — sites with millions of pages and domain authority no agent site will match. Chasing those rankings burns budgets and morale for a search that mostly produces window-shoppers anyway.</p>"
             "<p>The searches that produce clients are different: <b>agent-intent</b> (\"best realtor in [area]\", \"listing agent near me\") and <b>neighborhood-intent</b> (\"[neighborhood] real estate agent\", \"selling a house in [neighborhood]\"). Portals serve these badly — their pages are templated and nobody at Zillow knows your cul-de-sac.</p>"),
            ("The stack that ranks agents in 2026",
             "<ul><li><b><a href='../services/google-business-profile.html'>Google Business Profile</a>:</b> the single highest-leverage asset — categories, services, weekly activity, Q&A, and review velocity.</li>"
             "<li><b><a href='../services/local-seo.html'>Neighborhood pages</a>:</b> one genuinely useful page per farm area, refreshed with real market data.</li>"
             "<li><b>Schema:</b> RealEstateAgent + FAQ markup so machines parse your expertise, service area, and answers.</li>"
             "<li><b>Citations:</b> identical name/brokerage/market data across every directory that matters.</li>"
             "<li><b>Reviews:</b> volume, recency, and neighborhood-specific language.</li></ul>"),
            ("The AI layer on top",
             "<p>AI Overviews and assistants now intercept many of these queries before a classic results page is ever seen. The good news: they're built from the same signals, plus a premium on content that answers questions directly and sources that corroborate independently.</p>"
             "<p>Practical implication: every page you build should open with a direct answer a machine could lift, and every fact about you should be independently confirmable. That's the difference between ranking and being <i>cited</i>.</p>"),
            ("What to ignore",
             "<p>Ignore anyone selling \"#1 rankings\" for city-level listing keywords, mass-generated city pages with swapped names, and review-gating tools that filter unhappy clients (against Google's policies, and increasingly detected). Shortcuts in local SEO age into liabilities.</p>"
             "<p>The boring truth: a focused agent doing profile + neighborhoods + reviews + answers consistently for two quarters beats almost any amount of clever.</p>"),
        ],
        "faqs": [
            ("Do I need a separate website from my brokerage page?",
             "Usually yes. Brokerage subpages rarely support neighborhood pages, schema, or content at the depth ranking requires — and your equity should live on a domain you keep if you switch brokerages."),
            ("How many neighborhood pages should I build?",
             "Start with the 5 areas where you have real closings, reviews, or history — depth beats breadth. Expand toward 15–30 as each page matures. Quality bar: would a local homeowner learn something from it?"),
            ("Is blogging still worth it for agents?",
             "Generic national content, no. Local, question-first answers, absolutely — they're now doing double duty as AI citation sources. One excellent local answer a month outperforms daily fluff."),
        ],
    },
    {
        "slug": "how-to-get-buyer-leads-without-portals",
        "img": "img/how-to-get-buyer-leads-without-portals.jpg",
        "img_alt": "Illustration of a magnifying glass over houses with question-mark chat bubbles",
        "cat": "buyer-leads",
        "title": "How to Get Buyer Leads Without Buying Them From Portals",
        "date": "2026-06-16",
        "excerpt": "Buyers start with a question, not a listing. The agents who answer the question — in Google and in AI — get the client before the portal does.",
        "tldr": "Agents get buyer leads without portals by capturing buyers at the question stage — before they're deep in listing apps. That means winning agent-intent searches through Google Business Profile, publishing direct answers to buyer questions (\"how much do I need to buy in [city]\", \"best neighborhoods for families in [area]\"), building neighborhood guides buyers actually use, and being the agent AI assistants name when someone asks who to work with. Buyers contact the agent who already answered their question — pre-sold and unshared.",
        "sections": [
            ("Buyers begin with questions, not listings",
             "<p>Before anyone saves a search on Zillow, they ask questions: Can we afford this city? Which neighborhoods fit us? Do we even need an agent? Increasingly those questions go to ChatGPT and Google's AI first.</p>"
             "<p>Portals dominate the listing stage — but the <b>question stage comes earlier</b>, and it's where loyalty forms. The agent who answers the question owns the relationship before the portal ever sees the buyer.</p>"),
            ("Build the answers buyers are searching for",
             "<ul><li><b>Affordability and process answers:</b> \"How much do I need to buy in [city]?\" \"What does closing cost here?\" Local numbers, straight talk.</li>"
             "<li><b><a href='../services/content.html'>Neighborhood guides</a>:</b> the honest comparisons buyers can't get from listing data — commute, schools, vibe, trade-offs.</li>"
             "<li><b>First-timer content:</b> the anxieties nobody types into a portal search bar but everyone asks an AI.</li></ul>"
             "<p>Each answer is findable in Google, citable by AI, and shareable in a DM — three lead channels from one piece of work.</p>"),
            ("Be the recommended agent, not the fastest responder",
             "<p>Portal buyer leads are a response-time contest for a stranger. Owned buyer leads invert it: the buyer read your neighborhood guide, saw your reviews, maybe heard an AI name you — then reached out. You start as the trusted expert, not one of five missed calls.</p>"
             "<p>The same entity and review work that wins sellers wins buyers; the difference is the content layer. Buyer-side content is questions-and-guides; seller-side is proof-and-results.</p>"),
            ("The open-house multiplier",
             "<p>Open houses remain the best offline buyer-lead source — and they compound the online system. Every visitor who Googles you afterward should find a worked profile, neighborhood authority, and answers. The agents who convert open-house traffic best are the ones whose online presence confirms what the handshake started.</p>"),
        ],
        "faqs": [
            ("Aren't buyer leads less valuable than seller leads?",
             "Per transaction, often — but buyer-side content and relationships feed listings: today's buyer is a seller in 5–7 years, and buyer-side reviews build the authority sellers check. A balanced engine produces both."),
            ("Do neighborhood guides really generate leads?",
             "Yes, on two paths: search traffic from buyers comparing areas, and AI citations when someone asks an assistant where to live or who to work with there. The guide has to be genuinely useful — thin \"about the area\" pages don't move."),
            ("What about social media for buyer leads?",
             "Social is the multiplier, not the engine: it makes the recommendation feel real when buyers check you out. Pair neighborhood spotlights and market takes with the search/AI foundation and each makes the other convert better."),
        ],
    },
    {
        "slug": "what-are-neighborhood-pages",
        "img": "img/what-are-neighborhood-pages.jpg",
        "img_alt": "Illustration of a browser window framing a neighborhood with one glowing house",
        "cat": "seo",
        "title": "What Are Neighborhood Pages — and Why Do They Win Listings?",
        "date": "2026-06-09",
        "excerpt": "The most underused asset in agent marketing: a real page, for a real neighborhood, that proves you're its expert. Here's the anatomy.",
        "tldr": "A neighborhood page is a dedicated page on an agent's website about one specific community — its market conditions, housing stock, buyer and seller guidance, and the agent's actual track record there. Done well, neighborhood pages win the neighborhood-level searches portals serve badly, become the evidence AI assistants cite when recommending agents for that area, and function as pre-listing proof for sellers comparing agents. They're the online equivalent of farming — but the postcard never expires.",
        "sections": [
            ("The anatomy of a neighborhood page that works",
             "<ul><li><b>A direct opening answer:</b> what's happening in this market right now, in plain language.</li>"
             "<li><b>Real local specifics:</b> housing stock, price bands, what's driving demand — things only someone who works the area would say.</li>"
             "<li><b>Your track record there:</b> closings, reviews from the area, years worked. Proof, not adjectives.</li>"
             "<li><b>Seller and buyer guidance:</b> what listing prep matters here; what buyers should know before touring.</li>"
             "<li><b>Schema and internal links:</b> place + FAQ markup, linked into your services and content.</li></ul>"),
            ("Why portals can't compete here",
             "<p>Zillow has a page for your neighborhood too — an auto-generated template with listing counts and a mortgage widget. It has scale; it cannot have <i>knowledge</i>. No portal writer knows that homes on the west side back onto the arroyo or that the HOA just changed rental rules.</p>"
             "<p>Google and AI systems both reward specificity they can't find elsewhere. A page with genuinely local information is unmatchable content in the literal sense — there is nowhere else for it to come from but you.</p>"),
            ("The listing-interview effect",
             "<p>Here's the part that surprises agents: neighborhood pages win listings even when the seller never searched. Sellers vet their interview shortlist online, and an agent with a serious page about <i>their street's</i> market walks in pre-credentialed. The CMA confirms what the page already argued: this person knows our neighborhood.</p>"
             "<p>Pair the page with reviews from the same area and the effect stacks — the page claims expertise, the reviews prove it, and Google shows both.</p>"),
            ("How many, and in what order",
             "<p>Start with the neighborhoods where you have evidence: closings, reviews, personal history. Five deep pages beat thirty thin ones — thin location pages are the most common local SEO mistake in real estate.</p>"
             "<p>Then expand outward in rings: adjacent areas where your evidence partially transfers, then the aspirational territories. Refresh each page quarterly with real market data so it stays citable. (Our <a href='../services/local-seo.html'>plans cover 5, 15, or 30 neighborhoods</a> for exactly this reason.)</p>"),
        ],
        "faqs": [
            ("Aren't neighborhood pages just doorway pages?",
             "Doorway pages are thin duplicates with swapped place names — and they deserve their bad reputation. A real neighborhood page is the opposite: unique local knowledge, market data, and proof of work. The difference is obvious to readers, and to ranking systems."),
            ("Can I put listings on my neighborhood pages?",
             "A few current or recent listings help as proof of activity, but don't rebuild a mini-portal — the page's job is establishing you as the area expert, not competing on inventory. Guidance and knowledge convert; search widgets leak visitors back to portals."),
            ("What if I don't have closings in a neighborhood yet?",
             "Lead with knowledge instead of history: genuinely useful market analysis, honest area guidance, and hyperlocal specifics. Evidence accelerates the page, but usefulness earns rankings and citations on its own — and the first closing adds the proof."),
        ],
    },
]

ARTICLE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | CitedRealty</title>
<meta name="description" content="{excerpt}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="/assets/icon-square.svg">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
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
      <li><a href="../index.html#services" aria-haspopup="true">Services</a>
        <ul class="dd">
          <li><a href='../services/ai-citations.html'>AI Citations (GEO)</a></li>
          <li><a href='../services/website-design.html'>Website Design</a></li>
          <li><a href='../services/google-business-profile.html'>Google Business Profile</a></li>
          <li><a href='../services/local-seo.html'>Local SEO &amp; Neighborhoods</a></li>
          <li><a href='../services/content.html'>Blog &amp; Content</a></li>
          <li><a href='../services/social-media.html'>Social Media</a></li>
          <li><a href='../services/reviews.html'>Reviews &amp; Reputation</a></li>
        </ul>
      </li>
      <li><a href="../index.html#who" aria-haspopup="true">Who we help</a>
        <ul class="dd">
          <li><a href='../audiences/solo-agents.html'>Solo Agents</a></li>
          <li><a href='../audiences/teams.html'>Teams</a></li>
          <li><a href='../audiences/brokerages.html'>Brokerages</a></li>
          <li><a href='../audiences/listing-agents.html'>Listing Agents</a></li>
        </ul>
      </li>
      <li><a href="../index.html#pricing">Pricing</a></li>
      <li><a href="index.html">Resources</a></li>
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
  <a href="index.html">Resources</a>
  <a href="../index.html#faq">FAQ</a>
  <a href="../index.html#contact" class="grad">Free AI visibility audit →</a>
</div>

<main id="main">
<header class="article-hero">
  <div class="wrap">
    <p class="crumb"><a href="../index.html">Home</a> / <a href="index.html">Resources</a> / {cat_label}</p>
    <span class="cat">{cat_label}</span>
    <h1>{title}</h1>
    <p class="meta">CitedRealty · {date_h} · For realtors &amp; brokers</p>
  </div>
</header>

<div class="wrap article-grid">
  <article>
{figure}    <div class="tldr"><div class="label">TL;DR — the short answer</div><p>{tldr}</p></div>
    <div class="article-body">
{body}
    </div>
    <div class="article-faq">
      <h2 id="faq">FAQ</h2>
{faqs}
    </div>
    <div class="outcome article-cta reveal">
      <h2>Want this done for you?</h2>
      <p>CitedRealty runs the whole system — Google Business Profile, neighborhood pages, content, reviews, and AI citations — for realtors and brokers. Start with a free AI visibility audit of your market.</p>
      <a class="btn btn-primary" href="../index.html#contact">Get your free audit</a>
    </div>
  </article>
  <aside class="toc" aria-label="On this page">
    <div class="label">On this page</div>
    <ol>
{toc}
      <li><a href="#faq">FAQ</a></li>
    </ol>
  </aside>
</div>
</main>

<footer>
  <div class="wrap">
    <div class="foot-legal" style="border:none; margin:0; padding:0">
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

INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Resources &amp; News — Marketing Answers for Realtors | CitedRealty</title>
<meta name="description" content="Straight answers to the marketing questions realtors and brokers actually ask: seller leads, buyer leads, AI search visibility, and local SEO.">
<link rel="canonical" href="{brand}/blog/index.html">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="/assets/icon-square.svg">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/styles.css">
<script src="../assets/theme.js"></script>
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
      <li><a href="../index.html#services" aria-haspopup="true">Services</a>
        <ul class="dd">
          <li><a href='../services/ai-citations.html'>AI Citations (GEO)</a></li>
          <li><a href='../services/website-design.html'>Website Design</a></li>
          <li><a href='../services/google-business-profile.html'>Google Business Profile</a></li>
          <li><a href='../services/local-seo.html'>Local SEO &amp; Neighborhoods</a></li>
          <li><a href='../services/content.html'>Blog &amp; Content</a></li>
          <li><a href='../services/social-media.html'>Social Media</a></li>
          <li><a href='../services/reviews.html'>Reviews &amp; Reputation</a></li>
        </ul>
      </li>
      <li><a href="../index.html#who" aria-haspopup="true">Who we help</a>
        <ul class="dd">
          <li><a href='../audiences/solo-agents.html'>Solo Agents</a></li>
          <li><a href='../audiences/teams.html'>Teams</a></li>
          <li><a href='../audiences/brokerages.html'>Brokerages</a></li>
          <li><a href='../audiences/listing-agents.html'>Listing Agents</a></li>
        </ul>
      </li>
      <li><a href="../index.html#pricing">Pricing</a></li>
      <li><a href="index.html">Resources</a></li>
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
  <a href="index.html">Resources</a>
  <a href="../index.html#faq">FAQ</a>
  <a href="../index.html#contact" class="grad">Free AI visibility audit →</a>
</div>

<main id="main">
<header class="blog-hero">
  <div class="wrap">
    <p class="eyebrow">Resources &amp; News</p>
    <h1>Marketing answers for <span class="grad">realtors &amp; brokers.</span></h1>
    <p>The questions agents actually ask — seller leads, buyer leads, AI visibility, local SEO — answered straight, no gatekeeping. If it helps you do it yourself, good. If you'd rather have it done, you know where we are.</p>
    <div class="chips" role="tablist" aria-label="Filter articles">
      <button class="chip active" data-cat="all">All</button>
{chips}
    </div>
  </div>
</header>

<div class="wrap">
  <div class="post-grid" id="postGrid">
{cards}
  </div>
</div>
</main>

<footer>
  <div class="wrap">
    <div class="foot-legal" style="border:none; margin:0; padding:0">
      <span>© 2026 CitedRealty · <a href="../privacy.html">Privacy</a> · <a href="../terms.html">Terms</a> · <a href="#" data-cookie-prefs>Cookie preferences</a> · <a href="https://www.google.com/preferences/source?q=citedrealty.com" target="_blank" rel="noopener" title="Add CitedRealty as a preferred source in Google Search"><span style="color:#F59E0B">★</span> Make us a preferred source on Google</a></span>
      <span>When buyers ask AI, you're the answer.<sup>[1]</sup></span>
    </div>
  </div>
</footer>

<div class="sticky-cta"><a href="../index.html#contact">Get your free AI visibility audit</a></div>
<script src="../assets/app.js"></script>
<script src="../assets/consent.js" defer></script>
<script>
(function(){{
  var chips=document.querySelectorAll('.chip'), cards=document.querySelectorAll('.post-card');
  chips.forEach(function(ch){{
    ch.addEventListener('click',function(){{
      chips.forEach(function(c){{c.classList.remove('active')}});
      ch.classList.add('active');
      var cat=ch.getAttribute('data-cat');
      cards.forEach(function(card){{
        card.style.display=(cat==='all'||card.getAttribute('data-cat')===cat)?'':'none';
      }});
    }});
  }});
}})();
</script>
</body>
</html>
"""


def slugify_h2(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def date_human(iso: str) -> str:
    import datetime
    return datetime.date.fromisoformat(iso).strftime("%B %-d, %Y")


def build_article(p: dict) -> str:
    url = f"{BRAND_URL}/blog/{p['slug']}.html"
    og_image = f"{BRAND_URL}/blog/{p['img']}" if p.get("img") else BRAND_URL + "/assets/icon-512.png"
    figure = (
        f'    <figure class="article-figure"><img src="{p["img"]}" alt="{h.escape(p.get("img_alt",""))}" width="1200" height="800"></figure>\n'
        if p.get("img") else ""
    )
    body, toc = [], []
    for h2, content in p["sections"]:
        hid = slugify_h2(h2)
        body.append(f'      <h2 id="{hid}">{h.escape(h2)}</h2>\n{content}')
        toc.append(f'      <li><a href="#{hid}">{h.escape(h2)}</a></li>')
    faqs = "\n".join(
        f'      <details><summary>{h.escape(q)}</summary><p>{h.escape(a)}</p></details>'
        for q, a in p["faqs"]
    )
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": url + "#article",
                "headline": p["title"],
                "description": p["excerpt"],
                "datePublished": p["date"],
                "dateModified": p["date"],
                "url": url,
                "image": og_image,
                "author": {"@type": "Organization", "name": "CitedRealty", "@id": BRAND_URL + "/#business"},
                "publisher": {"@id": BRAND_URL + "/#business"},
                "mainEntityOfPage": url,
                "articleSection": CATS[p["cat"]],
            },
            {
                "@type": "FAQPage",
                "@id": url + "#faq",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in p["faqs"]
                ],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BRAND_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Resources", "item": BRAND_URL + "/blog/index.html"},
                    {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
                ],
            },
        ],
    }, indent=2)
    return ARTICLE.format(
        title=h.escape(p["title"]), excerpt=h.escape(p["excerpt"]), url=url, brand=BRAND_URL,
        schema=schema, cat_label=CATS[p["cat"]], date_h=date_human(p["date"]),
        tldr=h.escape(p["tldr"]), body="\n".join(body), faqs=faqs, toc="\n".join(toc),
        og_image=og_image, figure=figure,
    )


def build_index() -> str:
    chips = "\n".join(
        f'      <button class="chip" data-cat="{k}">{v}</button>' for k, v in CATS.items()
    )
    cards = []
    for i, p in enumerate(POSTS):
        feat = " featured" if i == 0 else ""
        thumb = (
            f'<img class="thumb" src="{p["img"]}" alt="" loading="lazy">' if p.get("img") else ""
        )
        cards.append(
            f'    <a class="post-card{feat}" data-cat="{p["cat"]}" href="{p["slug"]}.html">{thumb}'
            f'<span class="cat">{CATS[p["cat"]]}</span><h2>{h.escape(p["title"])}</h2>'
            f'<p>{h.escape(p["excerpt"])}</p><span class="meta">{date_human(p["date"])}</span></a>'
        )
    return INDEX.format(brand=BRAND_URL, chips=chips, cards="\n".join(cards))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for p in POSTS:
        (OUT / f"{p['slug']}.html").write_text(build_article(p))
        print("wrote", p["slug"] + ".html")
    (OUT / "index.html").write_text(build_index())
    print("wrote index.html")
