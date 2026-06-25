from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "brand": {
        "name": "Lesson",
        "primary_color": "#0d6efd",
        "secondary_color": "",
        "logo": "",
        "logo_alt": "",
    },
    "lesson": {
        "lang": "pt-BR",
        "theme": "light",
        "footer": "",
        "container": "lg",
        "show_brand_on_cover": True,
        "author_prefix": "Por",
        "labels": {
            "purpose": "Objetivo",
            "preparation": "Antes de começar",
            "section_fallback": "Seção",
        },
    },
    "sections": {
        "show_numbers": True,
        "number_style": "badge",
    },
    "blocks": {
        "callout_style": "info",
        "image_max_height": "28rem",
        "link_opens_new_tab": True,
    },
    "meta": {
        "description": "",
        "title_suffix": "",
    },
}


def load_config(path: Path | None) -> dict[str, Any]:
    config = deepcopy(DEFAULT_CONFIG)
    if path is None or not path.exists():
        return config

    with path.open(encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    for section, values in loaded.items():
        if isinstance(values, dict) and isinstance(config.get(section), dict):
            _deep_merge(config[section], values)
        else:
            config[section] = values

    return config


def _deep_merge(base: dict[str, Any], updates: dict[str, Any]) -> None:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
