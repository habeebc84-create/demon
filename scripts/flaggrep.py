#!/usr/bin/env python3
"""Recursively search files/directories for flag-shaped strings and 'flag' context."""
import argparse
import os
import re
import sys

FLAG_PATTERNS = [
    re.compile(rb"flag\{[^}\r\n]{1,200}\}", re.I),
    re.compile(rb"ctf\{[^}\r\n]{1,200}\}", re.I),
    re.compile(rb"hackitup\{[^}\r\n]{1,200}\}", re.I),
    re.compile(rb"htb\{[^}\r\n]{1,200}\}", re.I),
    re.compile(rb"picoCTF\{[^}\r\n]{1,200}\}", re.I),
    # generic { ... } with printable content
    re.compile(rb"[A-Za-z0-9_\-]{2,20}\{[^}\r\n]{1,200}\}"),
]
CONTEXT_RE = re.compile(rb"flag", re.I)


def is_binary(data: bytes) -> bool:
    return b"\x00" in data[:4096]


def scan_file(path: str, show_context: bool) -> list:
    hits = []
    try:
        with open(path, "rb") as f:
            data = f.read()
    except (OSError, PermissionError):
        return hits
    for pat in FLAG_PATTERNS:
        for m in pat.finditer(data):
            hits.append((path, m.group(0).decode("latin-1")))
    if show_context and not hits and CONTEXT_RE.search(data):
        # print a snippet around first 'flag' occurrence
        idx = data.lower().find(b"flag")
        snippet = data[max(0, idx - 60): idx + 120]
        hits.append((path, "CONTEXT: " + repr(snippet)))
    return hits


def main():
    ap = argparse.ArgumentParser(description="Grep files for flag-shaped strings")
    ap.add_argument("target", help="file or directory")
    ap.add_argument("-c", "--context", action="store_true", help="also show 'flag' keyword context")
    ap.add_argument("-x", "--ext", help="only scan files with this extension (e.g. txt)")
    args = ap.parse_args()

    target = args.target
    files = []
    if os.path.isfile(target):
        files = [target]
    elif os.path.isdir(target):
        for root, _, names in os.walk(target):
            for n in names:
                if args.ext and not n.lower().endswith("." + args.ext.lstrip(".")):
                    continue
                files.append(os.path.join(root, n))
    else:
        print("target not found:", target, file=sys.stderr)
        sys.exit(1)

    total = 0
    for fp in files:
        for path, val in scan_file(fp, args.context):
            print(f"{path}: {val}")
            total += 1
    print(f"\n{total} hit(s) across {len(files)} file(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
