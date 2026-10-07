# iOS Settings Card

Bundle id: `com.apple.Preferences`

Use this card only when iOS Settings is the foreground app or the task explicitly targets device settings.

## Useful Labels

- Settings search may appear near the top of the root Settings screen.
- Back navigation labels vary by current pane.
- Permission and privacy panes can require precise labels.

## Flow Notes

- Prefer Settings search for deep destinations when visible.
- Confirm the exact page title after navigation.
- Use one Back action at a time (tap the navigation bar Back button or edge swipe; `device.key("back")` is unsupported on iOS) and observe after each press.

## Traps

- `device.key("back")` does not exist on iOS. Always navigate back using `device.tap_text("<Back-Label>")` or a left-edge swipe (`device.swipe(10, cy, 300, cy)`).
- Some settings changes are destructive, privacy-sensitive, or require passcode confirmation. Ask before reset, account removal, VPN, profiles, accessibility, or permission changes unless the user explicitly requested that exact action.
- If Settings asks for passcode, Apple ID, password, biometric confirmation, payment, or recovery, stop and read `core/credentials/GUIDE.md`.
