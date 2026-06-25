from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from docx import Document

FIELD_RE = re.compile(r"^\[(\w+)\]\s*(.*?)\s*\[/\1\]\s*$", re.DOTALL)
OPEN_RE = re.compile(r"^\[(\w+)\]\s*$")
CLOSE_RE = re.compile(r"^\[/(\w+)\]\s*$")


class ParseError(ValueError):
    pass


def parse_docx(path: Path) -> dict[str, Any]:
    document = Document(str(path))
    lines = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    root, _ = _parse_block(lines, 0, None)
    return root


def _parse_block(lines: list[str], index: int, end_tag: str | None) -> tuple[dict[str, Any], int]:
    node: dict[str, Any] = {"_fields": {}, "_children": []}

    while index < len(lines):
        line = lines[index]

        close_match = CLOSE_RE.match(line)
        if close_match:
            tag = close_match.group(1)
            if end_tag is None:
                raise ParseError(f"Tag de fechamento inesperada: [/{tag}]")
            if tag != end_tag:
                raise ParseError(f"Esperado [/{end_tag}], encontrado [/{tag}]")
            return node, index + 1

        open_match = OPEN_RE.match(line)
        if open_match:
            tag = open_match.group(1)
            child, index = _parse_block(lines, index + 1, tag)
            node["_children"].append({tag: _finalize_node(child)})
            continue

        field_match = FIELD_RE.match(line)
        if field_match:
            key, value = field_match.group(1), field_match.group(2).strip()
            if end_tag == "section":
                if key == "heading":
                    node["_fields"][key] = value
                elif key == "answer" and node.get("_blocks") and node["_blocks"][-1]["type"] == "question":
                    question = node["_blocks"][-1]["content"]
                    node["_blocks"][-1]["content"] = {"question": question, "answer": value}
                else:
                    node.setdefault("_blocks", []).append({"type": key, "content": value})
            else:
                node["_fields"][key] = value
            index += 1
            continue

        raise ParseError(f"Linha não reconhecida: {line!r}")

    if end_tag is not None:
        raise ParseError(f"Bloco [/{end_tag}] não foi fechado")

    return node, index


def _finalize_node(node: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = dict(node["_fields"])
    if blocks := node.get("_blocks"):
        result["blocks"] = blocks
    for child in node["_children"]:
        for name, content in child.items():
            if name in result:
                existing = result[name]
                if not isinstance(existing, list):
                    result[name] = [existing]
                result[name].append(content)
            else:
                result[name] = content
    return result


def lesson_data(parsed: dict[str, Any]) -> dict[str, Any]:
    finalized = _finalize_node(parsed)
    cover = finalized.get("cover", {})
    sections = finalized.get("section", [])
    if isinstance(sections, dict):
        sections = [sections]
    return {
        "cover": cover,
        "sections": sections,
    }
