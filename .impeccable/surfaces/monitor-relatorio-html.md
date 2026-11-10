---
version: 1
slug: "monitor-relatorio-html"
primary_target: "monitor/relatorio.html"
related_targets: ["index.html"]
---

## Escopo
Relatório `index.html`, gerado a partir do modelo `monitor/relatorio.html`. Modo: Operate. O usuário, um colecionador, examina os achados no PC (aba aberta enquanto o --loop roda) e no celular (GitHub Pages), decide em segundos e abre o anúncio.

## Tarefa e conteúdo
Abas: Novidades, Todos, Bom preço; temas (Clássicos, Missais e liturgia, Devoção, Santos, Teologia e doutrina, Bíblia, Pensadores brasileiros, Ordens e Igreja, Latim, Outros); épocas (até 1900, 1901–1930, 1931–1958, sem ano). Filtros salvos no navegador: texto, faixa de preço (até 100, até 200, até 300, acima de 300), ano (com/sem), capa (com/sem), frete grátis, sebo e ordenação.

## Direction contract
THESIS: cada achado se lê como a guarda de um livro de sebo. O preço vai a lápis no canto, circulado quando é pechincha e riscado e reescrito quando cai. Isso substitui a grade de marketplace com selo de preço e o relatório creme com serifa.
OWN-WORLD: faixa de papel de guarda marmorizado índigo (marmorização procedural em SVG, só no topo) sobre um fundo claro frio; neutros de uma régua única de grafite com 9 tons; a tinta violeta de carimbo marca todo estado vivo (novo, preço caiu, aba ativa, foco); o sebo aparece como etiqueta de livreiro com fio duplo; quando falta capa, entra uma encadernação de pano gerada.
STORY: o usuário vê quantas novidades há, lê o ano e o preço a lápis num relance, filtra por faixa de preço, ano, capa e tema e abre o anúncio.
FIRST VIEWPORT: faixa marmorizada de cerca de 120px com o título, as contagens e a última rodada; abas sobre a faixa, com contagens; à esquerda, um trilho de filtros de 264px; grade de fichas em 3 colunas a 1440px: capa de 76px, ano grande, título serifado, autor e editora, preço a lápis no canto superior direito, carimbo violeta e etiqueta do sebo. No celular, as abas rolam na horizontal e os filtros ficam numa gaveta.
FORM: Guarda de sebo, posição 7 da lista; encenação: grade de fichas com trilho de filtros. seed:7241d9aff1640cce
Interação assinatura: na primeira visita após a chegada de um item, o carimbo violeta "bate" uma vez e o círculo a lápis do bom preço se desenha.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Pendências
Nenhuma.
