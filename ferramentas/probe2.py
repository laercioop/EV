import sys; sys.path.insert(0,'.')
from probe import *
def tryp(path):
    r=S.get(BASE+path,timeout=30); h=r.text
    try:
        i=h.index("window.__INITIAL_STATE__=")+len("window.__INITIAL_STATE__=")
        s=json.JSONDecoder().raw_decode(h[i:])[0].get("SearchPage") or {}
    except ValueError: s={}
    ps=s.get("parentSkus",[])
    print(r.status_code, path, "| total", s.get("total"), "| precos", [x['salePrice'] for x in ps][:6], "| anos", sorted({attrs(p).get('year') or '?' for p in ps})[:6])
    pass
    return s
