"""Monitor de livros católicos antigos na Estante Virtual.

Uso:
    python monitor/monitor.py               # uma rodada
    python monitor/monitor.py --loop 20     # uma rodada a cada 20 minutos
    python monitor/monitor.py --abrir       # abre o relatório ao final

Lê os feeds de anúncios mais recentes (sort=new-releases) e as buscas do config.json,
seleciona livros católicos até `ano_max`, guarda tudo em dados/monitor.db e gera index.html (raiz do repositório).
"""
import argparse
import base64
import html
import json
import re
import sqlite3
import subprocess
import sys
import time
import traceback
import unicodedata
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests

DIR = Path(__file__).resolve().parent
RAIZ = DIR.parent
DB_PATH = RAIZ / "dados" / "monitor.db"
REPORT_PATH = RAIZ / "index.html"
BASE = "https://www.estantevirtual.com.br"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
STATE_KEY = "window.__INITIAL_STATE__="
ANO_RE = re.compile(r"(?<!\d)(1[4-9]\d\d|20[0-3]\d)(?!\d)")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- utilidades

def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def compilar(termos):
    """'catolic*' casa como prefixo; os demais termos, como palavra inteira."""
    out = []
    for t in termos:
        prefixo = t.endswith("*")
        base = norm(t.rstrip("*"))
        out.append((t, re.compile(r"(?<![a-z0-9])" + re.escape(base) + ("" if prefixo else r"(?![a-z0-9])"))))
    return out


def carregar_config():
    cfg = json.loads((DIR / "config.json").read_text(encoding="utf-8"))
    cfg["_termos"] = [(peso, compilar(cfg["termos"].get(nivel, [])))
                      for nivel, peso in (("forte", 3), ("medio", 2), ("fraco", 1))]
    cfg["_negativos"] = compilar(cfg.get("negativos", []))
    return cfg


class Cliente:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
        self.requisicoes = 0

    def estado(self, path):
        for tentativa in range(3):
            try:
                r = self.s.get(BASE + path, timeout=30)
                self.requisicoes += 1
                if r.status_code == 404:
                    return None
                r.raise_for_status()
                h = r.text
                i = h.index(STATE_KEY) + len(STATE_KEY)
                return json.JSONDecoder().raw_decode(h[i:])[0]
            except Exception:
                if tentativa == 2:
                    raise


# ---------------------------------------------------------------- banco

SCHEMA = """
CREATE TABLE IF NOT EXISTS itens (
    code TEXT PRIMARY KEY, nome TEXT, autor TEXT, editora TEXT, ano INTEGER, ano_fonte TEXT,
    idioma TEXT, preco REAL, exemplares INTEGER, url TEXT, imagem TEXT, feeds TEXT,
    pontos INTEGER, motivos TEXT, candidato INTEGER DEFAULT 0, vendedor TEXT, descricao TEXT,
    frete_gratis INTEGER, data_cadastro TEXT, primeira_vez TEXT, ultima_vez TEXT
);
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT, quando TEXT, tipo TEXT,
    preco REAL, detalhe TEXT, notificado INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_eventos_quando ON eventos(quando);
"""


def abrir_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db


# ---------------------------------------------------------------- coleta

def parse_item(p):
    a = {x.get("name"): x.get("value") for x in p.get("attributes", [])}
    ano = a.get("year") or ""
    return {
        "code": p["code"],
        "nome": p.get("name") or "",
        "autor": a.get("author") or "",
        "editora": a.get("publisher") or "",
        "ano": int(ano) if ano.isdigit() else None,
        "ano_fonte": "anúncio" if ano.isdigit() else None,
        "idioma": a.get("language") or "",
        "preco": (p.get("salePrice") or 0) / 100,
        "exemplares": sum(v.get("total", 0) for v in p.get("variations") or []) or 1,
        "usado": any(v.get("condition") == "usado" for v in p.get("variations") or [])
                 or a.get("condition") == "usado",
        "url": BASE + p.get("productSlug", ""),
        "imagem": p.get("image") or "",
    }


def ler_feed(cli, nome, path, bonus, conhecidos, primeira, cfg):
    """Pagina o feed até achar exemplares únicos (grp-) já vistos em rodadas anteriores."""
    itens, sep = [], "&" if "?" in path else "?"
    limite = cfg["paginas_primeira_execucao"] if primeira else cfg["max_paginas"]
    for pagina in range(1, limite + 1):
        st = cli.estado(path if pagina == 1 else f"{path}{sep}page={pagina}")
        sp = (st or {}).get("SearchPage") or {}
        skus = sp.get("parentSkus") or []
        for p in skus:
            it = parse_item(p)
            it["_feed"], it["_bonus"] = nome, bonus
            itens.append(it)
        grp = [p["code"] for p in skus if p["code"].startswith("grp-")]
        if not skus or pagina >= (sp.get("totalPages") or 1):
            break
        if grp and grp[-1] in conhecidos:
            break
    return itens


def coletar(cli, cfg, conhecidos, primeira):
    tarefas = [(f["nome"], f["path"], f.get("bonus", 0)) for f in cfg["feeds"]]
    tarefas += [(f"busca: {q}", f"/busca?q={quote(q)}&sort=new-releases", 0) for q in cfg["buscas"]]
    erros = []

    def run(t):
        try:
            return ler_feed(cli, *t, conhecidos, primeira, cfg)
        except Exception as e:
            erros.append(f"{t[0]}: {e}")
            return []

    with ThreadPoolExecutor(cfg.get("threads", 8)) as ex:
        resultados = list(ex.map(run, tarefas))
    juntos = {}
    for lista in resultados:
        for it in lista:
            atual = juntos.get(it["code"])
            if atual is None:
                it["_feeds"] = {it["_feed"]}
                juntos[it["code"]] = it
            else:
                atual["_feeds"].add(it["_feed"])
                atual["_bonus"] = max(atual["_bonus"], it["_bonus"])
    return juntos, erros


# ---------------------------------------------------------------- classificação

def pontuar(it, cfg):
    texto = norm(" ".join([it["nome"], it["autor"], it["editora"]]))
    neg = [t for t, rx in cfg["_negativos"] if rx.search(texto)]
    if neg:
        return None, ["negativo: " + ", ".join(neg)]
    pts, motivos = 0, []
    for peso, termos in cfg["_termos"]:
        for t, rx in termos:
            if rx.search(texto):
                pts += peso
                motivos.append(t.rstrip("*"))
    if it.get("_bonus") and pts:
        pts += it["_bonus"]
        motivos.append("categoria")
    return pts, motivos


def ano_no_titulo(it):
    anos = [int(a) for a in ANO_RE.findall(it["nome"])]
    return min(anos) if anos else None


def preselecionar(it, cfg):
    """Primeiro filtro, só com os dados da listagem. Devolve True se vale enriquecer."""
    if not it["usado"]:
        return False
    if it["ano"] is None:
        a = ano_no_titulo(it)
        if a:
            it["ano"], it["ano_fonte"] = a, "título"
    if it["ano"] is not None and it["ano"] > cfg["ano_max"]:
        return False
    if cfg.get("preco_max") and it["preco"] > cfg["preco_max"]:
        return False
    pts, motivos = pontuar(it, cfg)
    it["pontos"], it["motivos"] = pts, motivos
    if pts is None:
        return False
    minimo = cfg["pontuacao_minima"] if it["ano"] is not None else cfg["pontuacao_minima_sem_ano"]
    return pts >= minimo


def enriquecer(cli, it, cfg):
    """Lê a página do produto: ano, vendedor, descrição, data de cadastro."""
    st = cli.estado(it["url"][len(BASE):])
    P = (st or {}).get("Product") or {}
    cur = P.get("currentProduct") or {}
    preco = cur.get("price") or {}
    it["vendedor"] = ((preco.get("seller") or {}).get("name")) or ""
    it["frete_gratis"] = int(bool(preco.get("freeShipping")))
    it["data_cadastro"] = (P.get("dateCreated") or "")[:19].replace("T", " ")
    it["descricao"] = (cur.get("description") or "")[:1500]
    if it["ano"] is None:
        fa = (P.get("formattedAttributes") or {}).get("year") or ""
        if fa.isdigit():
            it["ano"], it["ano_fonte"] = int(fa), "anúncio"
        else:
            anos = [int(a) for a in ANO_RE.findall(it["descricao"])]
            if anos:
                it["ano"], it["ano_fonte"] = min(anos), "descrição"
    if it["ano"] is not None and it["ano"] > cfg["ano_max"]:
        return False
    pts, motivos = pontuar(it, cfg)
    it["pontos"], it["motivos"] = pts, motivos
    if pts is None:
        return False
    minimo = cfg["pontuacao_minima"] if it["ano"] is not None else cfg["pontuacao_minima_sem_ano"]
    return pts >= minimo


# ---------------------------------------------------------------- rodada

def rodada(cfg, abrir=False):
    t0 = time.time()
    db = abrir_db()
    conhecidos = {r[0] for r in db.execute("SELECT code FROM itens")}
    primeira = not conhecidos
    cli = Cliente()
    itens, erros = coletar(cli, cfg, conhecidos, primeira)
    quando = agora()

    antigos = {r["code"]: r for r in db.execute("SELECT * FROM itens WHERE code IN (%s)" % ",".join("?" * len(itens)), list(itens))} if itens else {}

    # O que precisa de enriquecimento: itens novos que passam no pré-filtro,
    # e candidatos já conhecidos que ganharam exemplar ou baixaram de preço.
    para_enriquecer, eventos = [], []
    for code, it in itens.items():
        old = antigos.get(code)
        if old is None:
            if preselecionar(it, cfg):
                para_enriquecer.append(it)
        elif old["candidato"]:
            if it["preco"] < (old["preco"] or 0) - 0.005:
                eventos.append((code, "preço caiu", it["preco"], f"de R$ {old['preco']:.2f}"))
            if it["exemplares"] > (old["exemplares"] or 0):
                eventos.append((code, "novo exemplar", it["preco"], f"{old['exemplares']} → {it['exemplares']} exemplares"))

    def enr(it):
        try:
            it["_cand"] = enriquecer(cli, it, cfg)
        except Exception as e:
            it["_cand"] = True  # na dúvida, mostra
            erros.append(f"produto {it['code']}: {e}")
        return it

    with ThreadPoolExecutor(cfg.get("threads", 8)) as ex:
        list(ex.map(enr, para_enriquecer))

    novos_cand = [it for it in para_enriquecer if it.get("_cand")]
    for it in novos_cand:
        eventos.append((it["code"], "inicial" if primeira else "novo", it["preco"], ""))

    # Grava: todos os itens vistos (para saber até onde paginar na próxima rodada).
    for code, it in itens.items():
        old = antigos.get(code)
        if old is None:
            cand = int(bool(it.get("_cand")))
            db.execute(
                """INSERT INTO itens (code,nome,autor,editora,ano,ano_fonte,idioma,preco,exemplares,url,imagem,
                   feeds,pontos,motivos,candidato,vendedor,descricao,frete_gratis,data_cadastro,primeira_vez,ultima_vez)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (code, it["nome"], it["autor"], it["editora"], it["ano"], it.get("ano_fonte"), it["idioma"],
                 it["preco"], it["exemplares"], it["url"], it["imagem"], ", ".join(sorted(it["_feeds"])),
                 it.get("pontos"), ", ".join(it.get("motivos") or []), cand, it.get("vendedor"),
                 it.get("descricao"), it.get("frete_gratis"), it.get("data_cadastro"), quando, quando))
        else:
            db.execute("UPDATE itens SET preco=?, exemplares=?, ultima_vez=? WHERE code=?",
                       (it["preco"], it["exemplares"], quando, code))
    for code, tipo, preco, det in eventos:
        db.execute("INSERT INTO eventos (code,quando,tipo,preco,detalhe,notificado) VALUES (?,?,?,?,?,?)",
                   (code, quando, tipo, preco, det, int(primeira)))
    db.commit()

    gerar_relatorio(db, cfg)
    novos_alertas = [e for e in eventos if e[1] != "inicial"]
    dur = time.time() - t0
    print(f"[{quando}] {len(itens)} itens lidos, {len(para_enriquecer)} pré-selecionados, "
          f"{len(eventos)} eventos ({len(novos_alertas)} novos), {cli.requisicoes} requisições, {dur:.0f}s"
          + (" — primeira execução (linha de base)" if primeira else ""))
    for code, tipo, preco, det in eventos[:30]:
        r = db.execute("SELECT nome, ano, autor FROM itens WHERE code=?", (code,)).fetchone()
        print(f"   [{tipo}] R$ {preco:8.2f}  {r['ano'] or 's/ano':>5}  {r['nome'][:70]} — {r['autor'][:30]}")
    for e in erros[:10]:
        print("   ERRO", e)

    if novos_alertas and cfg.get("notificar_windows"):
        notificar(db, novos_alertas, cfg)
    db.close()
    if abrir:
        webbrowser.open(REPORT_PATH.as_uri())


# ---------------------------------------------------------------- notificação

def notificar(db, eventos, cfg):
    linhas = []
    for code, tipo, preco, _ in eventos[:3]:
        r = db.execute("SELECT nome, ano FROM itens WHERE code=?", (code,)).fetchone()
        bom = " ★" if preco <= cfg["preco_bom"] else ""
        linhas.append(f"R$ {preco:.0f}{bom} · {r['ano'] or 's/ano'} · {r['nome'][:60]}")
    titulo = f"Estante Virtual: {len(eventos)} achado(s)"
    if len(eventos) == 1:
        launch = db.execute("SELECT url FROM itens WHERE code=?", (eventos[0][0],)).fetchone()["url"]
    else:
        launch = REPORT_PATH.as_uri()
    esc = lambda s: html.escape(s, quote=True)
    xml = (f'<toast activationType="protocol" launch="{esc(launch)}"><visual><binding template="ToastGeneric">'
           f"<text>{esc(titulo)}</text>" + "".join(f"<text>{esc(l)}</text>" for l in linhas[:2])
           + "</binding></visual></toast>")
    ps = (
        "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null;"
        "[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] > $null;"
        "$x = New-Object Windows.Data.Xml.Dom.XmlDocument;"
        f"$x.LoadXml('{xml.replace(chr(39), chr(39) * 2)}');"
        "$app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe';"
        "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show("
        "[Windows.UI.Notifications.ToastNotification]::new($x))"
    )
    try:
        subprocess.run(["powershell.exe", "-NoProfile", "-EncodedCommand",
                        base64.b64encode(ps.encode("utf-16-le")).decode()],
                       capture_output=True, timeout=30)
    except Exception as e:
        print("   (notificação falhou:", e, ")")


# ---------------------------------------------------------------- relatório

def gerar_relatorio(db, cfg):
    rows = db.execute("""
        SELECT e.quando, e.tipo, e.preco AS preco_evento, e.detalhe, i.*
        FROM eventos e JOIN itens i ON i.code = e.code
        ORDER BY e.id DESC LIMIT 600""").fetchall()
    ultima = rows[0]["quando"] if rows else ""
    cards = []
    for r in rows:
        bom = r["preco_evento"] <= cfg["preco_bom"]
        ano = r["ano"]
        badges = []
        if r["tipo"] != "inicial":
            badges.append(f'<span class="b b-{"novo" if r["tipo"] == "novo" else "mud"}">{html.escape(r["tipo"])}</span>')
        if r["quando"] == ultima and r["tipo"] != "inicial":
            badges.append('<span class="b b-agora">esta rodada</span>')
        if bom:
            badges.append('<span class="b b-bom">bom preço</span>')
        if ano is None:
            badges.append('<span class="b b-semano">sem ano</span>')
        elif r["ano_fonte"] and r["ano_fonte"] != "anúncio":
            badges.append(f'<span class="b b-semano">ano pela {html.escape(r["ano_fonte"])}</span>')
        meta = " · ".join(html.escape(x) for x in [r["autor"], r["editora"]] if x)
        desc = html.escape((r["descricao"] or "")[:400])
        cards.append(f"""
<article class="card" data-bom="{int(bom)}" data-ano="{0 if ano is None else 1}" data-texto="{html.escape(norm(' '.join([r['nome'] or '', r['autor'] or '', r['editora'] or '', r['vendedor'] or ''])))}">
  <a class="thumb" href="{html.escape(r['url'])}" target="_blank" rel="noopener"><img loading="lazy" src="{html.escape(r['imagem'] or '')}" alt=""></a>
  <div class="body">
    <div class="top"><span class="ano">{ano if ano is not None else "s/ano"}</span>{''.join(badges)}</div>
    <h2><a href="{html.escape(r['url'])}" target="_blank" rel="noopener">{html.escape(r['nome'] or '')}</a></h2>
    <p class="meta">{meta}</p>
    {f'<p class="desc">{desc}</p>' if desc else ''}
    <p class="foot">{html.escape(r['vendedor'] or '')}{' · frete grátis' if r['frete_gratis'] else ''} · cadastrado {html.escape(r['data_cadastro'] or '?')} · visto {html.escape(r['quando'])}{(' · ' + html.escape(r['detalhe'])) if r['detalhe'] else ''}</p>
    <p class="why">{html.escape(r['motivos'] or '')}</p>
  </div>
  <div class="preco{' bom' if bom else ''}">R$&nbsp;{r['preco_evento']:.2f}</div>
</article>""")
    total = db.execute("SELECT COUNT(*) FROM itens").fetchone()[0]
    pagina = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="300">
<title>Achados católicos</title>
<style>
:root {{ --bg:#f6f3ee; --card:#fff; --ink:#1f1b16; --mute:#6b6257; --line:#e4ddd2; --acc:#7a1f2b; --ok:#1d6b3a; --okbg:#e3f2e8; --warn:#8a5a00; --warnbg:#fbf0d9; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#16130f; --card:#211d18; --ink:#efe9e0; --mute:#a89e91; --line:#3a332b; --acc:#e08a95; --ok:#7fd49c; --okbg:#1f3a28; --warn:#f0c46a; --warnbg:#3a2f17; }} }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.45 Georgia, "Times New Roman", serif; }}
header {{ position:sticky; top:0; background:var(--bg); border-bottom:1px solid var(--line); padding:14px 16px; z-index:1 }}
header h1 {{ margin:0 0 4px; font-size:20px; color:var(--acc) }}
header p {{ margin:0; color:var(--mute); font:13px system-ui, sans-serif }}
.ctl {{ display:flex; flex-wrap:wrap; gap:12px; margin-top:10px; font:14px system-ui, sans-serif; align-items:center }}
.ctl input[type=search] {{ flex:1; min-width:180px; padding:7px 10px; border:1px solid var(--line); border-radius:6px; background:var(--card); color:var(--ink) }}
main {{ max-width:980px; margin:0 auto; padding:12px 16px 40px }}
.card {{ display:grid; grid-template-columns:72px 1fr auto; gap:14px; background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px; margin-bottom:10px }}
.thumb img {{ width:72px; height:96px; object-fit:cover; border-radius:4px; background:var(--line) }}
.body {{ min-width:0 }}
h2 {{ font-size:16px; margin:2px 0 2px }} h2 a {{ color:var(--ink); text-decoration:none }} h2 a:hover {{ text-decoration:underline }}
.top {{ display:flex; flex-wrap:wrap; gap:6px; align-items:center; font:12px system-ui, sans-serif }}
.ano {{ font-weight:700; color:var(--acc); font-size:14px; margin-right:4px }}
.b {{ padding:1px 7px; border-radius:10px; background:var(--line); color:var(--mute) }}
.b-novo, .b-agora {{ background:var(--acc); color:#fff }} .b-mud {{ background:var(--warnbg); color:var(--warn) }}
.b-bom {{ background:var(--okbg); color:var(--ok) }} .b-semano {{ background:var(--warnbg); color:var(--warn) }}
.meta {{ margin:0; color:var(--mute) }}
.desc {{ margin:6px 0 0; font-size:13px; color:var(--mute); display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden }}
.foot, .why {{ margin:6px 0 0; font:12px system-ui, sans-serif; color:var(--mute) }} .why {{ opacity:.7 }}
.preco {{ font:700 17px system-ui, sans-serif; white-space:nowrap }} .preco.bom {{ color:var(--ok) }}
@media (max-width:600px) {{ .card {{ grid-template-columns:56px 1fr }} .thumb img {{ width:56px; height:76px }} .preco {{ grid-column:2 }} }}
</style></head><body>
<header><h1>Achados católicos · até {cfg['ano_max']}</h1>
<p>{len(rows)} achados · {total} anúncios monitorados · atualizado {html.escape(agora())} · bom preço ≤ R$ {cfg['preco_bom']:.0f}</p>
<div class="ctl"><input type="search" id="q" placeholder="Filtrar por título, autor, editora, sebo…">
<label><input type="checkbox" id="fb"> só bom preço</label><label><input type="checkbox" id="fa"> só com ano</label></div></header>
<main id="lista">{''.join(cards) or '<p>Nenhum achado ainda.</p>'}</main>
<script>
const q=document.getElementById('q'),fb=document.getElementById('fb'),fa=document.getElementById('fa');
const n=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
function f(){{const t=n(q.value);document.querySelectorAll('.card').forEach(c=>{{
 c.style.display=(!t||c.dataset.texto.includes(t))&&(!fb.checked||c.dataset.bom==='1')&&(!fa.checked||c.dataset.ano==='1')?'':'none';}});
 try{{localStorage.setItem('ev-f',JSON.stringify([q.value,fb.checked,fa.checked]))}}catch(e){{}}}}
try{{const s=JSON.parse(localStorage.getItem('ev-f')||'null');if(s){{[q.value,fb.checked,fa.checked]=s}}}}catch(e){{}}
[q,fb,fa].forEach(e=>e.addEventListener('input',f));f();
</script></body></html>"""
    REPORT_PATH.write_text(pagina, encoding="utf-8")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--loop", type=float, metavar="MIN", help="repetir a cada MIN minutos")
    ap.add_argument("--abrir", action="store_true", help="abrir o relatório ao final da primeira rodada")
    args = ap.parse_args()
    abrir = args.abrir
    while True:
        try:
            rodada(carregar_config(), abrir)
        except Exception:
            traceback.print_exc()
        abrir = False
        if not args.loop:
            break
        time.sleep(args.loop * 60)


if __name__ == "__main__":
    main()
