import os
import sys


def main() -> None:
    """Forward execution directly to the tool's python interpreter so scripts,
    heredocs and flags work identically to the python CLI.
    """
    os.execv(sys.executable, [sys.executable] + sys.argv[1:])


if __name__ == "__main__":
    main()
