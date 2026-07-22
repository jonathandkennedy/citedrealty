#!/bin/zsh
# CitedRealty blog hero images via Gemini (gemini-2.5-flash-image).
# Usage: zsh gen_blog_images_gemini.sh [slug ...]  (no args = all listed below)
set -a; source /Users/jonkennedy/retainer-reach/citedrealty/.env; set +a
OUT=/Users/jonkennedy/retainer-reach/citedrealty.com/blog/img
mkdir -p "$OUT"; cd "$OUT"

STYLE="Editorial illustration for a real estate marketing blog. Flat modern vector style, minimal, elegant. Very dark indigo background (#0B0B14) with glowing indigo-to-violet-to-lilac gradient accents (#4F46E5, #8B5CF6, #C084FC) and a single warm amber glow accent, subtle thin grid lines. No text, no letters, no words, no logos. Wide composition, generous margins."

typeset -A PROMPTS
PROMPTS[ai-tools-vs-getting-cited-by-ai]="Split composition: on the left a small robot arm writing on a document, on the right a glowing trophy with a tiny house on it; a subtle divider between them. $STYLE"
PROMPTS[the-3-3-3-rule-real-estate-marketing]="Three glowing clock faces in a neat row, each slightly larger, above a small warm house. $STYLE"
PROMPTS[digital-marketing-mistakes-realtors-make]="A small charming house with several little warning-sign flags planted in the ground around it, one flag glowing. $STYLE"
PROMPTS[real-estate-marketing-roi]="A balance scale: a small house on one pan, a rising stack of gradient coins on the other, tipping toward the coins. $STYLE"
PROMPTS[best-crm-for-realtors]="Stylized contact cards with tiny person icons flowing along glowing lines into a central house-shaped hub. $STYLE"
PROMPTS[are-real-estate-marketing-courses-worth-it]="A graduation cap beside a small glowing house, with a subtle forking path leading two directions in front of them. $STYLE"
PROMPTS[how-to-build-a-neighborhood-page]="A webpage frame being assembled like scaffolding around a charming cluster of small glowing houses and trees. $STYLE"
PROMPTS[diy-ai-visibility-audit]="A large magnifying glass examining a glowing AI chat bubble, with a small scorecard of checkmarks and crosses floating beside it. $STYLE"
PROMPTS[what-is-idx]="A stream of small listing cards with house icons flowing from a large office building into a smaller cozy website window. $STYLE"
PROMPTS[optimize-google-business-profile-realtor]="A glowing map pin hovering above a charming storefront-style house, with three floating checklist cards beside it showing checkmarks. $STYLE"
PROMPTS[get-more-google-reviews-real-estate-agent]="Five glowing stars rising from a house chimney like warm floating lanterns into the night. $STYLE"
PROMPTS[what-data-do-ai-assistants-use]="Streams of glowing particles flowing from a document, a star, and a small globe, converging into a large AI chat bubble. $STYLE"
PROMPTS[realestateagent-schema-walkthrough]="A house blueprint on the left morphing into elegant glowing code brackets and braces on the right. $STYLE"
PROMPTS[eeat-for-real-estate-agents]="Four glowing classical pillars of slightly different heights supporting a house-shaped roof. $STYLE"
PROMPTS[california-ai-listing-photo-law]="A framed photograph of a house on an easel, an elegant magic wand with sparkles hovering over it, and a small neat blank tag hanging from the frame corner. $STYLE"
PROMPTS[connecticut-private-listings-ban]="A charming house stepping out from behind a velvet rope barrier into warm open public light, small crowd of abstract figures welcoming it. $STYLE"
PROMPTS[nar-coming-soon-listings-rules]="A glowing house partially revealed behind an elegant theater curtain being lifted, soft spotlight. $STYLE"
PROMPTS[how-do-new-agents-get-first-clients]="An open upturned hand holding a tiny glowing house with a small sprout growing beside it. $STYLE"
PROMPTS[is-door-knocking-worth-it]="A single glowing front door with soft concentric sound ripples radiating outward from a knock. $STYLE"
PROMPTS[are-open-houses-worth-it]="A house with its front door wide open, warm light spilling out onto a welcoming path, small footprints approaching. $STYLE"
PROMPTS[is-cold-calling-dead-for-realtors]="A vintage telephone handset glowing warmly, its curly cord winding toward a small house silhouette. $STYLE"
PROMPTS[do-real-estate-postcards-work]="A neat stack of blank postcards with one card lifting into the air toward a glowing house, motion lines behind it. $STYLE"
PROMPTS[real-estate-ai-search-statistics]="A rising bar chart whose bars are stylized glowing houses of increasing height, with a large AI chat bubble beside it containing a small checkmark. $STYLE"
PROMPTS[facebook-ads-vs-google-lsa-for-realtors]="A split composition: on the left a glowing megaphone radiating soft social reaction bubbles, on the right a search bar with a verified checkmark badge, a small warm house centered between them. $STYLE"
PROMPTS[best-real-estate-website-design-companies]="A row of five floating browser windows, each framing a differently styled small house, one window glowing brighter than the rest. $STYLE"
PROMPTS[luxury-presence-alternatives]="One large ornate glowing doorway with a cluster of smaller varied doorways beside it, paths leading to each. $STYLE"
PROMPTS[real-estate-agent-website-cost]="A floating browser window with a hanging price tag, beside neat stacks of gradient coins of different heights. $STYLE"
PROMPTS[do-realtors-need-their-own-website]="A small warm glowing house standing proudly on its own foundation platform, apart from a big generic office building in the background. $STYLE"
PROMPTS[zillow-vs-realtor-com-vs-homes-com-leads]="Three large abstract doorways side by side, each glowing a slightly different hue, with a small figure of a person standing before them deciding which path to take. $STYLE"
PROMPTS[zillow-premier-agent-vs-local-seo]="A forked road: one branch leads to a big flashy billboard, the other winds toward a warmly glowing neighborhood of small houses on a hill. $STYLE"
PROMPTS[how-much-should-realtors-spend-on-marketing]="A house-shaped piggy bank with gradient coins stacked beside it forming an ascending bar chart. $STYLE"
PROMPTS[best-seller-lead-sources-for-listing-agents]="A winners' podium with three glowing houses on first, second and third place steps, confetti sparkles. $STYLE"

slugs=("$@")
if [ ${#slugs[@]} -eq 0 ]; then slugs=(${(k)PROMPTS}); fi

for name in $slugs; do
  p=${PROMPTS[$name]}
  if [ -z "$p" ]; then echo "SKIP unknown slug $name"; continue; fi
  echo "--- generating $name (gemini)"
  curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
    -d "$(jq -n --arg p "$p" '{contents:[{parts:[{text:$p}]}],generationConfig:{imageConfig:{aspectRatio:"3:2"}}}')" > "/tmp/gem_$name.json"
  python3 - "$name" <<'PY'
import json, base64, sys
name = sys.argv[1]
d = json.load(open(f"/tmp/gem_{name}.json"))
if "error" in d:
    print("FAILED", name, json.dumps(d["error"])[:250]); sys.exit(0)
parts = d.get("candidates", [{}])[0].get("content", {}).get("parts", [])
imgs = [p for p in parts if "inlineData" in p]
if imgs:
    open(f"{name}.png", "wb").write(base64.b64decode(imgs[0]["inlineData"]["data"]))
    print("OK", name)
else:
    print("NO IMAGE", name, json.dumps(d)[:250])
PY
done
echo "DONE"
