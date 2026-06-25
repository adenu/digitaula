from __future__ import annotations

import os
import sys
from pathlib import Path


def is_frozen() -> bool:
    return getattr(sys, "frozen", False)


def app_root() -> Path:
    """Pasta do projeto ou da pasta onde está o .exe (config, sources, output)."""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def bundle_root() -> Path:
    """Recursos embutidos no executável (assets)."""
    if is_frozen():
        return Path(sys._MEIPASS)
    return app_root()


def css_path() -> Path:
    return bundle_root() / "assets" / "lesson.css"


def examples_dir() -> Path:
    """Modelos de referência (não é a pasta de trabalho do professor)."""
    local = app_root() / "examples"
    if local.is_dir():
        return local
    bundled = bundle_root() / "examples"
    if bundled.is_dir():
        return bundled
    return local


def sources_dir() -> Path:
    """Pasta onde o professor salva os .docx para listagem no CLI."""
    folder = app_root() / "sources"
    folder.mkdir(exist_ok=True)
    return folder


def resolve_docx(path: Path) -> Path:
    candidate = path.expanduser()
    if candidate.is_absolute():
        if candidate.exists():
            return candidate.resolve()
        raise FileNotFoundError(f"Arquivo não encontrado: {candidate}")

    for base in (app_root(), sources_dir(), examples_dir(), bundle_root(), Path.cwd()):
        resolved = (base / candidate).resolve()
        if resolved.exists():
            return resolved

    raise FileNotFoundError(f"Arquivo não encontrado: {candidate}")


def output_dir() -> Path:
    return app_root() / "output"


def default_config_path() -> Path | None:
    for name in ("config.yaml", "config.example.yaml"):
        path = app_root() / name
        if path.exists():
            return path
    for name in ("config.yaml", "config.example.yaml"):
        bundled = bundle_root() / name
        if bundled.exists():
            return bundled
    return None


def pause_if_frozen() -> None:
    if is_frozen() and os.environ.get("DIGITAULA_NO_PAUSE") != "1":
        input("\nPressione Enter para fechar...")
