// CitedRealty — AI Visibility Checker (Vercel serverless function).
// Calls Gemini with Google Search grounding to test whether an agent shows up
// when AI is asked about their market. Requires env var GEMINI_API_KEY
// (Vercel dashboard → Project → Settings → Environment Variables).

const WINDOW_MS = 60 * 60 * 1000;
const MAX_PER_WINDOW = 5; // per IP per hour (per warm instance; good-enough MVP limit)
const hits = new Map();

function rateLimited(ip) {
  const now = Date.now();
  const rec = hits.get(ip) || { n: 0, t: now };
  if (now - rec.t > WINDOW_MS) { rec.n = 0; rec.t = now; }
  rec.n += 1;
  hits.set(ip, rec);
  return rec.n > MAX_PER_WINDOW;
}

const clean = (s, max) => String(s || "").replace(/[<>{}\\]/g, "").trim().slice(0, max);

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://citedrealty.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return res.status(503).json({ error: "not_configured",
      message: "The checker is warming up. Request a free human-run audit instead — it's more thorough anyway." });
  }

  const ip = (req.headers["x-forwarded-for"] || "?").split(",")[0].trim();
  if (rateLimited(ip)) {
    return res.status(429).json({ error: "rate_limited",
      message: "That's a lot of checking! Try again in an hour — or request the free full audit." });
  }

  const name = clean(req.body?.name, 80);
  const brokerage = clean(req.body?.brokerage, 80);
  const market = clean(req.body?.market, 80);
  if (!name || !market) return res.status(400).json({ error: "bad_input", message: "Name and market are required." });

  const prompt =
    `You are helping run a real estate AI-visibility check. Use web search and answer in plain text with EXACTLY these three labeled sections:\n\n` +
    `AGENTS: List up to 6 real estate agents or teams that credible public sources most recommend for "${market}" (names only, comma-separated). If none clearly emerge, say "unclear".\n\n` +
    `TARGET: State whether public sources show that "${name}"${brokerage ? ` (${brokerage})` : ""} is a real estate agent active in ${market}, and whether any source would justify recommending them. One or two sentences, factual only.\n\n` +
    `NOTE: One sentence on which kinds of sources dominated your results (portals, review sites, agent websites, press).`;

  try {
    const r = await fetch(
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
      {
        method: "POST",
        headers: { "x-goog-api-key": key, "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          tools: [{ google_search: {} }],
          generationConfig: { temperature: 0.2, maxOutputTokens: 900 },
        }),
      }
    );
    if (!r.ok) throw new Error(`gemini ${r.status}`);
    const data = await r.json();
    const cand = data.candidates?.[0];
    const text = (cand?.content?.parts || []).map(p => p.text || "").join("\n");

    const sources = [];
    for (const ch of cand?.groundingMetadata?.groundingChunks || []) {
      const uri = ch.web?.uri, title = ch.web?.title;
      if (title && !sources.some(s => s.title === title)) sources.push({ title, uri });
    }

    const named = text.toLowerCase().includes(name.toLowerCase());

    // Lead notification: every completed check goes to Formspree (emailed + stored
    // in the dashboard — same form as the site's lead form).
    try {
      await fetch("https://formspree.io/f/mykrpold", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          _subject: `Checker lead: ${name} (${market}) — ${named ? "NAMED by AI" : "NOT NAMED — sales opportunity"}`,
          tool: "AI Visibility Checker",
          agent_name: name,
          brokerage: brokerage || "(not given)",
          market,
          ai_named: named ? "yes" : "no",
          sources_cited: sources.slice(0, 5).map(s => s.title).join(", ") || "(none)",
        }),
      });
    } catch { /* never block the visitor's result on notification failure */ }

    return res.status(200).json({ ok: true, named, text, sources: sources.slice(0, 10) });
  } catch (e) {
    return res.status(502).json({ error: "upstream",
      message: "The AI check hit a snag. Try again in a minute — or grab the free full audit." });
  }
}
