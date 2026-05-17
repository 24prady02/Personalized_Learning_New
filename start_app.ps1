$projectDir = "C:\Users\magnu\Downloads\Personalized_Learning_Cleaned (1)\personalized_learning_system"
$python = "C:\Users\magnu\AppData\Local\Programs\Python\Python310\python.exe"
$script = "$projectDir\scripts\cpal_chat_app.py"
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
