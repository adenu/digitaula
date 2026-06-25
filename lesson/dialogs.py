from __future__ import annotations

import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any


@contextmanager
def _tk_root() -> Iterator[Any]:
    if not _can_use_gui():
        yield None
        return

    try:
        import tkinter as tk
    except ImportError:
        yield None
        return

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        yield root
    finally:
        root.destroy()


def _start_dir(initial_dir: Path | None) -> Path:
    if initial_dir and initial_dir.is_dir():
        return initial_dir
    return Path.home()


def pick_docx_file(initial_dir: Path | None = None) -> Path | None:
    with _tk_root() as root:
        if root is None:
            return None

        from tkinter import filedialog

        selected = filedialog.askopenfilename(
            parent=root,
            title="Selecione o arquivo Word da aula",
            initialdir=str(_start_dir(initial_dir)),
            filetypes=[
                ("Documento Word", "*.docx"),
                ("Todos os arquivos", "*.*"),
            ],
        )

    if not selected:
        return None

    return Path(selected).resolve()


def pick_output_dir(initial_dir: Path | None = None) -> Path | None:
    with _tk_root() as root:
        if root is None:
            return None

        from tkinter import filedialog

        selected = filedialog.askdirectory(
            parent=root,
            title="Selecione a pasta de saída da aula",
            initialdir=str(_start_dir(initial_dir)),
            mustexist=True,
        )

    if not selected:
        return None

    return Path(selected).resolve()


def _can_use_gui() -> bool:
    if os.environ.get("DIGITAULA_NO_GUI") == "1":
        return False
    if sys.platform == "win32":
        return True
    return bool(os.environ.get("DISPLAY"))
