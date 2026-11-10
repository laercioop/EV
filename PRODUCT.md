# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Um único usuário: o dono do repositório, colecionador e leitor de livros católicos antigos. Ele consulta o
relatório em dois cenários: numa aba do navegador no PC com Windows, aberta enquanto o monitor roda em
`--loop`, e no celular, pela versão publicada no GitHub Pages, quando está fora de casa. A tarefa é bater o
olho no que apareceu, decidir em segundos se vale a pena e abrir o anúncio na Estante Virtual antes que outro
comprador leve o livro.

## Product Purpose
Monitorar os anúncios recém-publicados na Estante Virtual e apresentar, num só lugar, os livros católicos
antigos (até 1958), além de clássicos que um católico leria, sobretudo os de bom preço. O objetivo é chegar
primeiro aos achados raros e baratos.

## Positioning
A Estante Virtual não tem alerta para "católico e anterior a 1958". O monitor junta feeds de categoria e buscas
ordenados por anúncio mais recente, pontua cada item com um vocabulário católico curado (com termos negativos
para descartar o que é espírita, protestante ou pós-conciliar), descobre o ano no título ou na descrição e
guarda o histórico de preço. Por isso o relatório mostra o que é novo **e** relevante, e não só o que é novo.

## Operating Context
- O `monitor/monitor.py` gera o relatório como arquivo estático (`index.html` na raiz), publicado no GitHub Pages.
  Não existe servidor; a interatividade vem toda de JavaScript no cliente, e as preferências ficam em `localStorage`.
- A página se recarrega a cada 5 minutos. O toast do Windows leva ao relatório ou direto ao anúncio.
- Os dados por item são capa (URL da Estante Virtual, às vezes o placeholder "indisponível"), título, autor,
  editora, ano (e a fonte dele: anúncio, título ou descrição, quando não há ano), preço, sebo, frete grátis,
  descrição do sebo (muitas vezes com o estado de conservação), data de cadastro, primeira vez visto, eventos
  (novo, preço caiu, novo exemplar) e os termos que deram a pontuação.

## Capabilities and Constraints
- Comportamentos que o usuário pediu: abas de estado (Novidades, Todos, Bom preço), abas por tema e por época;
  filtros ricos salvos no navegador (busca de texto, faixas de preço até 100, até 200, até 300 e acima de 300,
  com/sem ano, com/sem capa, sebo, frete grátis, ordenação).
- Clássicos que um católico leria entram no escopo (Dante, Chesterton, Manzoni, Bernanos, Papini, Newman…).
- Toda a interface fica em português do Brasil.
- Python 3.9 gera o HTML, sem build e sem dependências de front-end; fontes e scripts externos precisam funcionar offline o bastante (com fallback).

## Evidence on Hand
Dados reais em `dados/monitor.db` (cerca de 90 achados e 3.600 anúncios monitorados em 10/11/2026). As capas são imagens
da própria Estante Virtual. Não há logotipo nem marca.

## Product Principles
1. A velocidade de decisão vem antes de tudo: preço, ano e título se leem num relance.
2. Mostrar a evidência: por que o item entrou (termos) e de onde veio o ano.
3. Se não tiver certeza, mostrar e marcar ("sem ano", "ano pela descrição"), em vez de esconder.
4. Funcionar igualmente bem no celular e no PC.
