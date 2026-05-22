$cf = "C:\Program Files (x86)\cloudflared\cloudflared.exe"
$logDir = "C:\Users\magnu\Downloads\Personalized_Learning_Cleaned (1)\personalized_learning_system"

# Log rotation (added 2026-05-21) — see start_app.ps1 for rationale.
function Rotate-Log($path, $maxMB, $keep) {
    if (-not (Test-Path $path)) { return }
    if (((Get-Item $path).Length / 1MB) -lt $maxMB) { return }
    for ($i = $keep; $i -gt 0; $i--) {
        $src = "$path." + ($i - 1); $dst = "$path." + $i
        if ($i -eq 1) { $src = $path }
        if (Test-Path $src) {
            if (Test-Path $dst) { Remove-Item $dst -Force -ErrorAction SilentlyContinue }
            Move-Item $src $dst -Force -ErrorAction SilentlyContinue
        }
    }
}
Rotate-Log "$logDir\cloudflared.log" 50 3
Rotate-Log "$logDir\cloudflared.err" 50 3

# Kill any existing cloudflared to avoid duplicates
Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
$proc = Start-Process -FilePath $cf `
    -ArgumentList "tunnel","--config","C:\Users\magnu\.cloudflared\config.yml","run" `
    -RedirectStandardOutput "$logDir\cloudflared.log" `
    -RedirectStandardError  "$logDir\cloudflared.err" `
    -WindowStyle Hidden -PassThru
$proc.Id | Set-Content -Path "$logDir\.tunnel.pid" -Encoding ascii
