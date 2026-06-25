from __future__ import annotations

from pathlib import Path
from .config import load_config
from .parser import parse_docx
from .dialogs import pick_docx_file, pick_output_dir
from .paths import app_root, css_path, default_config_path, output_dir, resolve_docx, sources_dir
from .renderer import render_lesson, write_output
from . import ui


def convert_lesson(
    input_path: Path,
    out_dir: Path | None = None,
    css_source: Path | None = None,
    config_path: Path | None = None,
) -> Path:
    path = resolve_docx(input_path)

    config = load_config(config_path or default_config_path())
    parsed = parse_docx(path)
    target = out_dir or output_dir()
    html = render_lesson(parsed, config, path, target)
    write_output(html, target, css_source or css_path())
    return target / "index.html"


def discover_docx_files() -> list[Path]:
    folder = sources_dir()
    return sorted(path.resolve() for path in folder.glob("*.docx") if path.is_file())


def sources_folder_label() -> str:
    folder = sources_dir()
    root = app_root()
    try:
        return str(folder.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(folder).replace("\\", "/")


def _choose_docx() -> Path:
    root = app_root()
    options = discover_docx_files()
    sources_label = sources_folder_label()

    ui.print_section("Arquivos Word")
    ui.print_hint(f"Salve seus .docx em {sources_label}/ para aparecerem nesta lista.")

    if options:
        for index, path in enumerate(options, start=1):
            ui.print_option(index, str(path.relative_to(root)))
    else:
        ui.print_hint("Nenhum arquivo encontrado ainda.")

    ui.print_option(0, "Abrir arquivo no computador…")
    print()

    default_choice = "1" if options else "0"

    while True:
        choice = ui.prompt("Escolha o arquivo", default_choice)
        if choice == "0":
            ui.print_hint("Abrindo seletor de arquivos…")
            picked = pick_docx_file(sources_dir())
            if picked is None:
                fallback = _prompt_docx_path_fallback()
                if fallback is not None:
                    return fallback
                ui.print_hint("Nenhum arquivo selecionado.")
                continue
            if picked.suffix.lower() != ".docx":
                ui.print_error("Selecione um arquivo .docx.")
                continue
            return picked

        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]

        ui.print_error("Opção inválida. Tente novamente.")


def _prompt_docx_path_fallback() -> Path | None:
    ui.print_hint("Seletor indisponível — informe o caminho manualmente.")
    custom = ui.prompt("Caminho do .docx")
    if not custom:
        return None
    path = Path(custom).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    if path.suffix.lower() == ".docx" and path.exists():
        return path
    ui.print_error("Arquivo .docx inválido ou não encontrado.")
    return None


def _choose_output_dir() -> Path:
    root = app_root()
    default_out = output_dir()
    try:
        default_label = str(default_out.relative_to(root)).replace("\\", "/")
    except ValueError:
        default_label = str(default_out).replace("\\", "/")

    ui.print_section("Saída")
    ui.print_option(1, f"Usar pasta padrão: {default_label}")
    ui.print_option(0, "Escolher pasta no computador…")
    print()

    while True:
        choice = ui.prompt("Onde salvar a aula", "1")
        if choice in ("", "1"):
            return default_out.resolve()

        if choice == "0":
            ui.print_hint("Abrindo seletor de pastas…")
            picked = pick_output_dir(default_out if default_out.is_dir() else app_root())
            if picked is not None:
                return picked
            fallback = _prompt_output_dir_fallback()
            if fallback is not None:
                return fallback
            ui.print_hint("Nenhuma pasta selecionada.")
            continue

        ui.print_error("Opção inválida. Tente novamente.")


def _prompt_output_dir_fallback() -> Path | None:
    ui.print_hint("Seletor indisponível — informe o caminho manualmente.")
    custom = ui.prompt("Pasta de saída")
    if not custom:
        return None
    path = Path(custom).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    return path


def run_interactive() -> int:
    ui.init_terminal()
    ui.print_banner()

    try:
        input_path = _choose_docx()
    except FileNotFoundError as error:
        ui.print_error(str(error))
        return 1

    out = _choose_output_dir()

    ui.print_working("Convertendo Word em aula HTML…")
    try:
        result = convert_lesson(input_path, out)
    except Exception as error:
        ui.print_error(str(error))
        return 1

    ui.print_success(result)
    return 0
