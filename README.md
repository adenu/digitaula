# DigitAula

**Monte no Word, publique no EAD.**

Ferramenta para transformar um `.docx` com marcações simples em **página web** — capa, seções, mídia e perguntas — pronta para o Moodle, Classroom ou qualquer ambiente EAD.

Desenvolvido por **[github.com/adenu](https://github.com/adenu)**.

---

## De onde veio

Trabalhei com material didático digital em contexto corporativo de educação e vi o mesmo padrão repetir: o professor tinha o conteúdo no Word, mas dependia de alguém de TI ou de uma fila de design para publicar cada atualização.

O DigitAula nasceu disso — uma saída direta: **o docente continua no Word**, marca o texto com tags (`[cover]`, `[section]`, `[image]`…) e gera o HTML localmente, sem login, sem editor proprietário, no próprio ritmo.

Não é plataforma. É uma ponte entre o que o professor já escreve e o que o EAD precisa receber.

---

## O que sai no final

- Capa com título, autor, objetivo e orientações
- Seções com texto, listas, imagens, vídeo, áudio, links
- Perguntas com resposta expansível
- Visual ajustável por `config.yaml` (cor da escola, rodapé, tema claro/escuro)

Arquivos gerados: `index.html`, `lesson.css` e, se houver mídia local, a pasta `media/`.

---

## Documentação

| Quem | Guia |
|------|------|
| Professor | [GUIA-PROFESSOR.md](./GUIA-PROFESSOR.md) |
| Desenvolvedor | [DESENVOLVEDOR.md](./DESENVOLVEDOR.md) |

Exemplo: [`examples/geografia-brasil.docx`](./examples/geografia-brasil.docx)

---

## Uso rápido

```bash
pip install -r requirements.txt
python app.py
python app.py examples/geografia-brasil.docx
```

Para gerar o `.exe` e enviar a um professor sem Python:

```bash
pip install -r requirements.txt -r requirements-dev.txt
scripts\build.bat
```

A pasta `dist/DigitAula` contém o `DigitAula.exe` e tudo que ele precisa.

---

## Stack

Python · python-docx · PyYAML · Bootstrap 5 · PyInstaller

---

## Licença

MIT — veja [LICENSE](./LICENSE).
