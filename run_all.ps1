# PowerShell launcher script for Intelligent Review Router
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$PythonExe = if (Test-Path "$ScriptDir\.venv\Scripts\python.exe") {
    "$ScriptDir\.venv\Scripts\python.exe"
} else {
    "python"
}

& $PythonExe "$ScriptDir\run_all.py"

