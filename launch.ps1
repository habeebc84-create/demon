# launch.ps1 - Auto-open the CTF workspace at pre-flight time
$Kit = "H:\opencode\2027\ctf-kit"
$Platform = "https://unstop.com/hackathons/sea-of-secrets-ctf-hackitup-1764913"
$CyberChef = "https://gchq.github.io/CyberChef/"

Write-Host "=== Sea of Secrets CTF - Launching workspace ===" -ForegroundColor Cyan

# 1. Open kit folder in Explorer
Start-Process explorer.exe $Kit

# 2. Open notes folder
$notes = Join-Path $Kit "challenges"
if (-not (Test-Path $notes)) { New-Item -ItemType Directory -Path $notes | Out-Null }
Start-Process explorer.exe $notes

# 3. Open terminal in kit dir
$wt = Get-Command wt.exe -ErrorAction SilentlyContinue
if ($wt) {
    Start-Process wt.exe -ArgumentList "-d `"$Kit`""
} else {
    Start-Process powershell.exe -ArgumentList "-NoExit -Command `"cd '$Kit'`""
}

# 4. Open browser tabs: platform + CyberChef
Start-Process $Platform
Start-Sleep -Milliseconds 800
Start-Process $CyberChef

# 5. Try to launch Burp Suite if installed
$burpCandidates = @(
    "C:\Program Files\BurpSuiteCommunity\BurpSuiteCommunity.exe",
    "C:\Program Files\Burp Suite Community Edition\BurpSuiteCommunity.exe",
    "$env:LOCALAPPDATA\Programs\BurpSuiteCommunity\BurpSuiteCommunity.exe"
)
$burp = $burpCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($burp) {
    Start-Process $burp
    Write-Host "Burp Suite launched." -ForegroundColor Green
} else {
    Write-Host "Burp Suite not found - start it manually." -ForegroundColor Yellow
}

# 6. Try to open WSL (Kali/Ubuntu) terminal
$wsl = Get-Command wsl.exe -ErrorAction SilentlyContinue
if ($wsl) {
    Start-Process wsl.exe
    Write-Host "WSL launched." -ForegroundColor Green
} else {
    Write-Host "WSL not found - use your VM manually." -ForegroundColor Yellow
}

# 7. Print checklist
Write-Host ""
Write-Host "PRE-FLIGHT CHECKLIST:" -ForegroundColor Cyan
@(
    "VM/WSL reachable",
    "Burp proxy = 127.0.0.1:8080 in browser",
    "python3 + Crypto libs OK",
    "file/strings/exiftool/binwalk/steghide on PATH",
    "Ghidra runs",
    "Wireshark/tshark installed",
    "Platform login works; flag format noted",
    "notes-template copied per challenge"
) | ForEach-Object { Write-Host "  [ ] $_" }

Write-Host ""
Write-Host "Kit: $Kit" -ForegroundColor Green
