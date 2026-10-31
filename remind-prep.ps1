Add-Type -AssemblyName System.Windows.Forms
# Auto-launch the CTF workspace
& "H:\opencode\2027\ctf-kit\launch.ps1"
# Then notify
[System.Windows.Forms.MessageBox]::Show('Sea of Secrets CTF starts in 30 min (18:00 IST). Workspace launched: VM/Burp/notes/platform. Complete the checklist.', 'CTF Reminder - Prep') | Out-Null
