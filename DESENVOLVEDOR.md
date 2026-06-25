# Guia do desenvolvedor — DigitAula

Documentação para quem **mantém ou altera** a ferramenta (código, build, distribuição).

Professores que só **usam** o programa devem ler o **[Guia do professor](./GUIA-PROFESSOR.md)**.

---

## Início rápido

```bash
pip install -r requirements.txt   # só na primeira vez
python app.py                     # modo interativo
python app.py examples/geografia-brasil.docx
```

Gera `output/index.html` + `lesson.css` (+ `media/` quando houver arquivos locais).

## Estrutura

```
app.py
lesson/          parser, renderer, cli, config, paths, media, ui
assets/lesson.css
sources/         .docx do professor (listados no CLI)
examples/        modelo de referência
config.example.yaml
digitaula.spec
scripts/build.bat
```

## Tags suportadas

| Bloco | Campos / conteúdo |
|-------|-------------------|
| `[cover]` | `title`, `author`, `definition`, `purpose`, `preparation` |
| `[section]` | `heading` + blocos ordenados abaixo |

Blocos dentro de `[section]` (podem repetir e misturar na ordem):

| Tag | Formato |
|-----|---------|
| `paragraph`, `list`, `quote`, `callout` | `[tag] conteúdo [/tag]` |
| `question` + `answer` | duas linhas seguidas |
| `image`, `video`, `audio` | `[tag] url-ou-caminho \| legenda opcional [/tag]` |
| `link` | `[link] rótulo \| https://... [/link]` ou só a URL |
| `divider` | `[divider] [/divider]` |

Mídia local é copiada para `output/media/`. YouTube e Vimeo viram embed; URLs remotas diretas viram `<video>` / `<audio>`.

Regras: uma tag por linha; fechar blocos (`[/cover]`, `[/section]`). Modelos no [guia do professor](./GUIA-PROFESSOR.md).

## Personalização (white-label)

`config.example.yaml` → copiar para `config.yaml`.

| Seção | Exemplos de chaves |
|-------|-------------------|
| `brand` | `name`, `primary_color`, `secondary_color`, `logo`, `logo_alt` — paleta e seletor em `config.example.yaml` |
| `lesson` | `theme`, `container`, `footer`, `author_prefix`, `labels` |
| `sections` | `show_numbers`, `number_style` (`badge` / `text` / `hidden`) |
| `blocks` | `callout_style`, `image_max_height`, `link_opens_new_tab` |
| `meta` | `title_suffix`, `description` |

## Distribuir para o professor (sem Python)

```bash
pip install -r requirements.txt -r requirements-dev.txt
scripts\build.bat
```

Envie a pasta **`dist/DigitAula`** inteira (exe + `sources/` + `examples/` + guia). O professor não precisa de Python.

Variável `DIGITAULA_NO_PAUSE=1` desativa a pausa no fim do `.exe` (útil em testes automatizados).

## Stack

Python · python-docx · PyYAML · Bootstrap 5 (CDN) · PyInstaller (build)
