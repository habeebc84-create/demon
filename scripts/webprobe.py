#!/usr/bin/env python3
"""Quick web recon: headers, title, common paths, robots, sitemap, .git, source maps."""
import argparse
import re
import sys

try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print("pip install requests", file=sys.stderr)
    sys.exit(1)

COMMON_PATHS = [
    "robots.txt", "sitemap.xml", ".git/HEAD", ".env", "admin", "login",
    "api", "swagger.json", "openapi.json", "package.json", "config.js",
    "backup.zip", "backup.tar.gz", ".DS_Store",
]


def fetch(url):
    try:
        r = requests.get(url, timeout=10, verify=False, allow_redirects=True)
        return r
    except Exception as e:
        return e


def main():
    ap = argparse.ArgumentParser(description="Quick web recon")
    ap.add_argument("url")
    args = ap.parse_args()
    base = args.url.rstrip("/")

    print("=" * 60)
    print("TARGET:", base)
    print("=" * 60)

    r = fetch(base)
    if isinstance(r, Exception):
        print("ERR fetching base:", r)
        return
    print("\n[Status]", r.status_code)
    print("[Final URL]", r.url)
    print("\n[Headers]")
    for k, v in r.headers.items():
        print(f"  {k}: {v}")

    m = re.search(r"<title[^>]*>(.*?)</title>", r.text, re.I | re.S)
    print("\n[Title]", m.group(1).strip() if m else "(none)")

    # cookies
    if r.cookies:
        print("\n[Cookies]")
        for c in r.cookies:
            print("  ", c.name, "=", c.value)

    # common paths
    print("\n[Common paths]")
    for p in COMMON_PATHS:
        rr = fetch(base + "/" + p)
        if isinstance(rr, Exception):
            print(f"  {p}: ERR {rr}")
            continue
        status = rr.status_code
        marker = "  " if status >= 400 else ">>"
        print(f"  {marker} {p}: {status} ({len(rr.content)} bytes)")

    # source maps
    for m in re.finditer(r"sourceMappingURL=([^\s]+)", r.text):
        print("\n[Source map ref]", m.group(1))

    # forms
    forms = re.findall(r"<form[^>]*>.*?</form>", r.text, re.I | re.S)
    if forms:
        print(f"\n[Forms found: {len(forms)}]")
        for f in forms[:5]:
            print("  ", f[:200].replace("\n", " "))

    # hidden inputs
    hidden = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*>', r.text, re.I)
    if hidden:
        print(f"\n[Hidden inputs: {len(hidden)}]")
        for h in hidden:
            print("  ", h)


if __name__ == "__main__":
    main()
