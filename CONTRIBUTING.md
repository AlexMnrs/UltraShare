# Contributing to UltraShare

Thanks for considering a contribution to UltraShare.

UltraShare is a Windows desktop utility for cleaner screen sharing from ultrawide monitors. The project values focused improvements that make the app easier to run, easier to understand, or safer to use during presentations and recordings.

## Good First Areas

Useful contribution areas include:

- README clarity and screenshots.
- Documentation for multi-monitor behavior.
- Startup and dependency troubleshooting notes.
- UI copy improvements.
- Safer handling for elevated or protected windows.
- Basic smoke checks for app startup and window detection.
- Packaging notes for users who do not want to run from source.

## Local Setup

Requirements:

- Windows 10 or Windows 11.
- Python 3.10 or newer.

Clone the repository:

```bash
git clone https://github.com/AlexMnrs/UltraShare.git
cd UltraShare
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the app:

```powershell
python main.py
```

## Manual Testing

Before proposing a change, test the workflow on Windows:

- Start UltraShare with `python main.py`.
- Confirm the control panel opens.
- Confirm the overlay frame appears.
- Confirm visible windows can be listed.
- Snap a normal application window into the overlay region.
- Move the overlay and confirm the snapped window stays aligned when expected.
- Confirm manual movement of the target window does not leave the app in a confusing state.

If your change affects elevated applications, multi-monitor setups, keyboard hooks, or mouse behavior, describe exactly what you tested.

## Pull Request Guidelines

Please keep pull requests focused and easy to review.

A good PR description should include:

- What changed.
- Why the change helps.
- How you tested it.
- Any Windows version, monitor setup, or permission limitation you noticed.

For UI changes, screenshots or a short GIF are very helpful.
