# AGENTS.md

Este arquivo orienta agentes de código (Claude Code, Codex, Gemini CLI etc.) que trabalham neste repositório.

## Objetivo
Monitorar a Estante Virtual (estantevirtual.com.br) para encontrar, assim que são anunciados,
**livros católicos antigos (até 1958)**, sobretudo a preços bons. Tudo é feito por HTTP com
`requests`, sem navegador. O navegador só entra se o acesso por código realmente falhar.

## Comandos
```
python monitor/monitor.py               # uma rodada (lê os feeds, filtra, grava dados/monitor.db, gera index.html)
python monitor/monitor.py --loop 10     # repete a cada 10 min
python monitor/monitor.py --abrir       # abre index.html ao final
rm dados/monitor.db                     # reinicia a linha de base (a próxima rodada não notifica)
python ferramentas/probe.py "/religiao?sort=new-releases"   # inspeciona rapidamente qualquer URL de listagem
```
Ambiente: Windows 10 e Python 3.9 (não use `match`, `X | None` nem outra sintaxe de 3.10+). Não há testes nem lint.
Para validar uma mudança, rode `python monitor/monitor.py` e confira a linha de resumo e os eventos impressos.

## Decisões do usuário (respeite)
- O `robots.txt` do site bloqueia `Claude-User`/`ClaudeBot`. **O usuário decidiu explicitamente prosseguir mesmo assim.**
- **Sem pausas entre requisições** (pedido explícito). O intervalo do `--loop` é só a cadência entre rodadas.
- Toda a comunicação, a documentação e os textos do relatório ficam em português.

## Estrutura de pastas
```
index.html        relatório gerado (único arquivo na raiz; publicado pelo GitHub Pages)
monitor/          monitor.py e config.json
ferramentas/      probe.py e probe2.py (exploração do site)
docs/             NOTAS-ESTRUTURA.md
dados/            monitor.db (fora do git)
exploracao/       paginas/ e raw/, cópias salvas do site (fora do git)
```
O `AGENTS.md` fica na raiz porque o hook de SessionStart só o lê de lá.
Versionamento: git, remoto `https://github.com/laercioop/EV`, branch `main`, commits como `laercioop`.

## Arquitetura (`monitor/monitor.py`)
Fluxo de uma rodada (`rodada()`):
1. **Coleta** (`coletar` → `ler_feed`): em paralelo, lê os `feeds` (categorias com `sort=new-releases`) e as
   `buscas` do `config.json` (`/busca?q=…&sort=new-releases`). Cada feed vai paginando até encontrar, no fim
   da página, um exemplar `grp-` já presente no banco, com limite em `max_paginas`. Na primeira execução,
   lê `paginas_primeira_execucao`. Os itens são deduplicados por `code`, juntando os feeds de origem e o maior `bonus`.
2. **Pré-filtro** (`preselecionar`, só com dados da listagem): exige exemplar usado; descarta ano > `ano_max`
   (o ano pode vir do título); descarta por `negativos`; pontua com `pontuar`.
3. **Enriquecimento** (`enriquecer`, página do produto, em paralelo): sebo, descrição, `dateCreated`; se faltar
   ano, usa `formattedAttributes.year` ou o menor ano encontrado na descrição. Depois reaplica filtro e pontuação.
4. **Persistência**: **todos** os itens lidos vão para `itens`, o que é necessário para o critério de parada da
   paginação. Os candidatos geram linhas em `eventos` (`novo`, `preço caiu`, `novo exemplar`; `inicial` na linha de base).
5. **Saída**: `gerar_relatorio` reescreve `index.html` na raiz (HTML estático com filtros em JS e refresh a cada 5 min);
   `notificar` mostra um toast do Windows via `powershell.exe` 5.1 (WinRT, `-EncodedCommand`). Não use `pwsh`,
   que não carrega os tipos WinRT.

Pontuação: os termos em `config.json["termos"]` valem forte = 3, médio = 2 e fraco = 1. Eles são comparados com
`nome + autor + editora` normalizados (minúsculas, sem acento, pontuação virando espaço). O termo casa como palavra
inteira, ou como prefixo se terminar em `*`. O `bonus` do feed só soma se algum termo já tiver pontuado.
O ano **não** dá pontos, só filtra. O limiar é `pontuacao_minima` com ano conhecido e `pontuacao_minima_sem_ano` sem ano.

**Atenção:** o campo `candidato` é calculado só na primeira vez que o item é visto. Depois de mudar termos,
pesos ou filtros, apague `dados/monitor.db` para reclassificar (é rápido: cerca de 200 requisições e 10 s).

## Fatos do site que sustentam o código
Os detalhes estão em `docs/NOTAS-ESTRUTURA.md`. O essencial:
- Cada página de listagem ou produto traz o estado em JSON após `window.__INITIAL_STATE__=`
  (extraído com `json.JSONDecoder().raw_decode`). A listagem fica em `SearchPage.parentSkus`; o produto, em `Product`.
- `sort=new-releases` ordena pelos anúncios mais recentes (não funciona com `q=` vazio). Há 44 itens por página
  (`page=N`). `ano-de-publicacao=` aceita **um** ano só (repetir o parâmetro dá 404). `_preco=MIN-MAX` é em centavos.
- `grp-…` é um exemplar único (código sequencial); `…-BK` é uma obra agrupada por ISBN. Nela, `salePrice` é o menor
  preço, e a obra sobe no feed quando entra um exemplar novo (isso é detectado pela variação em `variations`/`salePrice`).
- O ano costuma vir vazio em livros antigos; por isso os itens sem ano são mantidos e marcados como "sem ano".

## Outros arquivos
- `ferramentas/probe.py` / `probe2.py`: helpers de exploração (`state(path)`, `tryp(path)`), usados para mapear o site.
- `exploracao/paginas/`: cópias salvas (`.html` e o `.json` extraído) das páginas exploradas em 10/11/2026, mais os bundles JS
  do site (`main.js` e `wildcard.js` contêm a lógica de ordenação e filtros). `exploracao/raw/` guarda as primeiras capturas.
