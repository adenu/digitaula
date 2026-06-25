# Guia do professor — montar a aula no Word e gerar o HTML

Este guia é para quem **só utiliza** a ferramenta — não precisa saber programar.

Você só precisa usar o **Microsoft Word** (ou LibreOffice Writer, salvando em `.docx`).

> Desenvolvedores: veja [DESENVOLVEDOR.md](./DESENVOLVEDOR.md).

---

## O que você vai fazer

1. Escrever a aula no Word usando **marcadores especiais** (tags) — parecidos com colchetes `[assim]`.
2. Rodar um programa no computador que **transforma** esse Word em uma **página web** pronta para abrir no navegador ou enviar para alunos.

**Resultado:** um arquivo `index.html` com visual de site (capa, seções, listas e perguntas expansíveis).

---

## Antes de começar (só na primeira vez)

Se alguém da equipe de TI enviou uma pasta com **`DigitAula.exe`**, **não precisa instalar nada**. Pule para o [Passo 6](#passo-6--gerar-a-aula-html).

Dentro da pasta você deve ter:

- `DigitAula.exe` — o programa
- `sources/` — **seus** arquivos Word (aparecem na lista ao gerar)
- `examples/` — modelo de referência para copiar
- `config.example.yaml` — personalização opcional
- `GUIA-PROFESSOR.md` — este guia

Se não recebeu o `.exe`, peça à equipe de TI para gerar o pacote (instruções em [DESENVOLVEDOR.md](./DESENVOLVEDOR.md)).

---

## Passo 1 — Abra um modelo ou comece do zero

**Modelo de referência:** abra, copie a estrutura e salve a sua versão em `sources/`:

`examples/geografia-brasil.docx` → salve como `sources/minha-aula.docx`

**Do zero:** crie um documento Word em branco (`.docx`).

---

## Passo 2 — Regras importantes do Word

| Regra | Por quê |
|-------|---------|
| **Uma tag por linha** | Cada `[algo]` ou `[campo] texto [/campo]` fica sozinha no parágrafo |
| **Digite as tags exatamente** | `[cover]` funciona; `[Cover]` ou `(cover)` **não** |
| **Sempre feche os blocos** | Abriu `[cover]` → termine com `[/cover]` |
| **Salve como .docx** | Não use `.doc` antigo nem PDF |

No Word: pressione **Enter** no fim de cada linha de tag. Não use tabelas nem caixas de texto para as tags.

---

## Passo 3 — Monte a capa da aula

A capa fica dentro de um bloco `[cover] ... [/cover]`.

Copie o modelo abaixo e **troque os textos** pelos seus (mantenha os colchetes):

```text
[cover]
[title] Nome da sua aula [/title]
[author] Seu nome [/author]
[definition] Uma frase que resume o tema. [/definition]
[purpose] O que o aluno vai aprender ao final. [/purpose]
[preparation] O que revisar antes (opcional). [/preparation]
[/cover]
```

| Campo | Obrigatório? | Aparece na aula como |
|-------|--------------|----------------------|
| `title` | Sim | Título grande no topo |
| `author` | Não | “Por …” |
| `definition` | Não | Texto logo abaixo do título |
| `purpose` | Não | Caixa “Objetivo” |
| `preparation` | Não | Caixa “Antes de começar” |

Se não quiser objetivo ou preparação, **apague a linha inteira** (não deixe a tag vazia).

---

## Passo 4 — Adicione as seções do conteúdo

Cada **seção** da aula é um bloco `[section] ... [/section]`.

Dentro de cada seção você pode usar:

| Tag | Para quê | Exemplo |
|-----|----------|---------|
| `[heading]` | Título da seção | `[heading] O clima no Brasil [/heading]` |
| `[paragraph]` | Texto corrido | `[paragraph] O Brasil tem climas variados... [/paragraph]` |
| `[list]` | Lista com marcadores | Ver modelo abaixo |
| `[image]` | Foto ou ilustração | Ver [mídia e links](#mídia-links-e-destaques) |
| `[video]` | Vídeo (YouTube, Vimeo ou arquivo) | Ver [mídia e links](#mídia-links-e-destaques) |
| `[audio]` | Áudio / narração | Ver [mídia e links](#mídia-links-e-destaques) |
| `[link]` | Botão com link externo | Ver [mídia e links](#mídia-links-e-destaques) |
| `[quote]` | Citação em destaque | `[quote] Frase importante. [/quote]` |
| `[callout]` | Caixa de dica ou aviso | `[callout] Revise o mapa antes de continuar. [/callout]` |
| `[divider]` | Linha separadora | `[divider] [/divider]` |
| `[question]` + `[answer]` | Pergunta que o aluno clica para ver a resposta | Ver modelo abaixo |

### Exemplo de seção só com texto

```text
[section]
[heading] Introdução [/heading]
[paragraph] Escreva aqui o texto da aula. Pode ter várias frases em um único parágrafo. [/paragraph]
[/section]
```

### Exemplo de seção com lista

Os itens ficam **na mesma tag** `[list]`, um por linha:

```text
[section]
[heading] As cinco regiões [/heading]
[list] Norte — floresta e rios
Nordeste — litoral e semiárido
Sul — inverno mais frio [/list]
[/section]
```

### Exemplo de seção com pergunta e resposta

```text
[section]
[heading] Para fixar [/heading]
[question] Qual é a maior região do Brasil? [/question]
[answer] A região Norte, em extensão territorial. [/answer]
[/section]
```

Você pode repetir `[section]` quantas vezes precisar — uma seção após a outra.

Dentro da mesma seção, **pode misturar** parágrafos, imagens, vídeos e outros blocos na ordem em que quiser que apareçam na aula.

### Mídia, links e destaques

Use o caractere ` | ` (espaço, barra vertical, espaço) para separar **endereço** e **legenda** quando quiser um texto explicativo.

| Tag | O que colocar dentro | Exemplo |
|-----|----------------------|---------|
| `[image]` | URL na internet **ou** caminho de arquivo | `[image] fotos/mapa.jpg \| Mapa das regiões [/image]` |
| `[video]` | Link do YouTube/Vimeo **ou** arquivo `.mp4` | `[video] https://youtu.be/abc123 \| Vídeo introdutório [/video]` |
| `[audio]` | Link ou arquivo `.mp3` | `[audio] audios/narracao.mp3 \| Ouça o texto [/audio]` |
| `[link]` | Texto do botão \| endereço | `[link] Site do IBGE \| https://www.ibge.gov.br/ [/link]` |

**Arquivos no computador:** coloque fotos, áudios e vídeos numa pasta ao lado do Word (ex.: `fotos/`, `audios/`) e use o caminho relativo na tag. Na geração, os arquivos são copiados para a pasta `output/media/`.

**Só link, sem legenda:**

```text
[link] https://www.ibge.gov.br/ [/link]
```

**Linha separadora e destaques:**

```text
[divider] [/divider]
[callout] Atenção: esta atividade vale pontos para a avaliação. [/callout]
[quote] Geografia é ler o território para entender a sociedade. [/quote]
```

---

## Passo 5 — Salve o arquivo

Salve com um nome claro, por exemplo:

`minha-aula-geografia.docx`

Guarde em `sources/` para o programa listar automaticamente, ou use a opção **0** para abrir o seletor de arquivos do Windows.

---

## Passo 6 — Gerar a aula (HTML)

1. Salve seu `.docx` em `sources/` (recomendado — aparece na lista).
2. Dê **dois cliques** em `DigitAula.exe`.
3. O programa pergunta:
   - **Qual arquivo Word** — escolha o número da lista ou a opção **0** para abrir o Explorer e buscar o `.docx`.
   - **Onde salvar** — Enter para `output` (padrão) ou opção **0** para escolher a pasta no Explorer.
4. Quando aparecer **“Pronto: …\output\index.html”**, pressione Enter para fechar a janela.

**Atalho:** arraste o arquivo `.docx` em cima do `DigitAula.exe` (se o Windows permitir) ou abra o Prompt na pasta e digite:

```text
DigitAula.exe sources\minha-aula.docx
```


## Passo 7 — Ver e compartilhar com os alunos

1. Abra a pasta `output` (ou a pasta que você escolheu).
2. Dê **dois cliques** em `index.html` — abre no Chrome, Edge ou Firefox.
3. Para enviar aos alunos:
   - Envie a pasta inteira (`index.html`, `lesson.css` e, se houver, `media/`), **ou**
   - Hospede num drive/servidor que sirva arquivos estáticos (peça ajuda à TI).

A página precisa de **internet na primeira abertura** para carregar o visual (Bootstrap). O texto da aula em si está nos arquivos locais.

---

## Personalizar aparência da aula (opcional)

Se alguém da equipe puder editar um arquivo de texto:

1. Copie `config.example.yaml` para `config.yaml`.
2. Ajuste nome da escola, cores, logo, tema claro/escuro, rótulos (“Objetivo”, “Antes de começar”), numeração das seções, rodapé e mais.

### Escolher cores (sem saber o que é “hex”)

O arquivo pede um **código de cor** que sempre começa com `#`. Você não precisa entender o significado — só copiar:

1. **Paleta pronta** — no final de `config.example.yaml` há sugestões como *Azul institucional → `#2563eb`*. Copie o código e cole em `primary_color`.
2. **Seletor online** — abra [htmlcolorcodes.com/color-picker](https://htmlcolorcodes.com/color-picker/), clique na cor da sua escola e copie o código `#` que o site mostrar.

Exemplo mínimo:

```yaml
brand:
  name: "Escola Municipal Exemplo"
  primary_color: "#2563eb"   # Azul institucional — veja paleta no config.example.yaml
lesson:
  footer: "Material de apoio — 2026"
  theme: "light"
sections:
  show_numbers: true
  number_style: "badge"
```

Todas as opções comentadas estão em `config.example.yaml`.

---

## Erros comuns

| O que aconteceu | O que fazer |
|-----------------|-------------|
| `Linha não reconhecida` | Alguma linha não está no formato de tag. Confira colchetes `[]` e se cada tag está em **linha separada**. |
| `Arquivo não encontrado` | Caminho do `.docx` errado ou arquivo não salvo. |
| `Mídia não encontrada` / `Arquivo não encontrado: fotos/...` | Caminho da imagem, áudio ou vídeo errado. Confira a pasta ao lado do Word. |
| Imagem ou vídeo não aparece na página | Envie a pasta `media/` junto com o HTML, ou use link `https://` na tag. |
| Vídeo do YouTube não carrega | Precisa de internet para assistir. Confira se o link está completo. |
| Lista não aparece / erro na lista | Use `[list] item1` + Enter + `item2` + Enter + `[/list]` na **mesma** tag de abertura/fechamento, não linhas soltas entre `[list]` e `[/list]`. |
| Tag de fechamento inesperada | Falta abrir `[cover]` ou `[section]`, ou nome diferente no fechamento (`[/cover]` vs `[/Cover]`). |
| Página sem formatação | Abra `index.html` pela pasta `output`; não mova só o HTML sem o `lesson.css`. |

---

## Checklist rápido antes de gerar

- [ ] Arquivo salvo como `.docx`
- [ ] `[cover]` tem `[title]` e fecha com `[/cover]`
- [ ] Cada `[section]` fecha com `[/section]`
- [ ] Tags digitadas em **minúsculas** (`[heading]`, não `[Heading]`)
- [ ] Listas no formato `[list] item … [/list]` com itens entre as tags
- [ ] Imagens e áudios locais estão na pasta correta (ex.: `fotos/arquivo.jpg`)
- [ ] Links de vídeo (YouTube) estão completos e com `https://`

---

## Modelo completo para copiar

```text
[cover]
[title] Geografia do Brasil [/title]
[author] Profa. Maria [/author]
[definition] Visão geral das regiões brasileiras. [/definition]
[purpose] Reconhecer as cinco regiões e um traço de cada uma. [/purpose]
[/cover]

[section]
[heading] Um país continental [/heading]
[paragraph] O Brasil é enorme e reúne diferentes climas, relevos e biomas. [/paragraph]
[/section]

[section]
[heading] Regiões [/heading]
[list] Norte
Nordeste
Centro-Oeste
Sudeste
Sul [/list]
[/section]

[section]
[heading] Pergunta [/heading]
[question] Quantas regiões o IBGE define? [/question]
[answer] Cinco regiões. [/answer]
[/section]

[section]
[heading] Material extra [/heading]
[image] fotos/mapa.jpg | Mapa das regiões [/image]
[link] IBGE | https://www.ibge.gov.br/ [/link]
[video] https://www.youtube.com/watch?v=exemplo | Vídeo complementar [/video]
[/section]
```

---

## Precisa de ajuda?

- Modelo de referência: `examples/geografia-brasil.docx`
- Seus arquivos de trabalho: pasta `sources/`
- Índice da documentação: [README.md](./README.md)

---

## Sobre o DigitAula

Ferramenta criada por [github.com/adenu](https://github.com/adenu) para quem produz aula no Word e precisa publicar no EAD sem depender de fila técnica a cada revisão.

Código aberto: [github.com/adenu/digitaula](https://github.com/adenu/digitaula)
