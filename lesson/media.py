from __future__ import annotations

import re
import shutil
from pathlib import Path


class MediaError(FileNotFoundError):
    pass


class MediaResolver:
    def __init__(self, docx_path: Path, output_dir: Path) -> None:
        self._docx_dir = docx_path.resolve().parent
        self._media_dir = output_dir / "media"
        self._copied: dict[str, str] = {}

    def resolve(self, source: str) -> str:
        raw = source.strip()
        if not raw:
            raise MediaError("Endereço de mídia vazio.")

        if _is_remote(raw):
            return raw

        if raw in self._copied:
            return self._copied[raw]

        file_path = (self._docx_dir / raw).resolve()
        if not file_path.is_file():
            raise MediaError(f"Arquivo não encontrado: {raw}")

        self._media_dir.mkdir(parents=True, exist_ok=True)
        destination = self._media_dir / file_path.name
        if not destination.exists() or file_path.stat().st_mtime_ns > destination.stat().st_mtime_ns:
            shutil.copy2(file_path, destination)

        relative = f"media/{destination.name}"
        self._copied[raw] = relative
        return relative


def _is_remote(value: str) -> bool:
    lowered = value.lower()
    return lowered.startswith(("http://", "https://", "//"))


def parse_pipe_value(content: str) -> tuple[str, str | None]:
    if " | " in content:
        left, right = content.split(" | ", 1)
        return left.strip(), right.strip() or None
    return content.strip(), None


def youtube_embed_id(url: str) -> str | None:
    patterns = (
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([\w-]{11})",
    )
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def vimeo_embed_id(url: str) -> str | None:
    match = re.search(r"vimeo\.com/(?:video/)?(\d+)", url, re.IGNORECASE)
    return match.group(1) if match else None

