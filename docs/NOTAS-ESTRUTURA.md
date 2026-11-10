# Estante Virtual: estrutura do site (mapeada em 2026-11-10)

## Como os dados chegam
- As páginas de busca, categoria e produto são renderizadas no servidor, com todo o estado em JSON
  dentro de `window.__INITIAL_STATE__=` no HTML. Basta `requests` mais `json.JSONDecoder().raw_decode`.
  Não precisa de navegador. O motor de busca é o SmartHint (`searchEngine: "SH"`).
- `robots.txt` bloqueia `Claude-User`/`ClaudeBot`. O usuário decidiu prosseguir mesmo assim, sem pausas entre requisições.

## URLs de listagem
| O quê | URL |
|---|---|
| Busca | `/busca?q=missal` |
| Categoria | `/religiao`, `/livros-raros`, `/filosofia`, `/historia-geral`… |
| Ordenação | `sort=` `relevance` (padrão), `lowest-first`, `highest-first`, `new-releases`, `best-sellers` |
| Página | `page=N` (44 itens por página) |
| Ano | `ano-de-publicacao=1950` (apenas **um** ano; repetir o parâmetro dá 404; vírgula e faixa dão 0 resultados) |
| Preço | `_preco=MIN-MAX` em centavos, ex.: `_preco=0-5000` = até R$ 50 |
| Outros | `tipo-de-livro=usado`, `idioma=…`, `categoria=…` |

**`sort=new-releases` = anúncios mais recentes** (validado pelo `dateCreated` da página do produto:
os primeiros itens tinham sido cadastrados minutos antes). Não funciona com `q=` vazio.

## Ritmo observado (10/11, madrugada e manhã)
- `/religiao?sort=new-releases`: cerca de 440 itens (10 páginas) cobriram 00:14 → 09:25.
  Há cargas em lote de sebos (ex.: 3 páginas ~04:07).
- Religião tem cerca de 732 mil itens; `/livros-raros` tem cerca de 73 mil.
- `/religiao?ano-de-publicacao=1948` tem 534 itens.

## Item da listagem (`SearchPage.parentSkus[]`)
- `code`: `grp-XXX-0000-000` = exemplar único (código sequencial); `XXX-0000-000-BK` = obra agrupada
  (com ISBN), com vários exemplares.
- `name`, `salePrice` (centavos; em obra agrupada é o **menor** preço), `productSlug` (`/livro/...`),
  `image`, `variations` (`[{condition: usado, total: 36}]`).
- `attributes[]`: `author`, `publisher`, `year` (muitas vezes vazio em livros antigos), `language`,
  `condition`, `isbn`.
- Obra agrupada (`-BK`) sobe para o topo de `new-releases` quando entra um exemplar novo, mas o
  `dateCreated` dela é o da criação do grupo. Detecte a novidade pela mudança em `variations` ou `salePrice`.

## Página de produto (`/livro/<slug>`) → `Product`
- `dateCreated`, `department.name`, `formattedAttributes` {publisher, year, language}, `author`.
- `currentProduct.price`: `saleInCents`, `seller` {id, name}, `freeShipping`.
- `currentProduct.description`: descrição do sebo, com estado de conservação e nº de páginas.

## Facetas (`SearchPage.normalizedAggregates`)
`tipo-de-livro`, `autor`, `editora`, `ano-de-publicacao`, `cidade`, `sebos-e-livreiros`, `_preco`,
`promocoes`, `categoria`, `idioma`, `_avaliacao`.

## Páginas salvas
`paginas/` guarda cada URL explorada como `.html` (bruto) e `.json` (o `__INITIAL_STATE__` extraído),
mais `robots.txt`, `main.js` e `wildcard.js`. São 21 páginas de 10/11/2026: 14 de listagem e 7 de produto.

## Monitor (`monitor.py`)
- `python monitor.py` faz uma rodada; `python monitor.py --loop 10` repete a cada 10 min; `--abrir` abre o relatório.
- Lê os feeds `new-releases` de Religião, Livros raros, Filosofia e História geral, mais as buscas do `config.json`.
  Pagina até encontrar exemplares `grp-` já vistos (no máximo `max_paginas`).
- Filtro: só usados; ano ≤ `ano_max` ou sem ano; nenhum termo negativo; pontuação dos termos
  (forte 3 / médio 2 / fraco 1, mais o bônus da categoria Religião) ≥ `pontuacao_minima`
  (sem ano: ≥ `pontuacao_minima_sem_ano`). O pré-selecionado é enriquecido com a página do produto
  (ano, sebo, descrição, data de cadastro); o ano pode vir do título ou da descrição.
- Guarda tudo em `dados/monitor.db` (tabelas `itens` e `eventos`) e gera `index.html`. Notifica pelo Windows
  quando há item novo, preço que caiu ou exemplar novo de uma obra agrupada.
- A primeira execução (banco vazio) só cria a linha de base, sem notificar. Apagar `dados/monitor.db` reinicia tudo.
