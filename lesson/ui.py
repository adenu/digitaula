from __future__ import annotations

import os
import sys
from pathlib import Path

from .meta import AUTHOR_HANDLE, TAGLINE

_BOX_INNER = 50


class _C:
    RESET = ""
    BOLD = ""
    DIM = ""
    CYAN = ""
    GREEN = ""
    YELLOW = ""
    RED = ""
    BLUE = ""
    MAGENTA = ""
    WHITE = ""


_ENABLED = False


def _enable_windows_ansi() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes

        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        ctypes.windll.kernel32.SetConsoleMode(handle, mode.value | 7)
    except (AttributeError, OSError, ValueError):
        pass


def init_terminal() -> None:
    global _ENABLED
    if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        return

    _enable_windows_ansi()
    _ENABLED = True
    _C.RESET = "\033[0m"
    _C.BOLD = "\033[1m"
    _C.DIM = "\033[2m"
    _C.CYAN = "\033[36m"
    _C.GREEN = "\033[32m"
    _C.YELLOW = "\033[33m"
    _C.RED = "\033[31m"
    _C.BLUE = "\033[34m"
    _C.MAGENTA = "\033[35m"
    _C.WHITE = "\033[97m"


def stylize(text: str, *styles: str) -> str:
    if not _ENABLED or not styles:
        return text
    return f"{''.join(styles)}{text}{_C.RESET}"


def _box_top() -> str:
    return stylize(f"╭{'─' * (_BOX_INNER + 2)}╮", _C.CYAN)


def _box_bottom() -> str:
    return stylize(f"╰{'─' * (_BOX_INNER + 2)}╯", _C.CYAN)


def _box_line(plain: str, styled: str | None = None) -> str:
    side = stylize("│", _C.CYAN)
    content = styled if styled is not None else plain
    pad = max(0, _BOX_INNER - len(plain))
    return f"{side} {content}{' ' * pad} {side}"


def print_banner() -> None:
    brand = stylize("DigitAula", _C.BOLD, _C.MAGENTA)
    plain1 = "                  DigitAula"
    row1 = _box_line(plain1, f"                  {brand}")

    plain2 = f"         {TAGLINE}"
    tagline = stylize(TAGLINE, _C.DIM)
    row2 = _box_line(plain2, f"         {tagline}")

    credit = stylize(AUTHOR_HANDLE, _C.DIM)
    print("\n".join(["", _box_top(), _box_line(""), row1, row2, _box_line(""), _box_bottom(), f"  {credit}", ""]))


def print_section(title: str) -> None:
    label = stylize(f"▸ {title}", _C.BOLD, _C.BLUE)
    rule = stylize("─" * 48, _C.DIM)
    print(f"\n{label}\n{rule}")


def print_option(index: int, label: str, *, highlight: bool = False) -> None:
    num = stylize(f"{index:>2})", _C.CYAN, _C.BOLD)
    text = stylize(label, _C.WHITE) if highlight else label
    print(f"  {num}  {text}")


def print_hint(text: str) -> None:
    print(stylize(f"  {text}", _C.DIM))


EXIT_CANCELLED = 130


def print_cancelled() -> None:
    text = stylize("Operação cancelada.", _C.YELLOW)
    print(f"\n  {text}\n", file=sys.stderr)


def prompt(text: str, default: str | None = None) -> str:
    label = stylize(text, _C.YELLOW, _C.BOLD)
    suffix = stylize(f" [{default}]", _C.DIM) if default else ""
    try:
        value = input(f"  {label}{suffix}: ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        raise
    return value or (default or "")


def print_working(message: str) -> None:
    print(stylize(f"\n  … {message}", _C.CYAN))


def print_success(result: Path) -> None:
    check = stylize("✓", _C.GREEN, _C.BOLD)
    title = stylize("Aula gerada com sucesso!", _C.GREEN, _C.BOLD)
    path = stylize(str(result), _C.CYAN)
    hint = stylize("Abra index.html no navegador.", _C.DIM)
    print(f"\n  {check}  {title}\n")
    print(f"     {path}")
    print(f"     {hint}\n")


def print_error(message: str) -> None:
    mark = stylize("✗", _C.RED, _C.BOLD)
    text = stylize(message, _C.RED)
    print(f"\n  {mark}  {text}\n", file=sys.stderr)


def print_usage() -> None:
    print_error("Uso: DigitAula [arquivo.docx]")


def print_generated(result: Path) -> None:
    print_success(result)
