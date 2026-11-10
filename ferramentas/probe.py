import json, sys, time, requests
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
S = requests.Session(); S.headers["User-Agent"] = UA
BASE = "https://www.estantevirtual.com.br"

def state(path):
    r = S.get(BASE + path, timeout=30)
    h = r.text
    i = h.index("window.__INITIAL_STATE__=") + len("window.__INITIAL_STATE__=")
    return r, json.JSONDecoder().raw_decode(h[i:])[0]

def attrs(p):
    return {a["name"]: a["value"] for a in p.get("attributes", [])}

if __name__ == "__main__":
    for path in sys.argv[1:]:
        r, st = state(path)
        s = st.get("SearchPage", {})
        print(f"\n== {path} -> {r.status_code} {r.url}")
        print("total", s.get("total"), "pages", s.get("totalPages"), "relaxed", s.get("relaxed"),
              "selected", json.dumps(s.get("selectedFilters"), ensure_ascii=False)[:200])
        for p in s.get("parentSkus", [])[:6]:
            a = attrs(p)
            print(f"  R${p['salePrice']/100:>8.2f} {a.get('year','?'):>5} {p['name'][:60]} | {a.get('author','')[:25]} | {p['variations']}")
        pass
