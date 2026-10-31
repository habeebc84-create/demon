# setup.ps1 - Auto-check/install the CTF toolchain and report status
$Kit = "H:\opencode\2027\demon"
Write-Host "=== CTF Toolchain Setup / Check ===" -ForegroundColor Cyan

function Has($name) { [bool](Get-Command $name -ErrorAction SilentlyContinue) }

# Python packages
$pyPkgs = @("requests","pwntools","pycryptodome","Pillow","zsteg")
$py = Get-Command python -ErrorAction SilentlyContinue
if ($py) {
    Write-Host "Python: $($py.Source)" -ForegroundColor Green
    foreach ($p in @("requests","Crypto","PIL")) {
        python -c "import $p; print('  OK $p')" 2>$null
        if ($LASTEXITCODE -ne 0) { Write-Host "  MISSING $p  -> pip install ..." -ForegroundColor Yellow }
    }
    # install requests if missing
    python -c "import requests" 2>$null
    if ($LASTEXITCODE -ne 0) { python -m pip install requests --quiet }
} else {
    Write-Host "Python NOT FOUND" -ForegroundColor Red
}

# Binaries
$bins = @("file","strings","exiftool","binwalk","steghide","xxd","tshark","ghidra")
foreach ($b in $bins) {
    if (Has $b) { Write-Host "  OK  $b" -ForegroundColor Green }
    else { Write-Host "  MISS $b" -ForegroundColor Yellow }
}

# WSL
if (Has "wsl") { Write-Host "  OK  wsl" -ForegroundColor Green } else { Write-Host "  MISS wsl" -ForegroundColor Yellow }

# Burp
$burp = @("C:\Program Files\BurpSuiteCommunity\BurpSuiteCommunity.exe","C:\Program Files\Burp Suite Community Edition\BurpSuiteCommunity.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($burp) { Write-Host "  OK  burp: $burp" -ForegroundColor Green } else { Write-Host "  MISS burp" -ForegroundColor Yellow }

# WSL/Kali tools
Write-Host ""
Write-Host "WSL/Kali tools:" -ForegroundColor Cyan
$wslTools = @("binwalk","steghide","exiftool","tshark","file","strings","python3")
foreach ($t in $wslTools) {
    $r = wsl -d kali-linux -u root bash -c "command -v $t" 2>$null
    if ($r) { Write-Host "  OK  $t  ($r)" -ForegroundColor Green }
    else { Write-Host "  MISS $t" -ForegroundColor Yellow }
}
$pyr = wsl -d kali-linux -u root python3 -c "import Crypto,requests,PIL,pwn; print('py libs OK')" 2>&1
if ($pyr -match "py libs OK") { Write-Host "  OK  python libs (Crypto,requests,PIL,pwn)" -ForegroundColor Green } else { Write-Host "  MISS python libs: $pyr" -ForegroundColor Yellow }

Write-Host ""
Write-Host "Run 'pip install requests pwntools pycryptodome Pillow' inside WSL/Python env." -ForegroundColor Cyan
Write-Host "Kit: $Kit" -ForegroundColor Green
