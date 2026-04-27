# 👁 TwentyTwentyTwenty

> A minimal macOS menubar app that enforces the **20-20-20 rule** to protect your eyes during long screen sessions.

---

## What is the 20-20-20 Rule?

Every **20 minutes** of screen time, look at something **20 feet away** for **20 seconds** — and blink 20 times.

This simple habit dramatically reduces digital eye strain, dry eyes, and headaches. Most people forget. This app makes sure you don't.

---

## How It Works

1. App runs silently in your **macOS menubar**, showing a live countdown.
2. When 20 minutes are up, a **full-screen overlay** appears on all your monitors.
3. The overlay **cannot be dismissed** — it holds for exactly 20 seconds.
4. A visual blink counter guides you through 20 gentle blinks.
5. Overlay fades away automatically. Your work resumes.

That's it.

---

## Features

- 🕐 **Live countdown** in the menubar — always know when your next break is
- 🖥 **Full-screen overlay** that covers all connected monitors
- 👁 **Animated blink counter** — 20 eyes, one per second
- 🔕 **Non-intrusive** — silent presence until break time
- ⏸ **Pause / Resume** for meetings or when stepping away
- 🔔 **30-second pre-warning** notification so you can reach a stopping point
- ⚙️ **Configurable** intervals, break duration, and sound
- 🌙 Supports macOS **dark and light mode**

---

## Screenshots

```
Menubar:   👁 18:42                    ← Counting down quietly

Overlay:   ┌────────────────────────┐
           │                        │
           │         20             │  ← Giant countdown
           │                        │
           │  Look 20 feet away     │
           │  Blink slowly 👁        │
           │                        │
           │  👁 👁 👁 👁 👁          │  ← Blink counter
           │  👁 👁 👁 👁 👁          │    (fills as seconds pass)
           │  👁 👁 👁 👁 👁          │
           │  👁 👁 👁 👁 👁          │
           │                        │
           └────────────────────────┘
```

---

## Requirements

- **macOS 12 Monterey** or later (tested on Ventura & Sonoma)
- **Python 3.11+**
- No additional system permissions required

---

## Installation

### Option A — Run from Source (Development)

```bash
# 1. Clone the repo
git clone https://github.com/yourname/twenty-twenty-twenty.git
cd twenty-twenty-twenty

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python src/main.py
```

The app icon will appear in your menubar. Click it to see the menu.

---

### Option B — Build a Standalone .app

```bash
# Make sure you're in the project root with venv activated
python setup.py py2app

# The built app will be at:
open dist/TwentyTwentyTwenty.app
```

You can drag this `.app` into your `/Applications` folder and launch it like any other macOS app.

---

### Option C — Start on Login

To have the app start automatically when you log in:

1. Open **System Settings → General → Login Items**
2. Click **+** and select `TwentyTwentyTwenty.app`

Or enable it from the app's **Settings** menu (writes a LaunchAgent automatically).

---

## Usage

### Menubar Menu

| Item | Action |
|---|---|
| `👁 18:42` (title) | Current countdown — click to open menu |
| **Pause** | Stops the timer; overlay won't appear |
| **Resume** | Restarts the countdown from where it paused |
| **Skip This Break** | Resets the 20-min timer without showing the overlay |
| **Settings…** | Opens the preferences panel |
| **Quit** | Exits the app |

### During a Break

- The overlay appears automatically — you don't need to do anything.
- Look at something in the distance and let your eyes relax.
- The blink counter fills one eye per second.
- After 20 seconds, the overlay fades and you're back.
- **There is no way to close the overlay early** — that's the point.

---

## Configuration

Open **Settings** from the menubar menu. Options:

| Setting | Default | Description |
|---|---|---|
| Work interval | 20 minutes | How long between breaks |
| Break duration | 20 seconds | How long the overlay stays up |
| Pre-warning | 30 seconds | Notification before break starts |
| Sound | On | Soft chime at break start/end |
| Blink counter | On | Animated eye counter on overlay |
| Start on login | Off | Auto-launch with macOS |

Settings are saved to:
```
~/Library/Application Support/TwentyTwentyTwenty/config.json
```

---

## Project Structure

```
twenty-twenty-twenty/
├── src/
│   ├── main.py           # Entry point
│   ├── app.py            # Menubar app (rumps)
│   ├── timer.py          # Countdown engine
│   ├── overlay.py        # Fullscreen break overlay (tkinter)
│   ├── blink_counter.py  # Animated blink visualiser
│   ├── config.py         # User preferences
│   ├── notifications.py  # macOS notifications
│   └── utils.py          # Helpers
├── assets/
│   ├── icon.png
│   └── eye_illustration.png
├── tests/
├── requirements.txt
├── setup.py
├── CLAUDE.md             # AI coding context
└── README.md
```

---

## Development

```bash
# Run tests
pytest tests/

# Run with verbose logging
LOG_LEVEL=DEBUG python src/main.py

# Lint
flake8 src/

# Format
black src/
```

---

## Philosophy

This app is intentionally **simple and calm**. It does one thing: remind you to rest your eyes. It won't gamify your breaks, track your streaks, or send you weekly reports. It's a quiet, respectful nudge — nothing more.

The overlay is the only "aggressive" thing about it, and that's deliberate. A dismissible reminder is one that gets ignored.

---

## Troubleshooting

**The overlay doesn't appear on my second monitor**
→ Make sure both displays are active. The app reads all connected screen geometries at break time.

**The app icon doesn't show in the menubar**
→ Your menubar may be full. Try hiding some other icons, or use Bartender / Ice to manage overflow.

**"TwentyTwentyTwenty" can't be opened because it's from an unidentified developer**
→ Right-click the `.app` → Open → Open anyway. (Standard macOS Gatekeeper behaviour for unsigned apps.)

**The overlay is behind other windows**
→ This may happen on macOS Sonoma with certain fullscreen apps. Report it as an issue with your macOS version and app details.

---

## Contributing

Pull requests are welcome. Please keep the scope small — this app's power is in what it *doesn't* do.

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-thing`
3. Commit your changes: `git commit -m 'add: my thing'`
4. Push: `git push origin feature/my-thing`
5. Open a pull request

---

## License

MIT — use it, modify it, share it.

---

## Acknowledgements

- [rumps](https://github.com/jaredks/rumps) — Ridiculously Uncomplicated macOS Python Statusbar apps
- The 20-20-20 rule was popularised by optometrist Dr. Jeffrey Anshel
- Inspired by the dozens of eye strain apps that are either too complex or too ugly

---

*Built for humans who forget to blink.*
