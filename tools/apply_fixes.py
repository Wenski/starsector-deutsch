"""Uebernimmt Korrekturen {datei: {schluessel: text}} nach Pruefung in translations/.
  python -I tools/apply_fixes.py work/<datei>.json"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ssde
fx = json.load(open(sys.argv[1], encoding="utf-8"))
ok = bad = 0
for f, d in fx.items():
    p = os.path.join(ssde.TRN, f)
    src = json.load(open(os.path.join(ssde.SRC, f), encoding="utf-8"))
    t = json.load(open(p, encoding="utf-8"))
    for k, v in d.items():
        v = ssde.norm(v)
        if "\r\n" in src.get(k, ""):
            v = re.sub(r"(?<!\r)\n", "\r\n", v)
        e = ssde.check_unit(k, src[k], v) if k in src else ["unbekannter Schluessel"]
        if e:
            print("!!", f, k, e); bad += 1; continue
        t[k] = v; ok += 1
    ssde.jdump(t, p)
print(f"{ok} uebernommen, {bad} abgelehnt")
