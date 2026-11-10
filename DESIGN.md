---
name: Achados católicos
description: Relatório do monitor da Estante Virtual, lido como a guarda de um livro de sebo.
colors:
  g0: "#ffffff"
  g1: "#eceeef"
  g2: "#dadde0"
  g3: "#c0c4c9"
  g4: "#999ea6"
  g5: "#646972"
  g6: "#4f535a"
  g7: "#35383e"
  g8: "#1c1e22"
  tabua: "#1f2b4a"
  ano-cor: "#1f2b4a"
  sangue: "#6b1f2a"
  carimbo: "#5b3fa6"
  carimbo-fundo: "#efeaf9"
  sobre-carimbo: "#ffffff"
  rotulo-fundo: "#ffffff"
  rotulo-fio: "#c0c4c9"
  rotulo-suave: "#4f535a"
  rotulo-tinta: "#1c1e22"
  pano-vinho: "#5b1a24"
  pano-verde: "#23402f"
  pano-indigo: "#1f2b4a"
  pano-ocre: "#7a5a1c"
  pano-ameixa: "#4a2340"
  pano-ardosia: "#3a4148"
  pano-tabaco: "#5a2d14"
typography:
  display:
    fontFamily: "\"Source Serif 4\", Georgia, \"Times New Roman\", serif"
    fontSize: "clamp(21px, 2.3vw, 28px)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "\"Source Serif 4\", Georgia, \"Times New Roman\", serif"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1.2
  title:
    fontFamily: "\"Source Serif 4\", Georgia, \"Times New Roman\", serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.005em"
  ano:
    fontFamily: "\"Source Serif 4\", Georgia, \"Times New Roman\", serif"
    fontSize: "21px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontFeature: "\"tnum\", \"lnum\""
  preco:
    fontFamily: "Kalam, \"Segoe Print\", \"Bradley Hand\", cursive"
    fontSize: "28px"
    fontWeight: 400
    lineHeight: 1.15
  preco-antigo:
    fontFamily: "Kalam, \"Segoe Print\", \"Bradley Hand\", cursive"
    fontSize: "16px"
    fontWeight: 700
    lineHeight: 1
  body:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.45
  body-sm:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.45
  label:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    letterSpacing: "0.06em"
  carimbo:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "11px"
    fontWeight: 800
    lineHeight: 1.5
    letterSpacing: "0.12em"
  etiqueta:
    fontFamily: "system-ui, -apple-system, \"Segoe UI\", Roboto, sans-serif"
    fontSize: "11.5px"
    fontWeight: 600
    letterSpacing: "0.04em"
rounded:
  carimbo: "3px"
  sm: "6px"
  md: "8px"
  ficha: "10px"
  aviso: "12px"
  gaveta: "16px"
  pilula: "999px"
spacing:
  gut: "40px"
  gut-celular: "16px"
  trilho: "264px"
  corpo: "32px"
  grade: "16px"
  ficha: "14px"
  ficha-celular: "12px"
components:
  button-primary:
    backgroundColor: "{colors.carimbo}"
    textColor: "{colors.sobre-carimbo}"
    rounded: "{rounded.md}"
    padding: "8px 14px"
  button-filtros:
    backgroundColor: "{colors.g0}"
    textColor: "{colors.g8}"
    rounded: "{rounded.md}"
    padding: "6px 12px"
  aba:
    textColor: "#cdd4e6"
    rounded: "8px 8px 0 0"
    padding: "12px 18px"
  aba-ativa:
    backgroundColor: "{colors.g1}"
    textColor: "{colors.carimbo}"
    rounded: "8px 8px 0 0"
    padding: "12px 18px"
  tema:
    textColor: "{colors.g6}"
    rounded: "{rounded.pilula}"
    padding: "6px 12px"
  tema-ativo:
    backgroundColor: "{colors.carimbo-fundo}"
    textColor: "{colors.carimbo}"
    rounded: "{rounded.pilula}"
    padding: "6px 12px"
  chip:
    backgroundColor: "{colors.g0}"
    textColor: "{colors.g8}"
    rounded: "{rounded.pilula}"
    padding: "3px 6px 3px 11px"
  input-busca:
    backgroundColor: "{colors.g0}"
    textColor: "{colors.g8}"
    rounded: "{rounded.md}"
    padding: "10px 12px 10px 36px"
  ficha:
    backgroundColor: "{colors.g0}"
    textColor: "{colors.g8}"
    rounded: "{rounded.ficha}"
    padding: "14px 14px 12px"
  carimbo:
    textColor: "{colors.carimbo}"
    typography: "{typography.carimbo}"
    rounded: "{rounded.carimbo}"
    padding: "1px 7px 0"
  etiqueta:
    backgroundColor: "{colors.g0}"
    textColor: "{colors.g7}"
    typography: "{typography.etiqueta}"
    padding: "1px 8px"
  rotulo:
    backgroundColor: "{colors.rotulo-fundo}"
    textColor: "{colors.rotulo-tinta}"
    padding: "14px 22px 13px"
---

# Design System: Achados católicos

## Overview

**Creative North Star: "A guarda do livro de sebo"**

Cada achado se lê como a folha de guarda de um livro usado: o ano impresso em serifa grande, o preço anotado a lápis no canto, circulado quando é pechincha e riscado e reescrito quando cai, a etiqueta do livreiro colada no pé e, no topo da página, uma faixa de papel de guarda marmorizado índigo. O mundo é frio e claro (grafite sobre papel acinzentado), não creme; o calor fica para a marmorização, para os panos de encadernação e para a tinta violeta do carimbo.

A densidade é de ferramenta de triagem: fichas compactas em grade, um trilho de filtros com contagens vivas e nada que atrase a leitura de preço, ano e título. Os materiais do sebo (lápis, carimbo, fio duplo, pano, papel marmorizado) não são ornamento: cada um carrega um dado. O lápis é o preço, o carimbo é o evento, a etiqueta é o sebo, o pano é a ausência de capa.

Um único movimento assinatura existe, e só para o que é novo para o leitor: o carimbo bate e o lápis circula, uma vez.

**Key Characteristics:**
- Neutros saídos de uma régua única de grafite com 9 tons (g0 a g8), com par claro e escuro.
- Uma tinta de estado só, o violeta de carimbo, para tudo o que é vivo: novo, preço caiu, aba ativa, filtro escolhido, foco, seleção.
- Marmorização procedural (SVG feTurbulence + feDisplacementMap) apenas na faixa do topo.
- Três vozes de letra: serifa (títulos e ano), lápis manuscrito (preço), sans do sistema (interface).
- Materiais com função: círculo a lápis, preço riscado, etiqueta de fio duplo, encadernação de pano gerada.

## Colors

Grafite frio sobre papel claro, com um índigo profundo no topo e um violeta de carimbo como única tinta de estado.

### Primary
- **Violeta de Carimbo** (carimbo): a tinta de todo estado vivo. Borda e texto do carimbo "Novo / Preço caiu / Mais um exemplar", texto e filete superior da aba ativa, tema ativo (com o fundo Lilás de Mata-borrão), rádio marcado no índice, `accent-color` de caixas e selects, contorno de foco, seleção de texto, botão primário, contagem de filtros ativos. No tema escuro vira um lilás claro, e o texto sobre ele inverte (sobre-carimbo).
- **Lilás de Mata-borrão** (carimbo-fundo): fundo da pílula de tema ativo; nunca aparece sem o violeta por cima.

### Secondary
- **Índigo de Guarda** (tabua): fundo da faixa marmorizada e do aviso flutuante "Há achados novos". A marmorização desenha sobre ele veios em índigo, bordô e um tom de pergaminho.
- **Índigo de Prelo** (ano-cor): a cor do ano em cada ficha. Igual ao índigo da faixa no claro; no escuro sobe para um azul-acinzentado claro para manter a leitura.

### Tertiary
- **Bordô de Veio** (sangue): só o complemento "· até 1958" no título do rótulo, ecoando o veio bordô da marmorização.
- **Panos de encadernação** (pano-vinho, pano-verde, pano-indigo, pano-ocre, pano-ameixa, pano-ardosia, pano-tabaco): sete tecidos escolhidos por hash do código do item quando não há capa. O texto sobre o pano é dourado de gravação a quente (#e7d6a2, fixo no componente).

### Neutral
- **Régua de Grafite** (g0 a g8): todos os neutros. Papel das fichas e campos (g0; g2 no escuro), chão da página (g1), fios (g2; g3 no escuro), bordas de controles (g3), fio duplo da etiqueta (g4), texto terciário e contagens (g5), texto secundário (g6), lápis e texto de controles (g7), tinta principal (g8). No escuro a régua inverte inteira.
- **Rótulo** (rotulo-fundo, rotulo-fio, rotulo-suave, rotulo-tinta): o rótulo de papel colado sobre a faixa é claro nos dois temas, por isso usa valores fixos da régua clara (g0, g3, g6, g8) em vez das variáveis que invertem.

### Named Rules
**A Regra da Tinta Única.** O violeta de carimbo é a única cor de estado. Se algo está ativo, novo, escolhido ou focado, está em violeta; se não está, não está. Nenhuma outra matiz marca estado na área de papel.

**A Regra da Régua.** Nenhum neutro fora de g0 a g8 nas superfícies de papel. Cinza novo entra como passo da régua ou não entra.

**A Regra do Rótulo Fixo.** O rótulo e o que fica sobre a faixa índigo não invertem no tema escuro: papel claro sobre guarda escura, nos dois temas.

## Typography

**Display Font:** Source Serif 4 (com Georgia, "Times New Roman", serif), pesos 600 e 700, eixo opsz
**Body Font:** system-ui (com -apple-system, "Segoe UI", Roboto, sans-serif)
**Label/Mono Font:** Kalam (com "Segoe Print", "Bradley Hand", cursive), a mão do lápis, pesos 400 e 700

**Character:** A serifa é a página impressa (título do livro, ano); o Kalam é a anotação do livreiro (preço); a sans do sistema é a ferramenta em volta. Números de preço, ano e contagens usam algarismos tabulares e alinhados.

### Hierarchy
- **Display** (700, clamp(21px, 2.3vw, 28px), 1.12): título "Achados católicos" no rótulo da faixa.
- **Headline** (600, 19px, 1.2; 17px no celular): título da listagem ("Todos os achados"), com a contagem em sans 14px ao lado.
- **Ano** (700, 21px, 1; tabular): o ano de cada ficha, em Índigo de Prelo. Sem ano: "s.d." em itálico 600, grafite g5.
- **Title** (600, 17px, 1.25): título do livro na ficha, `text-wrap: pretty`.
- **Preço** (Kalam 400, 28px, 1.15; 24px no celular; traço de 0.25px): o preço a lápis no canto da ficha, "R$" a 0.62em. Também o título manuscrito do estado vazio (Kalam 400, 26px, girado -1.5deg).
- **Preço antigo** (Kalam 700, 16px, 1): preço anterior riscado com traço de 2px na cor do lápis.
- **Body** (400, 15px, 1.45): interface, abas, índice. Autor e editora a 14px em g6.
- **Body pequeno** (400, 13px, 1.45): descrição do sebo (2 linhas), contagens, rodapé; pé da ficha a 12.5px.
- **Label** (700, 12px, 0.06em, maiúsculas): títulos de grupo do trilho de filtros (Preço, Época, Capa), em g5.
- **Carimbo** (800, 11px, 0.12em, maiúsculas) e **Etiqueta** (600, 11.5px, 0.04em, maiúsculas): os dois únicos usos de maiúsculas espaçadas além dos rótulos de grupo, ambos imitando objetos (carimbo de borracha, etiqueta impressa).

### Named Rules
**A Regra do Lápis.** O Kalam escreve preços e a nota manuscrita do estado vazio. Nunca títulos, nunca interface, nunca rótulos.

**A Regra dos Algarismos.** Todo número que se compara (preço, ano, contagem) usa `tabular-nums lining-nums`.

## Layout

Coluna de até 1480px com calha lateral de 40px (16px abaixo de 900px). No desktop, o corpo é uma grade de duas colunas: trilho de filtros de 264px, fixo (sticky a 68px do topo, com rolagem própria) e a área de fichas, separados por 32px. Acima do corpo, a faixa marmorizada (rótulo à esquerda, indicador da rodada à direita, abas encostadas na borda inferior) e uma barra de temas fixa no topo, translúcida com desfoque, com rolagem horizontal e máscara de fade de 40px à direita.

A grade de fichas usa `repeat(auto-fill, minmax(min(100%, 320px), 1fr))` com espaço de 16px. Colunas inteiras de 320 a ~440px: a área de fichas é um container (`container-type: inline-size`) e, abaixo de 655px de container, grade, cabeçalho e chips ficam limitados a 440px; entre 656 e 991px, a 896px. Assim uma coluna nunca se estica além de ~440px.

Até 1100px, o trilho vira gaveta inferior (cantos de 16px no topo, até 86vh, entra de baixo) com fundo escurecido e o botão "Filtros" aparece na barra de temas com a contagem de filtros ativos. Até 900px, a ficha encolhe (capa de 64 por 88px, padding de 12px) e o rótulo ocupa a largura toda.

A ficha é uma grade interna de 76px (capa de 76 por 104px) + 1fr com 14px entre colunas; o preço flutua no canto superior direito e a linha do ano reserva 96px à direita para ele.

## Elevation & Depth

Híbrido discreto: o papel se distingue do chão por tom (g0 sobre g1) mais uma sombra ambiente bem baixa; a profundidade forte fica para o que flutua sobre o conteúdo (rótulo sobre a guarda, aviso, gaveta). Não há sombras deslocadas duras.

### Shadow Vocabulary
- **Papel** (`box-shadow: 0 1px 2px rgba(28,30,34,.06), 0 4px 14px rgba(28,30,34,.05)`; no escuro `0 1px 2px rgba(0,0,0,.4), 0 4px 14px rgba(0,0,0,.25)`): fichas e estado vazio em repouso.
- **Papel em foco** (`box-shadow: 0 2px 4px rgba(28,30,34,.07), 0 10px 26px rgba(28,30,34,.09)`): ficha sob o ponteiro, com borda subindo para g3.
- **Rótulo colado** (`box-shadow: 0 1px 1px rgba(0,0,0,.35), 0 8px 22px rgba(5,10,25,.38)`): o rótulo de papel sobre a faixa índigo.
- **Capa** (`box-shadow: inset 0 0 0 1px rgba(0,0,0,.06), 1px 2px 4px rgba(0,0,0,.18)`): a capa ou o pano, como um livro pequeno pousado.
- **Flutuante** (`box-shadow: 0 10px 30px rgba(10,15,30,.35)`): aviso de relatório novo.
- **Gaveta** (`box-shadow: 0 -10px 40px rgba(10,15,30,.3)`): gaveta de filtros no celular.

### Named Rules
**A Regra do Papel Baixo.** Fichas ficam quase rentes ao chão. Sombra forte é só para o que está colado ou flutuando sobre outra camada.

## Shapes

Cantos suaves de papel cortado: fichas e estado vazio com 10px, campos e botões com 8px, linhas do índice com 6px, carimbo e capa com 3px (objetos físicos quase retos), pílulas de 999px para temas, chips e o indicador da rodada. Abas têm só os cantos de cima arredondados (8px). Fios são de 1px, com dois desvios deliberados: o pé da ficha separado por fio tracejado (1px dashed) e a etiqueta do sebo com fio duplo de 3px. O rótulo tem fio interno a 4px da borda, como etiqueta de papelaria. O carimbo é girado de -1 a -5deg (por hash) e o lápis é sempre um traço solto e arredondado (`stroke-linecap: round`), nunca uma forma geométrica fechada.

## Components

### Buttons
Ação direta e curta, sem cerimônia.
- **Shape:** cantos de 8px.
- **Primary:** fundo e borda em violeta de carimbo, texto sobre-carimbo, 600, padding 8px 14px. Hover: `filter: brightness(1.1)`.
- **Sobre a faixa índigo (aviso):** inverte para fundo branco e texto índigo.
- **Filtros (celular):** fundo de papel, borda g3, 600 14px, padding 6px 12px, com contador em pílula violeta de 20px.
- **Texto ("Limpar filtros"):** sem caixa, violeta, sublinhado com offset de 3px.

### Abas
Marcadores de livro que saem da faixa.
- **Style:** sobre um véu índigo translúcido na base da faixa; 600 15px, texto #cdd4e6, contagem 500 13px #9aa5c2.
- **Hover:** texto branco, fundo branco a 7%.
- **Ativa:** fundo da cor do chão (a aba "encaixa" na página), texto violeta e filete violeta de 3px no topo (`inset 0 3px 0`).
- **Teclado:** setas esquerda e direita trocam a aba (role tablist).

### Chips
- **Temas:** pílulas sem borda, texto g6 14px com contagem g5 12px; hover em papel g0; ativo com borda violeta, fundo lilás e texto violeta 600; tema sem resultados a 45% de opacidade.
- **Filtros ativos:** pílulas removíveis com borda g3 sobre papel, 13px, ícone X em SVG de 14px; hover põe borda e texto em violeta.

### Cards / Containers (Ficha)
- **Corner Style:** 10px.
- **Background:** papel (g0; g2 no escuro), borda de fio.
- **Shadow Strategy:** Papel em repouso, Papel em foco no hover (ver Elevation & Depth).
- **Internal Padding:** 14px 14px 12px (12px no celular).
- **Estrutura:** capa à esquerda (3 linhas), ano + carimbo, título serifado (o link cobre a ficha inteira), autor · editora, descrição de 2 linhas, pé tracejado com etiqueta do sebo, frete grátis em 600, datas "anunciado / visto" e "entrou por:" com os termos que pontuaram.
- **Estreia:** ficha nova desde a última visita ganha borda com 45% de violeta.

### Inputs / Fields
- **Style:** borda g3 de 1px, fundo de papel, cantos de 8px; busca com lupa SVG de 16px a 11px da esquerda.
- **Focus:** contorno violeta de 2px no lugar da borda. Foco global: `outline: 2px solid` violeta, offset 2px.
- **Caixas e selects:** `accent-color` violeta, caixa de 17px.

### Navigation (Índice de filtros)
Índice de livro com linha pontilhada.
- **Style:** cada opção é uma linha "rótulo ······ contagem": rótulo em g7, pontilhado de 1.5px em g3 que preenche o espaço, contagem g5 13px. O rádio é invisível; a linha inteira é o alvo.
- **Contagens vivas:** cada contagem é calculada com todos os outros filtros aplicados; opção com zero cai para 45% de opacidade.
- **Escolhida:** rótulo, pontilhado e contagem em violeta, 650.
- **Grupos:** título de grupo em maiúsculas 12px g5 (Preço, Época, Capa, Mais filtros).
- **Celular:** o índice inteiro vai para a gaveta, com cabeçalho fixo e o botão "Ver N livros".

### Preço a lápis (signature)
O preço em Kalam, cor do lápis (g7), no canto superior direito da ficha. Bom preço: um círculo SVG à mão livre (um de três traçados, escolhido por hash), traço de 2.1px a 85%, envolve o valor. Preço que caiu: o valor antigo aparece abaixo, em Kalam 700 16px g5, riscado a 2px. "Mais um exemplar" aparece em 11.5px g5 sob o preço.

### Carimbo (signature)
Borda violeta de 2px, cantos de 3px, 800 11px maiúsculas com 0.12em, opacidade 0.92, girado de -1 a -5deg. Só para itens com evento nos últimos 7 dias: "Novo", "Preço caiu", "Mais um exemplar".

### Etiqueta do sebo (signature)
Nome do sebo em maiúsculas 600 11.5px g7, dentro de fio duplo de 3px em g4 sobre papel; corta com reticências numa linha.

### Encadernação de pano (signature)
Sem capa (ou capa que falha ao carregar), entra um pano gerado: cor da lista de panos por hash, trama de dois ruídos fractais cruzados (`feTurbulence` 1.8 x 0.35 e 0.35 x 1.8) em `multiply`, título em serifa 600 9.5px dourado (#e7d6a2) entre dois filetes, até 4 linhas.

### Faixa de guarda (signature)
Índigo com marmorização procedural em SVG (`feTurbulence` fractal + tabela de cores de veios índigo/bordô/pergaminho + `feDisplacementMap` de escala 70 como pente). Leva o rótulo de papel com fio interno e o indicador da rodada (pílula escura translúcida, ponto de 8px lilás quando em dia, âmbar quando o monitor parece parado).

### Movimento assinatura
Só em `prefers-reduced-motion: no-preference` e só em fichas com evento posterior à última rodada vista (a primeira renderização da visita): o carimbo "bate" (0.42s, `cubic-bezier(.2,.9,.25,1)`, de escala 1.9 com desfoque para 0.94 e assenta em 1) e, 0.25s depois, o círculo a lápis se desenha (0.9s, `cubic-bezier(.3,.7,.2,1)`, via `stroke-dashoffset`). Atraso escalonado de 0.07s por ficha, até a 8ª. A gaveta desliza em 0.32s `cubic-bezier(.2,.8,.2,1)` e perde a transição com movimento reduzido. Hovers usam 0.15s.

## Do's and Don'ts

### Do:
- **Do** tirar todo neutro da régua g0 a g8 e redefinir a régua inteira no tema escuro.
- **Do** marcar todo estado vivo (novo, ativo, escolhido, foco, seleção) em violeta de carimbo, e só ele.
- **Do** escrever preços em Kalam na cor do lápis; circular a lápis o bom preço e riscar o preço antigo quando cai.
- **Do** usar a encadernação de pano gerada quando faltar capa, nunca um ícone de imagem quebrada.
- **Do** mostrar contagens vivas ao lado de cada opção de filtro e esmaecer (45%) as que dão zero.
- **Do** manter colunas da grade entre 320 e ~440px com os tetos por container query.
- **Do** restringir a animação de estreia ao que é novo desde a última visita e respeitar `prefers-reduced-motion`.

### Don't:
- **Don't** criar uma segunda cor de estado (verde de oferta, vermelho de desconto, selo de preço de marketplace); a pechincha é o círculo a lápis.
- **Don't** levar a marmorização para fora da faixa do topo.
- **Don't** usar fundo creme ou papel envelhecido: o papel é grafite frio claro.
- **Don't** usar o Kalam para títulos, rótulos ou interface.
- **Don't** inverter o rótulo da faixa no tema escuro; ele é papel claro nos dois temas.
- **Don't** animar fichas já vistas nem repetir o carimbo a cada recarga.
