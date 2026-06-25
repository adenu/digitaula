from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

from .media import (
    MediaResolver,
    parse_pipe_value,
    vimeo_embed_id,
    youtube_embed_id,
)
from .meta import AUTHOR_HANDLE, PROJECT_NAME
from .parser import lesson_data
from .theme import LessonTheme

BOOTSTRAP_VERSION = "5.3.3"
BOOTSTRAP_CSS = f"https://cdn.jsdelivr.net/npm/bootstrap@{BOOTSTRAP_VERSION}/dist/css/bootstrap.min.css"
BOOTSTRAP_JS = f"https://cdn.jsdelivr.net/npm/bootstrap@{BOOTSTRAP_VERSION}/dist/js/bootstrap.bundle.min.js"

LEGACY_BLOCK_ORDER = (
    "paragraph",
    "image",
    "video",
    "audio",
    "link",
    "quote",
    "callout",
    "divider",
    "list",
)


def render_lesson(parsed: dict[str, Any], config: dict[str, Any], docx_path: Path, output_dir: Path) -> str:
    data = lesson_data(parsed)
    theme = LessonTheme.from_config(config)
    resolver = MediaResolver(docx_path, output_dir)

    title = data["cover"].get("title", theme.brand_name)
    author = data["cover"].get("author", "")
    definition = data["cover"].get("definition", "")
    purpose = data["cover"].get("purpose", "")
    preparation = data["cover"].get("preparation", "")
    page_title = theme.page_title(title)
    meta_description = theme.meta_description or definition or purpose or title

    logo_html = _render_logo(theme, resolver)
    brand_html = (
        f'<p class="text-uppercase small fw-semibold mb-2 opacity-75">{html.escape(theme.brand_name)}</p>'
        if theme.show_brand_on_cover and theme.brand_name
        else ""
    )
    author_html = (
        f'<p class="lead mb-0"><span class="opacity-75">{html.escape(theme.author_prefix)}</span> {html.escape(author)}</p>'
        if author
        else ""
    )

    sections_html = "\n".join(
        _render_section(section, index, resolver, theme)
        for index, section in enumerate(data["sections"], start=1)
    )

    footer_html = (
        f'<footer class="border-top py-4"><div class="{theme.container_class()} text-center text-body-secondary small">'
        f'<p class="mb-0">{html.escape(theme.footer)}</p></div></footer>'
        if theme.footer
        else ""
    )

    secondary_css = (
        f"      --lesson-secondary: {html.escape(theme.secondary_color)};\n"
        if theme.secondary_color
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="{html.escape(theme.lang)}" data-bs-theme="{html.escape(theme.theme)}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{html.escape(meta_description)}" />
  <meta name="generator" content="{html.escape(f'{PROJECT_NAME} — {AUTHOR_HANDLE}')}" />
  <title>{html.escape(page_title)}</title>
  <link rel="stylesheet" href="{BOOTSTRAP_CSS}" />
  <link rel="stylesheet" href="lesson.css" />
  <style>
    :root {{
      --bs-primary: {html.escape(theme.primary_color)};
      --bs-primary-rgb: {_hex_to_rgb_css(theme.primary_color)};
      --lesson-image-max-height: {html.escape(theme.image_max_height)};
{secondary_css}    }}
  </style>
</head>
<body class="lesson-page">
  <header class="lesson-hero bg-primary text-white py-5 mb-4">
    <div class="{theme.container_class()}">
      {logo_html}
      {brand_html}
      <h1 class="display-5 fw-bold mb-3">{html.escape(title)}</h1>
      {author_html}
      {f'<p class="mt-3 mb-0 fs-5 opacity-90">{_inline_html(definition)}</p>' if definition else ''}
      {f'<div class="alert alert-light text-dark mt-4 mb-0"><h2 class="h6 text-uppercase text-primary mb-2">{html.escape(theme.label_purpose)}</h2>{_text_html(purpose)}</div>' if purpose else ''}
      {f'<div class="alert alert-secondary mt-3 mb-0"><h2 class="h6 text-uppercase mb-2">{html.escape(theme.label_preparation)}</h2>{_text_html(preparation)}</div>' if preparation else ''}
    </div>
  </header>
  <main class="{theme.container_class()} pb-5">
    {sections_html}
  </main>
  {footer_html}
  <script src="{BOOTSTRAP_JS}"></script>
</body>
</html>
"""


def _render_logo(theme: LessonTheme, resolver: MediaResolver) -> str:
    if not theme.logo:
        return ""
    src = _resolve_media_src(theme.logo, resolver)
    alt = html.escape(theme.logo_alt or theme.brand_name or "Logo")
    return f'<img src="{html.escape(src)}" class="lesson-brand-logo mb-3" alt="{alt}" />'


def _section_blocks(section: dict[str, Any]) -> list[dict[str, Any]]:
    if blocks := section.get("blocks"):
        return blocks

    legacy: list[dict[str, Any]] = []
    for key in LEGACY_BLOCK_ORDER:
        if key not in section:
            continue
        value = section[key]
        if isinstance(value, list):
            for item in value:
                legacy.append({"type": key, "content": item})
        else:
            legacy.append({"type": key, "content": value})

    if question := section.get("question"):
        legacy.append(
            {
                "type": "question",
                "content": {"question": question, "answer": section.get("answer", "")},
            }
        )
    return legacy


def _render_section(section: dict[str, Any], index: int, resolver: MediaResolver, theme: LessonTheme) -> str:
    raw_heading = section.get("heading", f"{theme.label_section_fallback} {index}")
    heading = theme.section_heading(raw_heading, index)
    badge = theme.section_number_badge(index)
    badge_html = (
        f'<span class="badge bg-primary me-2 align-middle">{badge}</span>' if badge else ""
    )
    body_parts = [
        _render_block(block, index, block_index, resolver, theme)
        for block_index, block in enumerate(_section_blocks(section), start=1)
    ]
    body = "\n".join(part for part in body_parts if part)

    return f"""
<article class="card shadow-sm mb-4 lesson-section" id="section-{index}">
  <div class="card-body">
    <h2 class="card-title h4 text-primary border-bottom pb-2 mb-3">{badge_html}{html.escape(heading)}</h2>
    {body}
  </div>
</article>""".strip()


def _render_block(
    block: dict[str, Any],
    section_index: int,
    block_index: int,
    resolver: MediaResolver,
    theme: LessonTheme,
) -> str:
    block_type = block.get("type", "")
    content = block.get("content", "")

    if block_type == "paragraph":
        return f'<div class="card-text lesson-block">{_text_html(str(content))}</div>'
    if block_type == "list":
        items = "\n".join(
            f'<li class="list-group-item">{html.escape(item)}</li>' for item in _split_lines(str(content))
        )
        return f'<ul class="list-group list-group-flush mt-3 lesson-block lesson-list">{items}</ul>'
    if block_type == "question":
        return _render_question(content, section_index, block_index)
    if block_type == "image":
        return _render_image(str(content), resolver)
    if block_type == "video":
        return _render_video(str(content), resolver)
    if block_type == "audio":
        return _render_audio(str(content), resolver)
    if block_type == "link":
        return _render_link(str(content), theme)
    if block_type == "quote":
        return _render_quote(str(content))
    if block_type == "callout":
        return _render_callout(str(content), theme)
    if block_type == "divider":
        return '<hr class="lesson-divider my-4" />'
    return ""


def _render_question(content: Any, section_index: int, block_index: int) -> str:
    if isinstance(content, dict):
        question = str(content.get("question", ""))
        answer = str(content.get("answer", ""))
    else:
        question = str(content)
        answer = ""

    collapse_id = f"section-{section_index}-answer-{block_index}"
    return f"""
<div class="accordion mt-3 lesson-block" id="accordion-{section_index}-{block_index}">
  <div class="accordion-item">
    <h3 class="accordion-header">
      <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
        data-bs-target="#{collapse_id}" aria-expanded="false" aria-controls="{collapse_id}">
        {html.escape(question)}
      </button>
    </h3>
    <div id="{collapse_id}" class="accordion-collapse collapse" data-bs-parent="#accordion-{section_index}-{block_index}">
      <div class="accordion-body">{_text_html(answer)}</div>
    </div>
  </div>
</div>""".strip()


def _render_image(content: str, resolver: MediaResolver) -> str:
    src, caption = parse_pipe_value(content)
    resolved = html.escape(resolver.resolve(src))
    caption_html = (
        f'<figcaption class="figure-caption mt-2 text-center">{html.escape(caption)}</figcaption>'
        if caption
        else ""
    )
    return f"""
<figure class="lesson-media lesson-image figure mt-3 mb-0">
  <img src="{resolved}" class="figure-img img-fluid rounded shadow-sm" alt="{html.escape(caption or 'Imagem da aula')}" loading="lazy" />
  {caption_html}
</figure>""".strip()


def _render_video(content: str, resolver: MediaResolver) -> str:
    src, caption = parse_pipe_value(content)
    src = src.strip()
    caption_html = (
        f'<p class="small text-body-secondary mt-2 mb-0">{html.escape(caption)}</p>' if caption else ""
    )

    if video_id := youtube_embed_id(src):
        embed = f"https://www.youtube.com/embed/{video_id}"
        return f"""
<div class="lesson-media lesson-video ratio ratio-16x9 mt-3">
  <iframe src="{embed}" title="{html.escape(caption or 'Vídeo da aula')}" allowfullscreen loading="lazy"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"></iframe>
</div>{caption_html}""".strip()

    if video_id := vimeo_embed_id(src):
        embed = f"https://player.vimeo.com/video/{video_id}"
        return f"""
<div class="lesson-media lesson-video ratio ratio-16x9 mt-3">
  <iframe src="{embed}" title="{html.escape(caption or 'Vídeo da aula')}" allowfullscreen loading="lazy"></iframe>
</div>{caption_html}""".strip()

    resolved = html.escape(_resolve_media_src(src, resolver))
    return f"""
<div class="lesson-media lesson-video mt-3">
  <video class="w-100 rounded shadow-sm" controls preload="metadata" src="{resolved}"></video>
  {caption_html}
</div>""".strip()


def _render_audio(content: str, resolver: MediaResolver) -> str:
    src, caption = parse_pipe_value(content)
    src = src.strip()
    resolved = html.escape(_resolve_media_src(src, resolver))
    caption_html = (
        f'<p class="small text-body-secondary mt-2 mb-0">{html.escape(caption)}</p>' if caption else ""
    )
    return f"""
<div class="lesson-media lesson-audio mt-3">
  <audio class="w-100" controls preload="metadata" src="{resolved}"></audio>
  {caption_html}
</div>""".strip()


def _resolve_media_src(src: str, resolver: MediaResolver) -> str:
    lowered = src.lower()
    if lowered.startswith(("http://", "https://", "//")):
        return src
    return resolver.resolve(src)


def _render_link(content: str, theme: LessonTheme) -> str:
    label, url = parse_pipe_value(content)
    if url is None:
        url = label
        label = _short_url_label(url)
    safe_url = html.escape(url, quote=True)
    safe_label = html.escape(label)
    target = ' target="_blank" rel="noopener noreferrer"' if theme.link_opens_new_tab else ""
    return f"""
<p class="lesson-block lesson-link mt-3 mb-0">
  <a class="btn btn-outline-primary" href="{safe_url}"{target}>{safe_label}</a>
</p>""".strip()


def _render_quote(content: str) -> str:
    return f"""
<blockquote class="lesson-block lesson-quote border-start border-4 border-primary ps-3 my-3">
  {_text_html(content)}
</blockquote>""".strip()


def _render_callout(content: str, theme: LessonTheme) -> str:
    style = theme.callout_style
    return f"""
<div class="lesson-block alert alert-{style} mt-3 mb-0" role="note">
  {_text_html(content)}
</div>""".strip()


def _short_url_label(url: str) -> str:
    cleaned = url.replace("https://", "").replace("http://", "")
    return cleaned.rstrip("/")[:48] + ("…" if len(cleaned) > 48 else "")


def _hex_to_rgb_css(value: str) -> str:
    color = value.lstrip("#")
    if len(color) != 6:
        return "13, 110, 253"
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    return f"{r}, {g}, {b}"


def _split_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def _inline_html(value: str) -> str:
    return html.escape(value.strip()).replace("\n", "<br />")


def _text_html(value: str) -> str:
    escaped = html.escape(value.strip())
    return re.sub(r"\n{2,}", "</p><p class='mb-0'>", f"<p class='mb-0'>{escaped}</p>").replace("\n", "<br />")


def write_output(html_content: str, output_dir: Path, css_source: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(html_content, encoding="utf-8")
    (output_dir / "lesson.css").write_text(css_source.read_text(encoding="utf-8"), encoding="utf-8")
