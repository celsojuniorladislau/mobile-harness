---
name: mobile-harness
description: Portable Android and iOS device-control harness for agents. Use when an agent needs to control or automate Android/iOS devices — tap, swipe, screenshot, app control — locally (ADB/Portal/Simulator) or on Mobilerun cloud devices.
---

# mobile-harness

Use this harness when an agent needs to control Android or iOS devices through
Mobilerun.

Start by reading `AGENTS.md`. It routes you to the smallest platform file for
the current task.

## Primary Control Model

Normal device control always uses:

```python
from mobilerun_core import Mobilerun
```

Use `Mobilerun()` to connect to cloud devices, local Android ADB with optional
Portal, local Android Portal HTTP-only, or local iOS Portal HTTP. Do not import
or call `mobilerun_core_local` directly for normal agent work. `mobilerun-core-local` is the
local-driver dependency used internally by `mobilerun-core` for Android and iOS
local backends.

## Load Order

1. Read `AGENTS.md`.
2. Read `platforms/android/GUIDE.md` for Android work.
3. Read `platforms/ios/GUIDE.md` for iOS work.
4. Read recovery, credentials, memory, and app-card files only when routed
   there by `AGENTS.md` or the platform guide.

## CLI Execution

When `mobile-harness` CLI (or `./bin/mobile-harness`) is available:

```bash
mobile-harness <<'PY'
import base64
import subprocess
from mobilerun_core import Mobilerun

m = Mobilerun()

# 1. Resolve ADB serial automatically if not provided (local-android-adb requires a serial)
try:
    serial = subprocess.check_output(["adb", "get-serialno"]).decode().strip()
except Exception:
    serial = None

device = m.connect(serial or "<adb-serial>", backend="local-android-adb")

# 2. Inspect accessibility hierarchy
tree = device.ui()
print(tree)

# 3. Optional: save screenshot (local backend returns base64-encoded PNG string)
# screenshot_b64 = device.screenshot()
# with open("screenshot.png", "wb") as f:
#     f.write(base64.b64decode(screenshot_b64))
PY
```

### Action Cycle (Observe -> Act -> Verify)

1. **Observe**: `device.ui()` extracts the semantic UI hierarchy. Fallback to `device.screenshot()` only if visual inspection is needed (note: local backend returns base64-encoded PNG string).
2. **Act**: `device.tap_text("Label")`, `device.tap_node(node)`, `device.type("Text")`, `device.scroll("down")`, `device.key("back")`.
3. **Verify**: Always re-check `device.ui()` after an action to ensure the state transitioned as expected before the next step.

For setup and runtime registration, read `install.md`.
