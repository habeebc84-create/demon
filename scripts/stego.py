#!/usr/bin/env python3
"""Steganography pipeline: file info, strings, exif, binwalk, steghide, zsteg."""
import argparse
import os
import shutil
import subprocess
import sys

def run(cmd, timeout=120):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = (r.stdout or "") + (r.stderr or "")
        return r.returncode, out
    except FileNotFoundError:
        return -1, f"[tool not found: {cmd[0]}]"
    except subprocess.TimeoutExpired:
        return -2, "[timeout]"


def have(tool):
    return shutil.which(tool) is not None


def main():
    ap = argparse.ArgumentParser(description="Stego pipeline")
    ap.add_argument("file")
    ap.add_argument("-p", "--password", default="", help="steghide password (default empty)")
    args = ap.parse_args()
    f = args.file
    if not os.path.isfile(f):
        print("file not found:", f); sys.exit(1)

    print("=" * 60)
    print("FILE:", f)
    print("=" * 60)

    print("\n[file]")
    print(run(["file", f])[1].strip())

    print("\n[ls -l]")
    print(run(["ls", "-l", f])[1].strip())

    print("\n[strings (first 40)]")
    rc, out = run(["strings", "-a", f])
    lines = out.splitlines()
    print("\n".join(lines[:40]))
    if len(lines) > 40:
        print(f"... ({len(lines)} total strings)")

    if have("exiftool"):
        print("\n[exiftool]")
        print(run(["exiftool", f])[1].strip())
    else:
        print("\n[exiftool not installed]")

    if have("binwalk"):
        print("\n[binwalk]")
        print(run(["binwalk", f])[1].strip())
        print("\n[binwalk -e (extract to ./_extracted)]")
        rc, out = run(["binwalk", "-e", "-C", "./_extracted", f])
        print(out.strip() or "(no output)")
    else:
        print("\n[binwalk not installed]")

    # steghide (JPEG/BMP/WAV/AU)
    if have("steghide"):
        print("\n[steghide info]")
        print(run(["steghide", "info", f, "-p", args.password])[1].strip())
        outdir = "./_steghide_out"
        os.makedirs(outdir, exist_ok=True)
        print("\n[steghide extract]")
        rc, out = run(["steghide", "extract", "-sf", f, "-p", args.password, "-xf", os.path.join(outdir, "extracted.bin")])
        print(out.strip() or "(no output)")
        if os.path.isfile(os.path.join(outdir, "extracted.bin")):
            print("  -> extracted to", os.path.join(outdir, "extracted.bin"))
            print(run(["file", os.path.join(outdir, "extracted.bin")])[1].strip())
    else:
        print("\n[steghide not installed]")

    # zsteg (PNG)
    if have("zsteg"):
        print("\n[zsteg]")
        print(run(["zsteg", "-a", f])[1].strip())
    else:
        print("\n[zsteg not installed]")

    # pngcheck
    if have("pngcheck"):
        print("\n[pngcheck]")
        print(run(["pngcheck", "-v", f])[1].strip())

    # try common passwords for steghide
    if have("steghide"):
        print("\n[steghide common-password sweep]")
        for pw in ["", "password", "secret", "flag", "stego", "123456", "admin"]:
            rc, out = run(["steghide", "extract", "-sf", f, "-p", pw, "-xf", "/tmp/_sh.bin"], timeout=30)
            if rc == 0 and "wrote" in out.lower():
                print(f"  SUCCESS with password: {pw!r}")
                break
        else:
            print("  (none of common passwords worked)")

    # LSB extraction (pure Python, no zsteg needed)
    print("\n[LSB extraction (Pillow)]")
    try:
        from PIL import Image
        img = Image.open(f)
        # try each channel
        for channel in ("R", "G", "B", "A"):
            try:
                px = img.split()[{"R": 0, "G": 1, "B": 2, "A": 3}.get(channel, 0)]
            except Exception:
                continue
            bits = "".join(str(p & 1) for p in px.getdata())
            # convert bits to bytes
            out_bytes = bytearray()
            for i in range(0, len(bits) - 7, 8):
                out_bytes.append(int(bits[i:i + 8], 2))
            # find printable run
            buf = bytearray()
            runs = []
            for b in out_bytes:
                if 32 <= b < 127 or b in (9, 10, 13):
                    buf.append(b)
                else:
                    if len(buf) >= 8:
                        runs.append(bytes(buf))
                    buf = bytearray()
            if buf and len(buf) >= 8:
                runs.append(bytes(buf))
            if runs:
                print(f"  channel {channel}: found {len(runs)} text run(s)")
                for r in runs[:5]:
                    print("   ", r[:200])
    except Exception as e:
        print("  err:", e)

    print("\nDone. Check ./_extracted and ./_steghide_out.")


if __name__ == "__main__":
    main()
