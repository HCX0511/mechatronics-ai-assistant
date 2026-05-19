$env:APP_HOST = "0.0.0.0"
$env:APP_PORT = "5000"
$env:FLASK_DEBUG = "false"

Set-Location $PSScriptRoot

Write-Host "Starting Flask server for LAN access..." -ForegroundColor Green
Write-Host "Local:   http://127.0.0.1:5000"
Write-Host "LAN IP:  http://10.87.120.219:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Keep this window open while others are visiting your site." -ForegroundColor Yellow

& "C:\Users\86189\AppData\Local\Programs\Python\Python314\python.exe" "app.py"
