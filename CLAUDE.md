# CLAUDE.md — 20-20-20 Eye Care App

## Project Overview

A macOS menubar application built with Python that enforces the **20-20-20 rule** for eye health:
> Every **20 minutes**, look at something **20 feet away** for **20 seconds**.

The app lives quietly in the macOS menubar, tracks time, and when the break is due — it locks the screen with a full-screen overlay and a friendly reminder. No way to dismiss early. Eyes first.

---

## Tech Stack

| Layer | Choice | Reason |
|---|---|---|
| Language | Python 3.11+ | Cross-platform logic, fast iteration |
| GUI Framework | `rumps` | Lightweight macOS menubar apps |
| Overlay Window | `tkinter` | Built-in, sufficient for fullscreen overlay |
| Scheduling | `threading.Timer` | Simple, non-blocking countdown |
| Packaging | `py2app` | Bundle into a `.app` for macOS |
| Config Persistence | `plistlib` / `json` | Store user preferences locally |

---

## Project Structure

```
twenty-twenty-twenty/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── setup.py                  # py2app config
├── assets/
│   ├── icon.png              # Menubar icon (22x22 px, dark/light mode aware)
│   ├── icon_active.png       # Ticking icon
│   └── eye_illustration.png  # Shown on overlay screen
├── src/
│   ├── main.py               # Entry point — launches the menubar app
│   ├── app.py                # MenubarApp class (rumps.App subclass)
│   ├── timer.py              # TimerEngine — countdown logic, thread management
│   ├── overlay.py            # FullscreenOverlay — tkinter lock screen
│   ├── blink_counter.py      # BlinkAnimation — animated blink counter on overlay
│   ├── config.py             # UserConfig — load/save preferences
│   ├── notifications.py      # macOS native notification (optional pre-warning)
│   └── utils.py              # Helpers: format_time, screen_dimensions, etc.
└── tests/
    ├── test_timer.py
    └── test_config.py
```

---

## Core Modules — What Each Does

### `main.py`
- Initialises `UserConfig`, `TimerEngine`, and `MenubarApp`
- Wires them together and calls `app.run()`

### `app.py` — `MenubarApp(rumps.App)`
- Displays time remaining in menubar title (e.g. `👁 18:42`)
- Menu items:
  - **Pause / Resume**
  - **Skip This Break**
  - **Settings** → opens a simple preferences panel
  - **Quit**
- Calls `TimerEngine.start()` on launch
- Receives callback from `TimerEngine` when break is due → calls `FullscreenOverlay.show()`

### `timer.py` — `TimerEngine`
- Counts down from `work_interval` (default: 20 min)
- Every second updates `app.title` with remaining time
- On completion: fires `on_break_due` callback, then starts a `break_timer` for `break_duration` (default: 20 sec)
- After break ends: fires `on_break_complete`, restarts work countdown
- Methods: `start()`, `pause()`, `resume()`, `reset()`, `skip()`

### `overlay.py` — `FullscreenOverlay`
- Creates a **fullscreen `tkinter` window** on all displays (multi-monitor support)
- Sits on top of all windows (`wm_attributes('-topmost', True)`)
- **Cannot be dismissed** during the 20-second break period
- Displays:
  - Large countdown timer (20 → 0)
  - Eye illustration / animation
  - Instruction text: *"Look 20 feet away and blink slowly"*
  - Animated blink counter (see `blink_counter.py`)
- After 20 seconds: automatically closes, returns control to user
- Design: soft dark background (#0D1117), large calming typography, gentle fade-in/out

### `blink_counter.py` — `BlinkAnimation`
- Renders 20 eye icons on the overlay
- Animates each one "blinking" in sequence as seconds pass
- Uses `tkinter.Canvas` with oval shapes to simulate open/closed eyes
- Paces one blink approximately every second

### `config.py` — `UserConfig`
- Loads/saves from `~/Library/Application Support/TwentyTwentyTwenty/config.json`
- Default values:
  ```python
  {
    "work_interval_minutes": 20,
    "break_duration_seconds": 20,
    "pre_warning_seconds": 30,  # notification before break
    "sound_enabled": True,
    "show_blink_counter": True,
    "start_on_login": False
  }
  ```
- Exposes `get(key)`, `set(key, value)`, `reset_defaults()`

### `notifications.py`
- Sends a native macOS notification 30 seconds before break (configurable)
- Uses `osascript` via `subprocess` for reliability (no extra deps)
- Message: *"Break in 30 seconds — get ready to look away 👁"*

### `utils.py`
- `format_time(seconds) → "MM:SS"`
- `get_all_screen_geometries() → list[dict]` — for multi-monitor overlay
- `play_sound(name)` — plays a soft chime using `afplay`

---

## UI / Design Spec

### Menubar
- Icon: a minimal eye glyph, 22×22px, supports macOS dark/light mode (use template image)
- Title format: `👁 19:45` while running, `⏸ Paused` when paused

### Overlay Screen
- **Background**: Very dark navy `#0A0E1A` with a subtle radial gradient
- **Font**: Use system SF Pro Display (macOS native) for headings; SF Pro Text for body
- **Countdown**: Giant numeral, center screen, `#E8F4FD` color, animates scale on each tick
- **Instruction**: `"Look 20 feet away · Blink slowly"` — muted, calm, `#8899AA`
- **Blink counter**: Row of 20 soft eye shapes, filling in as each second passes
- **No close button** — intentional, the point is to enforce the break
- **Fade in**: 0.3s opacity transition on appear; fade out on dismiss

### Settings Panel
- Simple `tkinter.Toplevel` window, not fullscreen
- Sliders or entry fields for interval and break duration
- Toggle for sound, pre-warning, start-on-login
- **Save** button — writes to `UserConfig`

---

## Behaviour Rules

1. **Break cannot be skipped during the 20-second overlay** — "Skip" only works between breaks.
2. **Pause stops the countdown** — overlay will not appear while paused.
3. **App restores timer state on relaunch** — if the app crashes and restarts, it picks up roughly where it left off (store last tick timestamp).
4. **Multi-monitor**: overlay covers ALL connected displays simultaneously.
5. **Do not steal focus** from other apps while ticking — only the overlay takes focus.
6. **macOS Accessibility permission** is NOT required — we use `tkinter` overlay, not system-level screen lock.

---

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run in development
python src/main.py

# Run tests
pytest tests/

# Build macOS .app bundle
python setup.py py2app

# Open built app
open dist/TwentyTwentyTwenty.app
```

---

## requirements.txt

```
rumps==0.4.0
py2app==0.28.8
pytest==8.0.0
```

> `tkinter` is bundled with Python — no separate install needed.

---

## Key Implementation Notes for Claude

- **Threading**: `TimerEngine` runs on a background thread. All `tkinter` UI updates MUST happen on the main thread — use `app.after()` or a queue pattern.
- **rumps + tkinter**: `rumps` uses `AppKit` under the hood. To show a `tkinter` window from a `rumps` callback, call it on the main thread using `rumps.App` timers or `dispatch_async` via `PyObjC`.
- **Fullscreen lock**: Set `root.attributes('-fullscreen', True)` and `root.attributes('-topmost', True)` and `root.grab_set()` to prevent interaction with anything underneath.
- **macOS Ventura+**: `wm_attributes('-topmost', True)` alone may not cover the menubar — use `root.overrideredirect(True)` combined with the geometry set to full screen size including menubar height.
- **Sound**: `afplay /System/Library/Sounds/Glass.aiff` for break start; `afplay /System/Library/Sounds/Ping.aiff` for break end.
- **Login Item**: Use `launchctl` or write a `LaunchAgent` plist to `~/Library/LaunchAgents/` for start-on-login.

---

## Non-Goals (Keep It Simple)

- No analytics or telemetry
- No cloud sync
- No iOS companion app
- No gamification or streaks (keep it calm, not addictive)
- No complex settings beyond interval/duration/sound

---

## Vibe

This app should feel like a **calm, thoughtful friend** reminding you to rest — not an aggressive productivity enforcer. The overlay is unavoidable but serene. The menubar presence is subtle. Every interaction should feel gentle and respectful of the user's flow.
