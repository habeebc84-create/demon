# CTF Kit — Sea of Secrets (HackitUp)

Quick reference for the individual CTF on **31 Oct 2026**.

## Folder layout

```
ctf-kit/
├── README.md
├── notes-template.md        # copy per challenge
├── challenges/              # your per-challenge notes live here
└── scripts/
    ├── flaggrep.py          # find flag-shaped strings in files/dirs
    ├── crack.py             # crypto cracker (rot/caesar/base64/xor/vigenere)
    ├── webprobe.py          # quick web recon
    ├── stego.py             # steganography pipeline
    └── forensics.py         # pcap / file forensics helpers
```

## Quick start

```bash
cd ctf-kit
python scripts/flaggrep.py ./some-dump
python scripts/crack.py "Gur dhvpx oebja sbk whzcf bire gur ynml qbt"
python scripts/webprobe.py https://target.example
python scripts/stego.py ./image.png
python scripts/forensics.py ./capture.pcap
```

## Toolchain checklist (verify tonight)

- [ ] WSL/Kali or Ubuntu reachable
- [ ] `python3 --version` && `pip list | grep -i crypto`
- [ ] `burpsuite` launches, browser proxy = 127.0.0.1:8080
- [ ] `file`, `strings`, `exiftool`, `binwalk`, `steghide`, `xxd` on PATH
- [ ] `ghidra` runs (Java installed)
- [ ] `wireshark` / `tshark` installed
- [ ] CyberChef bookmarked: https://gchq.github.io/CyberChef/
- [ ] CTF platform login works; flag format noted

## Rules reminder

- Individual only. No flag sharing, no teaming.
- Don't hammer/disrupt infra. Rate limits apply.
- Ethical scope only.

## During-event loop

1. Triage all challenges (15 min) → sort by points asc.
2. Easy Misc/Stego/Web first → momentum.
3. Medium Web/Crypto/Forensics.
4. Hard RevEng/Crypto last 2 hrs.
5. Skip if stuck >25 min; revisit with fresh eyes.
6. Document dead ends.
