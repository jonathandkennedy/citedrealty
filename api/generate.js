// CitedRealty — shared generator endpoint for free AI tools
// (review-reply and listing-description). Uses GEMINI_API_KEY env var.

const WINDOW_MS = 60 * 60 * 1000;
const MAX_PER_WINDOW = 10; // generations per IP per hour (per warm instance)
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

function buildPrompt(mode, f) {
  if (mode === "review-reply") {
    return (
      `Write a public response from a real estate agent to a client review. ` +
      `Agent name: ${f.name}. Tone: ${f.tone}. ` +
      `Rules: 2-4 sentences, warm and specific to what the review actually says, no emojis, ` +
      `no discount offers, never reveal transaction or personal details the reviewer didn't share, ` +
      `sign off with the agent's first name. If the review is negative: acknowledge calmly, no arguing, ` +
      `no admissions of fault, invite an offline conversation. Output ONLY the reply text.\n\n` +
      `REVIEW:\n"${f.review}"`
    );
  }
  // listing-description
  return (
    `Write a real estate listing description. ` +
    `Property details: ${f.details}. ` +
    `${f.neighborhood ? `Neighborhood: ${f.neighborhood}. ` : ""}` +
    `Tone: ${f.tone}. ` +
    `Rules: 120-180 words, lead with the strongest feature, specific over superlative, no ALL CAPS, ` +
    `no fair-housing red flags (never describe the ideal buyer or neighborhood demographics — describe the property), ` +
    `no invented facts beyond the details given, end with a simple call to action to schedule a showing. ` +
    `Output ONLY the description text.`
  );
}

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "https://citedrealty.com");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    return res.status(503).json({ error: "not_configured",
      message: "This tool is warming up — try again soon, or grab the free human-run audit." });
  }

  const ip = (req.headers["x-forwarded-for"] || "?").split(",")[0].trim();
  if (rateLimited(ip)) {
    return res.status(429).json({ error: "rate_limited",
      message: "You've hit the hourly limit — back in a bit, or get the free full audit." });
  }

  const mode = clean(req.body?.mode, 30);
  const fields = {
    name: clean(req.body?.name, 80),
    tone: clean(req.body?.tone, 40) || "professional and warm",
    review: clean(req.body?.review, 1200),
    details: clean(req.body?.details, 1200),
    neighborhood: clean(req.body?.neighborhood, 120),
    market: clean(req.body?.market, 80),
  };

  if (mode === "review-reply" && (!fields.name || !fields.review))
    return res.status(400).json({ error: "bad_input", message: "Your name and the review text are required." });
  if (mode === "listing-description" && !fields.details)
    return res.status(400).json({ error: "bad_input", message: "Property details are required." });
  if (mode !== "review-reply" && mode !== "listing-description")
    return res.status(400).json({ error: "bad_input", message: "Unknown tool." });

  try {
    const r = await fetch(
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
      {
        method: "POST",
        headers: { "x-goog-api-key": key, "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [{ parts: [{ text: buildPrompt(mode, fields) }] }],
          generationConfig: { temperature: 0.7, maxOutputTokens: 500 },
        }),
      }
    );
    if (!r.ok) throw new Error(`gemini ${r.status}`);
    const data = await r.json();
    const text = (data.candidates?.[0]?.content?.parts || []).map(p => p.text || "").join("").trim();
    if (!text) throw new Error("empty");

    // Lead notification → Formspree (emailed + stored in dashboard)
    try {
      await fetch("https://formspree.io/f/mykrpold", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          _subject: `Tool lead: ${mode} — ${fields.name || "(no name)"} ${fields.market ? `(${fields.market})` : ""}`,
          tool: mode,
          agent_name: fields.name || "(not given)",
          market: fields.market || fields.neighborhood || "(not given)",
        }),
      });
    } catch { /* non-blocking */ }

    return res.status(200).json({ ok: true, text });
  } catch (e) {
    return res.status(502).json({ error: "upstream",
      message: "The generator hit a snag — try again in a minute." });
  }
}
