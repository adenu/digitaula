from __future__ import annotations

import sys
from pathlib import Path

from lesson import ui
from lesson.cli import convert_lesson, run_interactive
from lesson.paths import css_path, default_config_path, output_dir, pause_if_frozen, resolve_docx
from lesson.ui import EXIT_CANCELLED


def main() -> int:
    code = 0
    try:
        if len(sys.argv) == 1:
            code = run_interactive()
        elif len(sys.argv) == 2:
            ui.init_terminal()
            try:
                result = convert_lesson(
                    resolve_docx(Path(sys.argv[1])),
                    output_dir(),
                    css_path(),
                    default_config_path(),
                )
            except Exception as error:
                ui.print_error(str(error))
                code = 1
            else:
                ui.print_generated(result)
        else:
            ui.init_terminal()
            ui.print_usage()
            code = 1
    except (KeyboardInterrupt, EOFError):
        ui.init_terminal()
        ui.print_cancelled()
        code = EXIT_CANCELLED
    finally:
        if code != 0 or len(sys.argv) == 1:
            pause_if_frozen()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
