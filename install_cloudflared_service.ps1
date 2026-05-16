# Installs the cloudflared named tunnel (tutor.cpaltutor.com -> localhost:7860)
# as a Windows service so it survives reboots / logout / closing Cursor.
# RUN THIS IN AN ELEVATED (Administrator) POWERSHELL.

$ErrorActionPreference = "Stop"

# --- 0. must be elevated ---
$elevated = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
            ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $elevated) {
    Write-Host "ERROR: not running as Administrator. Right-click PowerShell -> Run as administrator, then re-run this." -ForegroundColor Red
    exit 1
}

$cf       = "C:\Program Files (x86)\cloudflared\cloudflared.exe"
$tunnelId = "15a21901-7f50-4d42-bbb1-dde60d0db44f"
$userDir  = "C:\Users\magnu\.cloudflared"
$sysDir   = "C:\Windows\System32\config\systemprofile\.cloudflared"

# --- 1. stage config + credentials where the LocalSystem service will find them ---
New-Item -ItemType Directory -Force -Path $sysDir | Out-Null
Copy-Item "$userDir\$tunnelId.json" "$sysDir\$tunnelId.json" -Force
Copy-Item "$userDir\cert.pem"       "$sysDir\cert.pem"       -Force

# config.yml with credentials-file repointed at the systemprofile copy
@"
tunnel: $tunnelId
credentials-file: $sysDir\$tunnelId.json

ingress:
  - hostname: tutor.cpaltutor.com
    service: http://localhost:7860
  - service: http_status:404
"@ | Set-Content -Path "$sysDir\config.yml" -Encoding ascii
Write-Host "Staged config + credentials in $sysDir" -ForegroundColor Green

# --- 2. install + start the service ---
if (Get-Service -Name "cloudflared" -ErrorAction SilentlyContinue) {
    Write-Host "Service already exists - skipping install." -ForegroundColor Yellow
} else {
    & $cf service install
    Write-Host "Service installed." -ForegroundColor Green
}
Set-Service -Name "cloudflared" -StartupType Automatic
Start-Service -Name "cloudflared"
Start-Sleep -Seconds 8

# --- 3. stop any manually-started cloudflared so we don't run duplicates ---
Get-CimInstance Win32_Process -Filter "Name='cloudflared.exe'" |
    Where-Object { $_.CommandLine -notmatch "system32" } |
    ForEach-Object {
        Write-Host "Stopping manual cloudflared PID $($_.ProcessId)" -ForegroundColor Yellow
        Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
    }

# --- 4. verify ---
Write-Host ""
Get-Service cloudflared | Format-Table Name, Status, StartType -AutoSize
try {
    $r = Invoke-WebRequest -Uri "https://tutor.cpaltutor.com" -UseBasicParsing -TimeoutSec 20
    Write-Host "https://tutor.cpaltutor.com -> HTTP $($r.StatusCode)  ($($r.Content.Length) bytes)  OK" -ForegroundColor Green
} catch {
    Write-Host "Public URL check failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "(If the Gradio app on port 7860 is down you'll get 502 - that's separate from the tunnel.)"
}
