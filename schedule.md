# Sea of Secrets CTF — Schedule (31 Oct 2026)

**Official event window:** 08:30 – 16:30 EDT (8 hours)
**Your machine (IST):** 18:00 (31 Oct) – 02:00 (1 Nov)
**Format:** Individual, online (Unstop platform)

## Time blocks (IST)

| Time (IST) | Time (EDT) | Block | Goal |
|---|---|---|---|
| 17:30 | 08:00 | Pre-flight | VM up, Burp proxy on, notes open, platform login checked, flag format noted |
| 18:00 | 08:30 | **START — Triage (15 min)** | Open every challenge, log title/points/category, sort by points asc |
| 18:15 | 08:45 | Easy sweep | Misc / Stego / Web (50–100 pt) — build momentum & points |
| 19:15 | 09:45 | Medium Web | SQLi, XSS, LFI, JWT, IDOR, SSTI |
| 20:15 | 10:45 | Medium Crypto | Cipher ID, CyberChef, RSA/XOR, base64 layers |
| 21:00 | 11:30 | **Break (15 min)** | Stretch, water, snack |
| 21:15 | 11:45 | Forensics | pcap, memory, file carving, metadata |
| 22:15 | 12:45 | OSINT | Reverse image, usernames, dorks, geolocation |
| 23:00 | 13:30 | **Break (15 min)** | Fresh eyes |
| 23:15 | 13:45 | Hard RevEng | strings, ltrace, Ghidra, patch & run |
| 00:15 | 14:45 | Hard Crypto | RSA params, custom ciphers, brute-force |
| 01:00 | 15:30 | Final push | Re-read descriptions/hints, retry stuck ones, try alt angles |
| 01:30 | 16:00 | Verify submissions | Re-check every submitted flag, no trailing spaces, format exact |
| 02:00 | 16:30 | **END** | Screenshot scoreboard, save notes, hydrate, sleep |

## Per-challenge micro-loop (use for every challenge)

1. Read description twice → note keywords/theme.
2. Identify category & likely technique.
3. Inspect artifact: `file`, `strings`, `exiftool`, `binwalk`.
4. Try the obvious → then escalate tools.
5. If stuck >25 min, skip and return later.
6. Document dead ends in `challenges/<name>.md`.

## Stuck escalation

- Web → Burp Repeater, all params, cookies, JWT, source map, `/robots.txt`, `/.git/`
- Crypto → CyberChef Magic, frequency analysis, common ciphers, RSA params
- Stego → `steghide extract`, `zsteg`, `binwalk -e`, LSB, audio spectrogram
- Forensics → Wireshark follow stream, `volatility` pslist, `foremost` carve
- OSINT → reverse image search, Sherlock, Google dorks, Wayback
- Rev → `strings`, `ltrace`, Ghidra decompile, patch & run

## Rules (individual — no sharing, no teaming, no infra disruption)

## Kit commands

```bash
cd ctf-kit
python scripts/flaggrep.py ./some-dump
python scripts/crack.py "ciphertext here"
python scripts/webprobe.py https://target.example
python scripts/stego.py ./image.png
python scripts/forensics.py ./capture.pcap
```
