# CitedRealty — citedrealty.com

**When buyers ask AI, you're the answer.**

Marketing site for CitedRealty: AI search marketing (GEO), websites, local SEO, and
content for realtors and brokers. Pure static HTML/CSS/JS — no build step, no framework.

## Deploy (Vercel)

Import this repo in Vercel → Framework preset: **Other** → no build command, output
directory: root. That's it. Then point the `citedrealty.com` domain at the project.

## Develop locally

```
python3 -m http.server 4601
# http://localhost:4601
```

## Editing

- Homepage: `index.html` (self-contained styles/scripts)
- Service / audience / blog pages are **generated** — edit the data in
  `gen_services.py`, `gen_audiences.py`, `gen_blog.py`, then run the script
  (`python3 gen_blog.py`) to rebuild.
- Blog hero images: `gen_blog_images_gemini.sh` (API keys live outside this repo).
- Full documentation, design system, and the pre-launch checklist: **`HANDOFF.md`**
