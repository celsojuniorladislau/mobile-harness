import os
import sys


from pathlib import Path


def main() -> None:
    """Forward execution directly to the tool's python interpreter so scripts,
    heredocs and flags work identically to the python CLI.
    """
    if not os.environ.get("HARNESS_ROOT"):
        candidates = [
            Path.home() / ".local/share/mobile-harness",
            Path.home() / ".gemini/config/skills/mobile-harness",
            Path.home() / ".codex/skills/mobile-harness",
        ]
        for candidate in candidates:
            if candidate.is_dir() and (candidate / "AGENTS.md").is_file():
                os.environ["HARNESS_ROOT"] = str(candidate.resolve())
                break
    os.execv(sys.executable, [sys.executable] + sys.argv[1:])


if __name__ == "__main__":
    main()
