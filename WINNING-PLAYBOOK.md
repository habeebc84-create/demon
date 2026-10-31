# 🏆 How to WIN Sea of Secrets CTF — Master Playbook

8-hour individual CTF (8:30 AM–4:30 PM EDT). Categories: Web, Crypto, Forensics, OSINT, RevEng, Stego, Misc. Goal: maximum points. Strategy > raw skill.

---

## 0. Mindset (read before start)

- **Points, not pride.** Solve easy ones first to build momentum and points. A 50-pt easy = same scoreboard value as 50 min on a 300-pt hard that you might not finish.
- **Time-box: 25 min per challenge.** If stuck, skip and return. Fresh eyes solve 80% of stuck challenges.
- **Individual = no sharing.** Don't risk disqualification.
- **Don't hammer infra.** Rate limits; one IP ban = zero points.

---

## 1. The 8-hour timeline (IST: 18:00 → 02:00)

| Block | Time (IST) | Action |
|---|---|---|
| Triage | 18:00–18:15 | Open EVERY challenge. Log title/points/category. Sort by points asc. |
| Easy sweep | 18:15–19:15 | Misc + Stego + easy Web. Target 40–50% of total points here. |
| Medium Web | 19:15–20:15 | SQLi, XSS, LFI, JWT, IDOR, SSTI, SSRF |
| Medium Crypto | 20:15–21:00 | Cipher ID, CyberChef, RSA/XOR, base64 layers |
| Break | 21:00–21:15 | Stretch, water, snack |
| Forensics | 21:15–22:15 | pcap, memory, carving, metadata |
| OSINT | 22:15–23:00 | Reverse image, usernames, dorks, geo |
| Break | 23:00–23:15 | Fresh eyes |
| Hard RevEng | 23:15–00:15 | strings, ltrace, Ghidra, patch |
| Hard Crypto | 00:15–01:00 | RSA params, custom ciphers |
| Final push | 01:00–01:30 | Re-read hints, retry stuck, alt angles |
| Verify | 01:30–02:00 | Re-check every submission (no trailing spaces, exact format) |

---

## 2. Universal workflow (per challenge)

1. **Restate the goal** — what flag format? what does it ask?
2. **List artifacts** — files, URLs, ports, strings, hints.
3. **Basic observations** — file types, obvious strings, errors, patterns.
4. **Pick ONE direction** based on evidence, not familiarity.
5. **Test one idea** — change one variable at a time.
6. **Record** — what you tried, why, result, learning.
7. **Adjust** — continue, pivot, or ask (hint).
8. **Verify** — flag matches format, explainable from evidence.

**Golden rule:** change ONE thing at a time. Otherwise you don't know what worked.

---

## 3. Category playbooks (fast paths to flags)

### Web
- View source, check cookies/localStorage, Network tab.
- Try: SQLi (`' OR 1=1--`), LFI (`../../../etc/passwd`), SSTI (`{{7*7}}`), JWT `alg:none`, IDOR (change IDs), SSRF, command injection (`;id`, `%0a`).
- Check `/robots.txt`, `/.git/HEAD`, `/.env`, source maps, `/admin`, `/api`.
- Tools: Burp Repeater, ffuf, sqlmap, curl.
- **Winning move:** read the source map; many flags hide in JS bundles.

### Crypto
- Identify cipher: frequency analysis, known plaintext, magic bytes.
- CyberChef "Magic" first. Then dcode.fr, factorDB.
- RSA: small e, common modulus, Wiener attack, factor via factorDB.
- XOR: single-byte (score by English), repeating-key (try key lengths).
- Vigenere: try key guesses from theme words.
- Base64 layers: decode until plaintext.
- **Winning move:** challenge title/theme often = key or cipher name.

### Forensics
- `file`, `strings`, `exiftool`, `binwalk -e`, `foremost`.
- pcap: Wireshark follow HTTP stream, extract objects, check DNS/FTP.
- Memory: volatility pslist/netscan/filescan.
- **Winning move:** `strings | grep -i flag`, check deleted files, carved images.

### OSINT
- Reverse image search (Google, TinEye, Yandex).
- Username enumeration (Sherlock), email → socials.
- Google dorks: `site:`, `filetype:`, `intext:`.
- EXIF geolocation, Wayback Machine.
- **Winning move:** challenge author's name/handle → social profiles → flag.

### Reverse Engineering
- `strings binary`, run it, `ltrace`/`strace`.
- Ghidra decompile; look for strcmp/memcmp with the flag.
- Patch or emulate.
- **Winning move:** often the flag is a hardcoded string or simple XOR in main.

### Steganography
- `steghide extract` (try empty + common passwords), `zsteg` (PNG), `stegsolve`.
- LSB extraction, audio spectrograms, trailing data after EOF.
- `binwalk -e`, check image dimensions for hidden rows.
- **Winning move:** check the LEAST significant bits of each channel; check appended ZIPs (`binwalk`).

### Misc
- Often a puzzle: base64 chains, QR codes, esoteric langs, zip bombs, git history.
- `git log`, `git fsck`, check `.git/`.

---

## 4. Tools quick reference (run in WSL)

| Task | Command |
|---|---|
| File type | `file x` |
| Strings | `strings -a -n 6 x` |
| Metadata | `exiftool x` |
| Carve | `binwalk -e x` / `foremost -i x` |
| Stego extract | `steghide extract -sf x -p ""` |
| PNG LSB | `zsteg -a x` |
| Hex dump | `xxd x | head` |
| pcap HTTP | `tshark -r x -Y http -T fields -e ...` |
| Extract HTTP objs | `tshark -r x --export-objects http,outdir` |
| Memory | `volatility -f x imageinfo` |
| Web recon | `python3 scripts/webprobe.py URL` |
| Crypto | `python3 scripts/crack.py "cipher"` |
| Flag search | `python3 scripts/flaggrep.py dir` |
| Stego pipeline | `python3 scripts/stego.py file` |
| Forensics | `python3 scripts/forensics.py file` |

---

## 5. Winning tactics (the edge)

1. **Read the description TWICE.** Authors hide hints in titles, flavor text, file names.
2. **Theme = key.** "Sea of Secrets" → maritime words, nautical terms as passwords/keys.
3. **Easy first.** Scoreboard position early = confidence + time for hard ones.
4. **Note everything.** Dead ends are data; don't repeat them.
5. **Take breaks.** 10 min every 90 min; fresh eyes solve stuck crypto/reveng.
6. **Cross-category.** A stego image may hide a crypto key; a forensics pcap may contain a web flag.
7. **Check the simple.** `strings`, `file`, `exiftool` solve ~30% of challenges in 30 seconds.
8. **Ask for hints** (politely, with context) if completely stuck — organizers often nudge.
9. **Verify submissions.** Exact flag format, no trailing spaces/newlines.
10. **Last 30 min:** re-read ALL unsolved descriptions; many click with full context.

---

## 6. Common mistakes to avoid

- Skipping enumeration → jumping to exploits.
- Ignoring error messages (they reveal DB/file paths).
- Overcomplicating — many challenges have a simple solution. Start basic.
- Changing multiple variables at once.
- Not taking notes → repeating failed ideas.
- Reading writeups immediately → you get the flag but miss the skill (and risk).
- Hammering infra → rate limits / bans.

---

## 7. If stuck (reset checklist)

- Re-read the prompt.
- Write only confirmed facts; separate from guesses.
- Check category + title again.
- Inspect simplest artifact first.
- Try a smaller version of the problem.
- Explain theory out loud / in notes.
- Take a 5-min break.
- Ask for a hint with context ("I tried X, got Y, expected Z").

---

## 8. Post-event

- Screenshot scoreboard.
- Save all notes to `challenges/`.
- Push to GitHub: `git add -A && git commit -m "ctf results" && git push`.
- Review unsolved via writeups later (learn, don't just collect flags).

---

## Quick reference: flag format
Likely `hackitup{...}` or `flag{...}`. Confirm on platform at start. Submit exact strings.

---

**Remember:** 8 hours is plenty. Consistency + triage + notes = winning. You've got this. 🏴‍☠️
```