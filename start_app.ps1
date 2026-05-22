$projectDir = "C:\Users\magnu\Downloads\Personalized_Learning_Cleaned (1)\personalized_learning_system"
$python = "C:\Users\magnu\AppData\Local\Programs\Python\Python310\python.exe"
$script = "$projectDir\scripts\cpal_chat_app.py"

# Log rotation (added 2026-05-21). Cap the chat-app log at 50 MB and
# keep the last 3 rotations as .1 .2 .3. Without this, cpal_chat_app.log
# grows unbounded — at ~1 MB / 100 student turns it would silently fill
# the disk in production.
function Rotate-Log($path, $maxMB, $keep) {
    if (-not (Test-Path $path)) { return }
    $sizeMB = (Get-Item $path).Length / 1MB
    if ($sizeMB -lt $maxMB) { return }
    for ($i = $keep; $i -gt 0; $i--) {
        $src = "$path." + ($i - 1)
        $dst = "$path." + $i
        if ($i -eq 1) { $src = $path }
        if (Test-Path $src) {
            if (Test-Path $dst) { Remove-Item $dst -Force -ErrorAction SilentlyContinue }
            Move-Item $src $dst -Force -ErrorAction SilentlyContinue
        }
    }
}
Rotate-Log "$projectDir\cpal_chat_app.log"     50 3
Rotate-Log "$projectDir\cpal_chat_app.log.err" 50 3

# Kill any previously-launched app, but only ones running this script (don't nuke unrelated python)
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match "cpal_chat_app\.py" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 1
$proc = Start-Process -FilePath $python `
    -ArgumentList "`"$script`"" `
    -WorkingDirectory $projectDir `
    -RedirectStandardOutput "$projectDir\cpal_chat_app.log" `
    -RedirectStandardError  "$projectDir\cpal_chat_app.log.err" `
    -WindowStyle Hidden -PassThru
$proc.Id | Set-Content -Path "$projectDir\.app.pid" -Encoding ascii
