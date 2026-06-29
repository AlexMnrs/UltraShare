# Packaging UltraShare

UltraShare can be packaged as a Windows executable with PyInstaller. This is useful for testers and non-technical users who do not want to run the app from source.

## Build from a clean checkout

Use Windows with Python 3.10 or newer.

```powershell
git clone https://github.com/AlexMnrs/UltraShare.git
cd UltraShare
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.\scripts\build-windows.ps1
```

The executable is written to:

```text
dist\UltraShare.exe
```

## Manual build command

The build script runs this PyInstaller command:

```powershell
python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onefile `
  --name UltraShare `
  --collect-data customtkinter `
  main.py
```

`--collect-data customtkinter` is included because CustomTkinter ships theme assets that must be bundled with the executable.

## Release checklist

Before publishing a downloadable release:

- Build the executable on Windows.
- Start `dist\UltraShare.exe`.
- Confirm the control panel opens.
- Confirm the overlay frame appears.
- Confirm the window list refreshes.
- Snap a normal application window into the overlay region.
- Move the overlay and confirm the snapped window stays aligned.
- Test at least one elevated-window limitation and document the result.
- Upload the executable to a GitHub Release with short release notes.

## Current status

The repository now documents the packaging path, but there is not yet an official downloadable release artifact. Until a release is published, users should run UltraShare from source.
