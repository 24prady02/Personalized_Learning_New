$cf = "C:\Program Files (x86)\cloudflared\cloudflared.exe"
$logDir = "C:\Users\magnu\Downloads\Personalized_Learning_Cleaned (1)\personalized_learning_system"
# Kill any existing cloudflared to avoid duplicates
Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
$proc = Start-Process -FilePath $cf `
    -ArgumentList "tunnel","--config","C:\Users\magnu\.cloudflared\config.yml","run" `
    -RedirectStandardOutput "$logDir\cloudflared.log" `
    -RedirectStandardError  "$logDir\cloudflared.err" `
    -WindowStyle Hidden -PassThru
$proc.Id | Set-Content -Path "$logDir\.tunnel.pid" -Encoding ascii
