$projectDir = "C:\Users\magnu\Downloads\Personalized_Learning_Cleaned (1)\personalized_learning_system"
$docsDir = "$projectDir\docs"
$python  = "C:\Users\magnu\AppData\Local\Programs\Python\Python310\python.exe"

# Serves docs/ on localhost:8765 so the cloudflared ingress rule
#   path ^/wireframe(/.*)?$  ->  http://localhost:8765
# resolves. Root MUST be docs/ (NOT docs/wireframe/) because cloudflared
# forwards the FULL /wireframe/... path to the origin. Added 2026-06-07
# to make tutor.cpaltutor.com/wireframe a persistent link (previously the
# server was started by hand and died on logout/reboot).

# Log rotation — cap at 50 MB, keep last 3. Mirrors start_app.ps1.
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
Rotate-Log "$projectDir\docs_server.log" 50 3
Rotate-Log "$projectDir\docs_server.err" 50 3

# Kill any previously-launched docs server (only ones serving 8765).
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match "http\.server 8765" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 1

$proc = Start-Process -FilePath $python `
    -ArgumentList "-m","http.server","8765","--bind","127.0.0.1","--directory","`"$docsDir`"" `
    -WorkingDirectory $docsDir `
    -RedirectStandardOutput "$projectDir\docs_server.log" `
    -RedirectStandardError  "$projectDir\docs_server.err" `
    -WindowStyle Hidden -PassThru
$proc.Id | Set-Content -Path "$projectDir\.docs.pid" -Encoding ascii
