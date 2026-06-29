$ErrorActionPreference = "Stop"

$python = if ($env:PYTHON) { $env:PYTHON } else { "python" }

& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt -r requirements-dev.txt

& $python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onefile `
  --name UltraShare `
  --collect-data customtkinter `
  main.py

Write-Host "Build complete: dist\UltraShare.exe"
