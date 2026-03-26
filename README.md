[![中文](https://img.shields.io/badge/README-中文-red)](README.zh.md)

# ClipSaver 📋

**Save clipboard images to the current Finder window with ⌘⌥V.**

macOS has no native way to save a clipboard image directly to a file — `⌘V` does nothing in Finder. ClipSaver fills that gap. Whatever the source — system screenshot, Feishu capture, copy from browser, Figma export — if it's in your clipboard, open Finder, navigate to the target folder, and press `⌘⌥V` to save it instantly as a PNG. Want to save the same image to multiple folders? Just switch folders and press again.

---

## How to Use

1. Copy an image to your clipboard:
   - `⌘⌃⇧4` — Screenshot directly to clipboard (no file saved, works on all macOS versions)
   - `⌘⇧4` — Screenshot + auto-copy on macOS Monterey (12)+
   - Or copy from any screenshot tool, web page, or design app
2. Open Finder and navigate to the destination folder
3. Press `⌘⌥V` — saves as `screenshot-HHMMSS.png`, Finder highlights the new file
4. Want to save to another folder? Switch there and press again

The 📋 icon in the menu bar means ClipSaver is running. Click it to trigger a save manually, or toggle launch-at-login.

---

## Installation

**Dependencies**

```bash
pip install rumps pyobjc
brew install pngpaste
```

**Run**

```bash
python3 clipsaver.py
```

On first launch, grant access in **System Settings → Privacy & Security → Accessibility** (required for global hotkey).

**Launch at Login**

Click 📋 in the menu bar → Launch at Login. No extra setup needed.

---

## Requirements

- macOS 12+
- Python 3.9+

---

## How It Works

80 lines of Python, three core dependencies:

- **rumps** — Menu bar app shell
- **NSEvent (pyobjc)** — System-level global hotkey listener
- **pngpaste + osascript** — Write clipboard image to disk & get Finder's current directory

---

## License

MIT
