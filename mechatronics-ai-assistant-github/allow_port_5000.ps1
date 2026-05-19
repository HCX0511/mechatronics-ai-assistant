Write-Host "Adding Windows Firewall rule for TCP port 5000..." -ForegroundColor Green
Write-Host "If this fails, please reopen PowerShell as Administrator and run this script again." -ForegroundColor Yellow

netsh advfirewall firewall add rule name="mechatronics-ai-assistant-5000" dir=in action=allow protocol=TCP localport=5000
