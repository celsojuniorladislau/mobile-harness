---
name: mobile-harness
description: Portable Android and iOS device-control harness for agents. Use when an agent needs to control or automate Android/iOS devices — tap, swipe, screenshot, app control — locally (ADB/Portal/Simulator) or on Mobilerun cloud devices.
---

# mobile-harness

Use this harness when an agent needs to control Android or iOS devices through Mobilerun.

## Load Order & Guidance

Subguides reside inside the harness root (e.g. `~/.local/share/mobile-harness/` or `~/.codex/skills/mobile-harness/`):
1. Read `AGENTS.md` for core rules, safety boundaries, and non-negotiables.
2. For Android specifics, read `platforms/android/GUIDE.md`. For iOS, read `platforms/ios/GUIDE.md`.
3. Read package App Cards (`apps/android/<package>/CARD.md`) only when one exists (Settings, Chrome, Gmail, eBay). For all other apps, navigate using semantic accessibility tree inspection (`find_nodes`, `tap_text`).

## Primary Control Model

Normal device control always uses `mobilerun_core`:

```python
from mobilerun_core import Mobilerun
```

Use `Mobilerun()` to connect to cloud devices, local Android ADB with optional Portal, local Android Portal HTTP-only, or local iOS Portal HTTP. Do not import or call `mobilerun_core_local` directly for normal agent work.

## CLI Execution

When `mobile-harness` CLI (or `./bin/mobile-harness`) is available:

```bash
mobile-harness <<'PY'
import base64
import subprocess
from mobilerun_core import Mobilerun

m = Mobilerun()

# 1. Resolve ADB serial automatically (resilient to multiple/offline devices)
try:
    out = subprocess.check_output(["adb", "devices"]).decode()
    devices = [line.split()[0] for line in out.strip().splitlines()[1:] if "\tdevice" in line]
    serial = devices[0] if devices else None
except Exception:
    serial = None

device = m.connect(serial or "<adb-serial>", backend="local-android-adb")

# 2. Inspect UI hierarchy or find on-screen nodes directly
nodes = device.find_nodes_on_screen(text_contains="Settings")
print(f"Found {len(nodes)} on-screen matches")

# 3. Optional: save screenshot (local backend returns base64-encoded PNG string)
# screenshot_b64 = device.screenshot()
# with open("screenshot.png", "wb") as f:
#     f.write(base64.b64decode(screenshot_b64))
PY
```

You can also run one-liners directly via `mobile-harness -c "..."` or execute Python scripts via `mobile-harness script.py`.

## Action Cycle (Observe -> Act -> Verify)

1. **Observe**:
   - `device.find_nodes(any_contains="...")` or `device.find_nodes_on_screen(...)` locates target elements and computes their center coordinates.
   - `device.current_app_id()` identifies the active foreground package/bundle.
   - Fallback to `device.screenshot()` only if visual inspection is required (note: local backend returns a base64-encoded PNG string).

2. **Act**:
   - **Taps**: `device.tap_text("Label")`, `device.tap_node(node)`, or `device.tap_and_wait("Label", idle=1.5)` (preferred to allow transitions to settle).
   - **Text Input**: `device.type("Text", stealth=False)`. Always prefer `stealth=False` for fast, reliable input across any OEM keyboard (Samsung, Xiaomi, Gboard) and non-English locales. *Note: `get_clipboard`/`set_clipboard` is unsupported on `local-android-adb`.*
   - **Scroll & Search**: `device.scroll_until(text_contains="Target", direction="down")` automatically scrolls until off-screen elements come into view. Use `device.scroll("down")` for simple viewport movement.
   - **App Lifecycle**: `device.start_app("com.example.app")` brings an app to the foreground. Follow immediately with `device.wait_for_app("com.example.app", timeout=5.0)`. Use `device.stop_app("com.example.app")` to terminate.
   - **Hardware/Nav Keys**: Use `device.key("back")`, `device.key("home")`, `device.key("enter")`.
   - **Waking the Screen**: Never use `device.key("power")` (it is blocked and raises `ValueError`). To wake an inactive screen, use `device.key("wakeup")` followed by `device.scroll("up")` to dismiss the lock screen.

3. **Verify**:
   - Always verify the expected state before proceeding to the next step.
   - Use `device.wait_for_idle()` or `device.wait_for_text("Success", timeout=5.0)` to prevent race conditions during UI animations.

For setup and runtime registration, read `install.md`.
