#!/bin/zsh
# CitedRealty blog hero images via Gemini (gemini-2.5-flash-image).
# Usage: zsh gen_blog_images_gemini.sh [slug ...]  (no args = all listed below)
set -a; source /Users/jonkennedy/retainer-reach/citedrealty/.env; set +a
OUT=/Users/jonkennedy/retainer-reach/citedrealty.com/blog/img
mkdir -p "$OUT"; cd "$OUT"

STYLE="Editorial illustration for a real estate marketing blog. Flat modern vector style, minimal, elegant. Very dark indigo background (#0B0B14) with glowing indigo-to-violet-to-lilac gradient accents (#4F46E5, #8B5CF6, #C084FC) and a single warm amber glow accent, subtle thin grid lines. No text, no letters, no words, no logos. Wide composition, generous margins."

typeset -A PROMPTS
PROMPTS[best-social-media-platforms-for-realtors]="Four floating smartphone screens showing abstract social feed cards, each glowing a slightly different accent hue, arranged in an arc around a small warm house. $STYLE"
PROMPTS[what-should-real-estate-agents-blog-about]="An open notebook whose right page morphs into a glowing webpage layout, small question-mark speech bubbles floating above, a tiny house beside it. $STYLE"
PROMPTS[email-marketing-for-real-estate-agents]="A trail of glowing envelopes flying like paper planes from a small warm house toward a neat row of mailboxes. $STYLE"
PROMPTS[google-ads-for-real-estate-agents]="A large glowing search bar with soft rounded filled shapes and a small empty amber pill badge at its corner, hovering above a charming softly-lit house, a neat short stack of violet gradient coins beside the house. $STYLE"
PROMPTS[google-business-profile-posts-for-realtors]="Small update cards and photo cards pinned in a neat feed to the side of a glowing storefront-style house. $STYLE"
PROMPTS[on-page-seo-real-estate-listing-pages]="A clean webpage wireframe with glowing highlight labels on its title bar, an image block, and a link, a small house icon in the layout. $STYLE"
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
# --- New posts (photo heroes generated via gemini-3.1-flash-image, downscaled to 1200x800 JPG). ---
PROMPTS[ai-tools-for-real-estate-agents]="A friendly robotic hand offering a glowing toolbox of tiny app icons toward a small warm house, a single AI chat bubble above containing a tiny house and a spark. $STYLE"
PROMPTS[new-real-estate-agent-playbook]="A tiny glowing house sprouting like a seedling with two small leaves from its rooftop, held above fresh soil in an open hand, a sense of a new beginning. $STYLE"
PROMPTS[best-real-estate-lead-sources-reddit]="Several glowing upward arrows and small chat-bubble icons funneling and converging up into a single warm house at the top, like leads flowing toward it. $STYLE"
PROMPTS[real-estate-agent-websites-guide]="A glowing browser window framing a small warm house and a little neighborhood, with subtle structural wireframe lines suggesting a well-built site. $STYLE"
PROMPTS[real-estate-website-builders-for-agents]="Glowing modular building blocks and drag-and-drop panels assembling into a small website window that frames a house, a sense of construction. $STYLE"
PROMPTS[real-estate-postcards-guide]="Several glowing real estate postcards fanning out through the air toward a warm neighborhood of small houses, a subtle sense of direct mail in motion. $STYLE"
PROMPTS[free-real-estate-marketing-templates]="A tidy arrangement of glowing template cards, social-post graphics, and small tool icons floating around a central warm house, a free-resource toolkit feel. $STYLE"
PROMPTS[real-estate-lead-generation-guide]="Glowing lead signals and small person icons flowing along light paths from all directions into a central warm house-shaped hub, a sense of leads converging. $STYLE"
PROMPTS[real-estate-lead-magnets]="A large glowing horseshoe magnet drawing small house icons and person icons toward it through the air, clean minimal composition. $STYLE"
PROMPTS[real-estate-niche-marketing]="One glowing house singled out and spotlighted with a warm beam of light, standing out among many faint dim houses around it, a sense of focus and standing out. $STYLE"
PROMPTS[exclusive-real-estate-leads]="A single glowing person-marker icon highlighted under a soft spotlight and encircled by a gentle ring, set apart from a faint crowd of similar dim icons, a sense of one-to-one exclusivity. $STYLE"
PROMPTS[is-geo-snake-oil]="A large elegant magnifying glass inspecting a glowing AI chat bubble: under the lens one half of the bubble resolves into solid geometric building blocks, the other half drifts away as faint smoke wisps, a small warm house beside the solid blocks. $STYLE"
PROMPTS[how-to-hire-a-geo-agency]="A glowing checklist card with several confident checkmarks and one small amber warning flag on its lowest row, hovering protectively beside a small warm house, a sense of careful vetting before a handshake. $STYLE"
PROMPTS[does-ai-search-send-traffic]="A large glowing AI chat bubble with a single thin winding light path leading from it to a small warm house, beside a modest bar chart of tiny dim bars with one taller warmly glowing bar, a sense of few but valuable visits. $STYLE"
PROMPTS[expired-listings-guide]="A faded tilted for-sale yard sign being relit by a warm amber glow beside a small house, a calendar page curling away, sense of a second chance. $STYLE"
PROMPTS[real-estate-scripts]="Several glowing dialogue speech-bubble cards fanned like playing cards beside a vintage telephone handset, a small warm house in the background. $STYLE"
PROMPTS[real-estate-listing-presentation]="An elegant open presentation folder with softly glowing pages and a rising line chart, facing a small warm house across a table, sense of a confident pitch. $STYLE"
PROMPTS[closing-gifts-for-realtors]="A warmly glowing wrapped gift box with a ribbon placed on the doorstep of a charming small house, gentle sparkles, sense of gratitude. $STYLE"
PROMPTS[real-estate-farming]="A small neighborhood of houses inside a soft glowing boundary ring, one house warmly lit at the center, faint sprouting leaves at the ring's edge, sense of tending a territory. $STYLE"
PROMPTS[real-estate-branding]="A small warm house whose glowing silhouette repeats identically across several floating panels and screens of different sizes, sense of one consistent identity everywhere. $STYLE"
PROMPTS[real-estate-slogans]="An elegant glowing blank ribbon banner unfurling above a small warm house, abstract sparkles along the ribbon, completely blank ribbon with no text. $STYLE"
PROMPTS[real-estate-agent-bio]="A glowing profile card with a portrait circle and soft blank text-line placeholders, standing beside a small warm house, sense of a trustworthy introduction. $STYLE"
PROMPTS[real-estate-newsletters]="A glowing folded newsletter page emerging from an open envelope, an abstract small house shape on the page, a trail of soft envelopes behind. $STYLE"
PROMPTS[open-house-ideas-for-realtors]="A charming house with its front door open spilling warm light onto a path lined with small glowing directional yard signs, welcoming footprints approaching. $STYLE"
PROMPTS[real-estate-video-marketing]="A glowing smartphone on a small tripod filming a charming warm house, a soft play-button badge floating above, gentle spotlight. $STYLE"
PROMPTS[real-estate-referral-fees]="Two elegant glowing hands gently exchanging a small warm house token above a softly split coin, clean and balanced. $STYLE"
PROMPTS[luxury-real-estate-marketing]="A grand elegant house under one refined narrow spotlight, restrained gold accent details, deep calm negative space. $STYLE"
PROMPTS[new-construction-real-estate-agent]="A house half-assembled from glowing wireframe lines beside its finished warmly-lit twin, a subtle crane silhouette behind. $STYLE"
PROMPTS[how-do-real-estate-teams-work]="Several small glowing house tokens arranged in an orbit around one warm central house, connected by soft light lines. $STYLE"
PROMPTS[how-to-recruit-real-estate-agents]="A warm central house drawing several small glowing person markers toward it along gentle curved paths, welcoming. $STYLE"
PROMPTS[what-is-a-real-estate-isa]="A glowing headset resting beside a neat stack of contact cards and a small warm house, calm and orderly desk scene. $STYLE"
PROMPTS[buyer-agency-agreement-guide]="A glowing document with a soft pen beside two small abstract figures and a warm house, calm and reassuring. $STYLE"
PROMPTS[real-estate-name-ideas]="Several glowing blank name cards floating above a small warm house, one card lit brighter than the rest, completely blank cards with no text. $STYLE"
PROMPTS[divorce-real-estate-agent]="A house gently dividing into two soft glowing paths that curve apart kindly, handled with calm and care, no harsh imagery. $STYLE"
PROMPTS[veteran-real-estate-agent]="A warm house with a gentle abstract star emblem above the door and a path of soft glowing footsteps arriving home. $STYLE"
PROMPTS[probate-real-estate-leads]="A quiet house with a gentle glowing document and a single key resting before it, soft respectful light. $STYLE"

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
