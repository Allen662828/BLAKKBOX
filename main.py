"""
main.py

Entry point for BLAKKBOX.
"""

from __future__ import annotations

import sys

from core.logger import Logger
from core.logger import info
from core.logger import error

from core.workflow import Workflow


def main() -> int:
    """
    Application entry point.
    """

    Logger.configure()

    info("=" * 60)
    info("BLAKKBOX DENSO STUDIO")
    info("=" * 60)

    try:

        workflow = Workflow()
        workflow.run()

        info("=" * 60)
        info("Workflow Finished")
        info("=" * 60)

        return 0

    except KeyboardInterrupt:

        error("Execution cancelled by user.")
        return 1

    except Exception as exc:

        error("=" * 60)
        error("Unhandled Exception")
        error("=" * 60)
        error(str(exc))

        return 1


if __name__ == "__main__":
    sys.exit(main())
