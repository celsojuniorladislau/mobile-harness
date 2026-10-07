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

# 1. Connect automatically to the local device (or pass explicit serial)
try:
    device = m.ensure_device(scope="local")
except Exception:
    import subprocess
    out = subprocess.check_output(["adb", "devices"]).decode()
    devices = [line.split()[0] for line in out.strip().splitlines()[1:] if "\tdevice" in line]
    device = m.connect(devices[0] if devices else "<adb-serial>", backend="local-android-adb")

# 2. Inspect UI hierarchy or find on-screen nodes directly
nodes = device.find_nodes_on_screen(text_contains="Settings")
print(f"Found {len(nodes)} on-screen matches")

# 3. Optional: save screenshot (local backend returns base64 PNG string; cloud returns file path)
# screenshot_val = device.screenshot()
# if not screenshot_val.startswith("/"):
#     with open("screenshot.png", "wb") as f:
#         f.write(base64.b64decode(screenshot_val))
PY
```

You can also run one-liners directly via `mobile-harness -c "..."` or execute Python scripts via `mobile-harness script.py`.

## Action Cycle (Observe -> Act -> Verify)

1. **Observe**:
   - `device.find_nodes_on_screen(...)` locates on-screen elements reliably.
   - *Search Shadowing Caveat*: `any_contains=` evaluates `text` first. If a node has both text and description, use `desc_contains=` or full `resource_id=` explicitly.
   - `device.current_app_id()` identifies the active foreground package (returns `None` on local iOS).
   - Fallback to `device.screenshot()` only if visual inspection is required (local backend returns base64-encoded PNG string; cloud returns file path).

2. **Act**:
   - **Taps**: `device.tap_text("Label")`, `device.tap_node(node)`, or `device.tap_and_wait("Label", idle=1.5)` (preferred to allow transitions to settle).
   - **Text Input**: `device.type("Text", stealth=False)`. Always prefer `stealth=False` for fast input. *Note: in ADB-only mode (without Portal), input strictly supports printable ASCII (accents/emojis raise `ValueError`). `get_clipboard`/`set_clipboard` is unsupported on `local-android-adb`.*
   - **Scroll & Search**: `device.scroll_until(text_contains="Target", direction="down")` automatically scrolls until off-screen elements come into view. Use `device.scroll("down")` for simple viewport movement.
   - **App Lifecycle**: `device.open_and_settle("com.example.app")` is the canonical opener (starts app, waits for foreground, waits for idle; Android/Cloud). Use `device.stop_app("com.example.app")` to terminate (on local iOS use `device.key("home")`).
   - **Hardware/Nav Keys**: On Android, use `device.key("back")`, `device.key("home")`, `device.key("enter")`. On local iOS (`local-ios-http`), **only `device.key("home")` is supported** (`"back"` raises `UnsupportedOperation`; navigate back using nav-bar taps or left-edge swipes).
   - **Waking the Screen**: Never use `device.key("power")` (it is blocked and raises `ValueError`). To wake an inactive Android screen, use `device.key("wakeup")` followed by `device.scroll("up")` to dismiss the lock screen.

3. **Verify**:
   - Always verify the expected state before proceeding to the next step.
   - Use `device.wait_for_idle()` or `device.wait_for_text("Success", timeout=5.0)` to prevent race conditions during UI animations. On Android, use `device.assert_on("com.example.app")` to ensure the correct app remained in foreground.

For setup and runtime registration, read `install.md`.
