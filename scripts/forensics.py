#!/usr/bin/env python3
"""Forensics helpers: file triage, strings, pcap extraction via tshark."""
import argparse
import os
import shutil
import subprocess
import sys

def run(cmd, timeout=180):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except FileNotFoundError:
        return -1, f"[tool not found: {cmd[0]}]"
    except subprocess.TimeoutExpired:
        return -2, "[timeout]"


def have(t): return shutil.which(t) is not None


def main():
    ap = argparse.ArgumentParser(description="Forensics helpers")
    ap.add_argument("file")
    args = ap.parse_args()
    f = args.file
    if not os.path.isfile(f):
        print("file not found:", f); sys.exit(1)

    print("=" * 60)
    print("FILE:", f)
    print("=" * 60)

    print("\n[file]")
    print(run(["file", f])[1].strip())
    print("\n[size]")
    print(os.path.getsize(f), "bytes")

    # strings
    rc, out = run(["strings", "-a", "-n", "6", f])
    lines = out.splitlines()
    print(f"\n[strings count={len(lines)}; first 60]")
    print("\n".join(lines[:60]))

    # grep flag-like in strings
    import re
    print("\n[flag-like strings]")
    for ln in lines:
        if re.search(r"flag|ctf|hackitup|\{", ln, re.I):
            print("  ", ln)

    # exiftool
    if have("exiftool"):
        print("\n[exiftool]")
        print(run(["exiftool", f])[1].strip())

    # binwalk
    if have("binwalk"):
        print("\n[binwalk]")
        print(run(["binwalk", f])[1].strip())

    # pcap handling
    ext = os.path.splitext(f)[1].lower()
    if ext in (".pcap", ".pcapng", ".cap") or have("tshark"):
        if have("tshark"):
            print("\n[tshark protocols]")
            print(run(["tshark", "-r", f, "-q", "-z", "io,phs"])[1].strip())
            print("\n[tshark http requests]")
            rc, out = run(["tshark", "-r", f, "-Y", "http.request", "-T", "fields",
                           "-e", "ip.src", "-e", "http.host", "-e", "http.request.method", "-e", "http.request.uri"])
            print(out.strip() or "(none)")
            print("\n[tshark credentials-ish]")
            rc, out = run(["tshark", "-r", f, "-Y", "http.authorization || ftp.request.command", "-T", "fields",
                           "-e", "ip.src", "-e", "http.authorization", "-e", "ftp.request.arg"])
            print(out.strip() or "(none)")
            # extract http objects
            outdir = "./_http_objects"
            os.makedirs(outdir, exist_ok=True)
            rc, out = run(["tshark", "-r", f, "--export-objects", f"http,{outdir}"])
            print("\n[exported http objects ->", outdir, "]")
            print(out.strip() or "(none)")
            if os.path.isdir(outdir):
                for n in os.listdir(outdir):
                    print("   ", n)
        else:
            print("\n[tshark not installed]")

    # volatility hint
    print("\n[volatility hint] if this is a memory dump, run:")
    print("  volatility -f", f, "imageinfo")
    print("  volatility -f", f, "pslist / netscan / filescan")

    print("\nDone.")


if __name__ == "__main__":
    main()
