# DigitAula

**Monte no Word, publique no EAD.**

Ferramenta open source para docentes converterem um `.docx` estruturado em **página web** pronta para abrir no navegador ou publicar em **LMS** (Moodle, Google Classroom, ambientes EAD etc.).

---

## Por que este projeto existe

Na Educação a Distância, o gargalo costuma não ser a didática — é a **distância entre a ideia do professor e o material publicado**: filas de design, templates engessados ou ferramentas que exigem perfil técnico.

O **DigitAula** devolve **autonomia editorial ao docente**. Você organiza a aula no Word, com marcações simples, e gera um HTML responsivo com capa, seções, mídia e atividades interativas — **no seu ritmo**, revisando e republicando quando quiser.

O professor permanece no ambiente que já domina; a ferramenta cuida da conversão.

---

## O que você consegue produzir

- **Capa** com título, autor, objetivos e orientações prévias
- **Seções** com texto, listas e perguntas com resposta expansível
- **Mídia**: imagens, vídeos (YouTube/Vimeo ou arquivo), áudio e links
- **Destaques**: citações, caixas de aviso e separadores visuais
- **Visual configurável** (nome da instituição, cor da marca, rodapé) via YAML

Saída: `index.html` + `lesson.css` (+ pasta `media/` quando há arquivos locais).

---

## Como funciona

```
Word (.docx) com tags  →  DigitAula  →  aula HTML (Bootstrap 5)
```

1. O docente escreve no Word usando tags como `[cover]`, `[section]`, `[paragraph]`, `[image]`, `[video]`…
2. Executa a ferramenta (`DigitAula.exe` no Windows ou `python app.py` no desenvolvimento).
3. Abre ou publica o HTML gerado na plataforma de ensino.

---

## Documentação

| Perfil | Guia |
|--------|------|
| **Professor** — monta o Word e gera a aula | [**Guia do professor**](./GUIA-PROFESSOR.md) |
| **Desenvolvedor** — código, build e distribuição | [**Guia do desenvolvedor**](./DESENVOLVEDOR.md) |

Exemplo pronto: [`examples/geografia-brasil.docx`](./examples/geografia-brasil.docx)

---

## Início rápido (desenvolvimento)

```bash
pip install -r requirements.txt
python app.py                              # modo interativo
python app.py examples/geografia-brasil.docx # conversão direta
```

### Distribuir para o professor (sem Python)

```bash
pip install -r requirements.txt -r requirements-dev.txt
scripts\build.bat
```

Envie a pasta `dist/DigitAula` inteira. O docente só precisa executar `DigitAula.exe`.

---

## Stack

Python · python-docx · PyYAML · Bootstrap 5 (CDN) · PyInstaller

---

## Estrutura do repositório

```
app.py
lesson/              # parser, renderer, CLI, mídia
assets/lesson.css
sources/             # seus .docx (listados no CLI)
examples/            # modelo de referência
config.example.yaml
scripts/build.bat
```
