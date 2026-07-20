#!/bin/zsh
# CitedRealty blog hero image generator (OpenAI gpt-image-1).
# Usage: zsh gen_blog_images.sh [slug ...]   (no args = all slugs listed below)
# Writes blog/img/<slug>.png, then downscale with:  sips -Z 1200 -s format jpeg ...
set -a; source /Users/jonkennedy/retainer-reach/citedrealty/.env; set +a
OUT=/Users/jonkennedy/retainer-reach/citedrealty.com/blog/img
mkdir -p "$OUT"; cd "$OUT"

STYLE="Editorial illustration for a real estate marketing blog. Flat modern vector style, minimal, elegant. Very dark indigo background (#0B0B14) with glowing indigo-to-violet-to-lilac gradient accents (#4F46E5, #8B5CF6, #C084FC), subtle thin grid lines, soft glow. No text, no letters, no words, no logos. Wide 3:2 composition, generous margins."

typeset -A PROMPTS
PROMPTS[how-realtors-get-seller-leads-without-buying-them]="A modern house with a blank for-sale yard sign, radiating gentle signal waves that reach a glowing smartphone held nearby. $STYLE"
PROMPTS[how-real-estate-agents-show-up-in-chatgpt]="A large AI chat answer bubble containing a small glowing house icon with a tiny superscript citation marker floating beside it, sparkles around. $STYLE"
PROMPTS[zillow-leads-vs-owning-your-pipeline]="A balance scale: one side holds a pile of coins slipping away, the other side holds a small house with roots growing downward like a tree. $STYLE"
PROMPTS[local-seo-for-real-estate-agents-2026]="A stylized neighborhood map from above with rows of small houses and one glowing gradient map pin standing tall above a chosen block. $STYLE"
PROMPTS[how-to-get-buyer-leads-without-portals]="A magnifying glass hovering over a row of different houses, with small question-mark chat bubbles floating above rooftops. $STYLE"
PROMPTS[what-are-neighborhood-pages]="A browser window frame containing a charming illustrated neighborhood of houses and trees, one house highlighted with a gradient glow. $STYLE"

slugs=("$@")
if [ ${#slugs[@]} -eq 0 ]; then slugs=(${(k)PROMPTS}); fi

for name in $slugs; do
  p=${PROMPTS[$name]}
  if [ -z "$p" ]; then echo "SKIP unknown slug $name"; continue; fi
  echo "--- generating $name"
  resp=$(curl -s https://api.openai.com/v1/images/generations \
    -H "Authorization: Bearer $OPENAI_API_KEY" -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$p" '{model:"gpt-image-1", prompt:$p, size:"1536x1024", quality:"medium", n:1}')")
  if echo "$resp" | jq -e '.data[0].b64_json' >/dev/null 2>&1; then
    echo "$resp" | jq -r '.data[0].b64_json' | base64 -d > "$name.png"
    echo "OK $name"
  else
    echo "FAILED $name: $(echo "$resp" | jq -c '.error // .' | head -c 300)"
  fi
done
echo "DONE"
