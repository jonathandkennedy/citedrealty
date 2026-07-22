#!/usr/bin/env python3
"""
submit_indexnow.py — tell IndexNow (Bing, Yandex, Seznam, Naver, …) to crawl new/changed pages now.

WHY THIS EXISTS: ChatGPT web search runs on Bing's index, so fast Bing indexing is a
prerequisite for some of the AI citations CitedRealty sells (see HANDOFF §10). IndexNow
pushes a URL to participating engines the moment it changes, instead of waiting days for a
scheduled crawl. Submitting to one endpoint fans out to all of them.

USAGE
    python3 submit_indexnow.py                     # submit every URL in sitemap.xml
    python3 submit_indexnow.py <url> [<url> ...]    # submit only the given URLs (after editing a few pages)
    python3 submit_indexnow.py --dry-run [urls...]  # print what would be sent, submit nothing

RUN IT *AFTER* THE DEPLOY IS LIVE. IndexNow verifies ownership by fetching the key file at
KEY_LOCATION, so the key file must already be reachable on citedrealty.com (i.e. pushed and
deployed by Vercel) or the engines will reject the submission.

THE KEY IS PUBLIC BY DESIGN. IndexNow requires the key to be hosted openly at the site root,
so 78f577...txt and the value below are meant to be committed and public — this is NOT a
secret like the Gemini/OpenAI API keys.
"""

import sys
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

HOST = "citedrealty.com"
KEY = "78f577af8eab42e2a0aa8001fe3ffc5d"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
# Vendor-neutral endpoint; it shares submissions with Bing, Yandex, Seznam, Naver, etc.
# Swap to "https://www.bing.com/indexnow" if you ever want to target Bing directly.
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP = Path(__file__).parent / "sitemap.xml"


def urls_from_sitemap():
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    tree = ET.parse(SITEMAP)
    return [loc.text.strip() for loc in tree.findall(".//sm:loc", ns) if loc.text]


def submit(urls):
    payload = {"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    urls = [a for a in args if a != "--dry-run"] or urls_from_sitemap()

    # IndexNow rejects a batch whose URLs are not all on the declared host.
    bad = [u for u in urls if not u.startswith(f"https://{HOST}/")]
    if bad:
        sys.exit(f"Refusing to submit — these URLs are not on https://{HOST}/:\n  " + "\n  ".join(bad))

    print(f"{len(urls)} URL(s) to submit:")
    for u in urls:
        print(f"  {u}")
    if dry_run:
        print("\n--dry-run: nothing sent.")
        return

    print(f"\nSubmitting to {ENDPOINT} …")
    try:
        status, body = submit(urls)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        # 403 = key file missing/mismatched; 422 = URL/key host mismatch.
        sys.exit(f"IndexNow returned HTTP {e.code}: {body or '(no body)'}")
    except urllib.error.URLError as e:
        sys.exit(f"Network error reaching IndexNow: {e.reason}")

    # 200 = accepted; 202 = accepted, key validation pending. Both are success.
    ok = status in (200, 202)
    print(f"HTTP {status} — {'OK' if ok else 'unexpected response'}")
    if body:
        print(body)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
