#!/usr/bin/env python3
"""Multi-technique crypto cracker: rot/caesar/base64/xor/vigenere/atbash."""
import argparse
import base64
import itertools
import string

ENGLISH_FREQ = "etaoinshrdlcumwfgypbvkjxqz"


def score_text(s: str) -> float:
    s = s.lower()
    score = 0.0
    for ch in s:
        if ch in ENGLISH_FREQ:
            score += (26 - ENGLISH_FREQ.index(ch)) / 26.0
        elif ch in " \n.,'\"-!?":
            score += 0.5
        elif ch.isprintable():
            score += 0.1
        else:
            score -= 5.0
    # word-ish bonus
    for w in ("the", "and", "flag", "is", "of", "to", "a"):
        score += s.count(w) * 2
    return score


def try_rot(text, n):
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr((ord(ch) - base + n) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def caesar_brute(text):
    res = []
    for n in range(1, 26):
        cand = try_rot(text, n)
        res.append((score_text(cand), n, cand))
    res.sort(reverse=True)
    return res[:5]


def atbash(text):
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr(base + 25 - (ord(ch) - base)))
        else:
            out.append(ch)
    return "".join(out)


def base64_layers(text, depth=4):
    out = [text]
    cur = text
    for i in range(depth):
        try:
            dec = base64.b64decode(cur, validate=False).decode("utf-8", errors="replace")
        except Exception:
            break
        if dec == cur:
            break
        out.append(dec)
        cur = dec
    return out


def single_byte_xor(data: bytes):
    res = []
    for key in range(256):
        dec = bytes(b ^ key for b in data)
        try:
            s = dec.decode("utf-8")
        except UnicodeDecodeError:
            s = dec.decode("latin-1")
        res.append((score_text(s), key, s))
    res.sort(reverse=True)
    return res[:8]


def repeating_xor(data: bytes, maxkey=20):
    best = []
    for kl in range(1, maxkey + 1):
        # break into kl groups
        groups = [bytearray() for _ in range(kl)]
        for i, b in enumerate(data):
            groups[i % kl].append(b)
        key = bytearray()
        ok = True
        for g in groups:
            r = single_byte_xor(bytes(g))
            if not r:
                ok = False
                break
            key.append(r[0][1])
        if not ok:
            continue
        dec = bytes(data[i] ^ key[i % kl] for i in range(len(data)))
        try:
            s = dec.decode("utf-8")
        except UnicodeDecodeError:
            s = dec.decode("latin-1")
        best.append((score_text(s), kl, bytes(key), s))
    best.sort(reverse=True)
    return best[:5]


def vigenere(text, key):
    out = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            shift = ord(key[ki % len(key)].lower()) - ord("a")
            out.append(chr((ord(ch) - base - shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="Crypto cracker")
    ap.add_argument("text", nargs="?", help="ciphertext string (or use -f file)")
    ap.add_argument("-f", "--file", help="read input from file (raw bytes)")
    ap.add_argument("-k", "--key", help="vigenere key to try")
    args = ap.parse_args()

    if args.file:
        with open(args.file, "rb") as fh:
            raw = fh.read()
        text = raw.decode("latin-1")
        data = raw
    else:
        text = args.text or ""
        data = text.encode("latin-1")

    print("=" * 60)
    print("INPUT:", repr(text[:200]))
    print("=" * 60)

    # Atbash
    print("\n[Atbash]")
    print(atbash(text))

    # Caesar / ROT
    print("\n[Caesar/ROT top-5]")
    for sc, n, cand in caesar_brute(text):
        print(f"  shift={n:2d} score={sc:6.2f} -> {cand[:120]}")

    # ROT13
    print("\n[ROT13]")
    print(try_rot(text, 13))

    # Base64 layers
    print("\n[Base64 layers]")
    for i, layer in enumerate(base64_layers(text.strip())):
        print(f"  layer {i}: {layer[:200]}")

    # Single-byte XOR
    print("\n[Single-byte XOR top-8]")
    for sc, key, s in single_byte_xor(data):
        print(f"  key=0x{key:02x} ({key:3d}) score={sc:6.2f} -> {s[:120]}")

    # Repeating XOR
    print("\n[Repeating-key XOR top-5]")
    for sc, kl, key, s in repeating_xor(data):
        print(f"  keylen={kl} key={key!r} score={sc:6.2f} -> {s[:120]}")

    # Vigenere (if key given)
    if args.key:
        print(f"\n[Vigenere key={args.key}]")
        print(vigenere(text, args.key))

    # hex / binary decode attempts
    print("\n[Hex decode (if hex)]")
    try:
        h = text.strip().replace(" ", "").replace("\n", "")
        if all(c in "0123456789abcdefABCDEF" for c in h) and len(h) % 2 == 0 and len(h) > 4:
            dec = bytes.fromhex(h).decode("utf-8", errors="replace")
            print("  ", dec[:300])
    except Exception as e:
        print("  err:", e)

    print("\n[Binary decode (if 0/1)]")
    t = text.strip().replace(" ", "").replace("\n", "")
    if t and all(c in "01" for c in t) and len(t) % 8 == 0:
        try:
            dec = "".join(chr(int(t[i:i + 8], 2)) for i in range(0, len(t), 8))
            print("  ", dec[:300])
        except Exception as e:
            print("  err:", e)


if __name__ == "__main__":
    main()
