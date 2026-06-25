from __future__ import annotations

from dataclasses import dataclass
from typing import Any


CALLOUT_STYLES = frozenset({"info", "warning", "success", "danger", "primary", "secondary"})
CONTAINER_WIDTHS = frozenset({"sm", "md", "lg", "xl", "xxl", "fluid"})
THEMES = frozenset({"light", "dark"})


@dataclass
class LessonTheme:
    brand_name: str = "Lesson"
    primary_color: str = "#0d6efd"
    secondary_color: str = ""
    logo: str = ""
    logo_alt: str = ""
    lang: str = "pt-BR"
    theme: str = "light"
    footer: str = ""
    container: str = "lg"
    show_brand_on_cover: bool = True
    author_prefix: str = "Por"
    label_purpose: str = "Objetivo"
    label_preparation: str = "Antes de começar"
    label_section_fallback: str = "Seção"
    show_section_numbers: bool = True
    section_number_style: str = "badge"
    callout_style: str = "info"
    image_max_height: str = "28rem"
    link_opens_new_tab: bool = True
    meta_description: str = ""
    title_suffix: str = ""

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> LessonTheme:
        brand = config.get("brand", {})
        lesson = config.get("lesson", {})
        sections = config.get("sections", {})
        blocks = config.get("blocks", {})
        meta = config.get("meta", {})
        labels = lesson.get("labels", {})

        container = str(lesson.get("container", "lg")).lower()
        if container not in CONTAINER_WIDTHS:
            container = "lg"

        callout = str(blocks.get("callout_style", "info")).lower()
        if callout not in CALLOUT_STYLES:
            callout = "info"

        theme_name = str(lesson.get("theme", "light")).lower()
        if theme_name not in THEMES:
            theme_name = "light"

        number_style = str(sections.get("number_style", "badge")).lower()
        if number_style not in {"badge", "text", "hidden"}:
            number_style = "badge"

        return cls(
            brand_name=str(brand.get("name", "Lesson")),
            primary_color=str(brand.get("primary_color", "#0d6efd")),
            secondary_color=str(brand.get("secondary_color", "")),
            logo=str(brand.get("logo", "")),
            logo_alt=str(brand.get("logo_alt", "")),
            lang=str(lesson.get("lang", "pt-BR")),
            theme=theme_name,
            footer=str(lesson.get("footer", "")),
            container=container,
            show_brand_on_cover=bool(lesson.get("show_brand_on_cover", True)),
            author_prefix=str(lesson.get("author_prefix", "Por")),
            label_purpose=str(labels.get("purpose", "Objetivo")),
            label_preparation=str(labels.get("preparation", "Antes de começar")),
            label_section_fallback=str(labels.get("section_fallback", "Seção")),
            show_section_numbers=bool(sections.get("show_numbers", True)),
            section_number_style=number_style,
            callout_style=callout,
            image_max_height=str(blocks.get("image_max_height", "28rem")),
            link_opens_new_tab=bool(blocks.get("link_opens_new_tab", True)),
            meta_description=str(meta.get("description", "")),
            title_suffix=str(meta.get("title_suffix", "")),
        )

    def container_class(self) -> str:
        if self.container == "fluid":
            return "container-fluid"
        if self.container == "lg":
            return "container"
        return f"container-{self.container}"

    def page_title(self, lesson_title: str) -> str:
        suffix = self.title_suffix.strip()
        if suffix:
            return f"{lesson_title} · {suffix}"
        return lesson_title

    def section_heading(self, heading: str, index: int) -> str:
        if not self.show_section_numbers or self.section_number_style == "hidden":
            return heading
        if self.section_number_style == "text":
            return f"{index}. {heading}"
        return heading

    def section_number_badge(self, index: int) -> str:
        if not self.show_section_numbers or self.section_number_style != "badge":
            return ""
        return str(index)
