"""Prueft ein fertiges Paket in work/done, OHNE etwas zu uebernehmen oder zu loeschen.

  python -I tools/pruefe_paket.py work/done/<name>.json
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ssde

path = sys.argv[1]
fn = os.path.basename(path)
rel = {ssde.side(r)[:-5]: r for r in ssde.all_files()}[fn.split("--")[0]]
src = ssde.jload(os.path.join(ssde.SRC, ssde.side(rel)))
todo = ssde.jload(os.path.join(ssde.TODO, fn), {})
try:
    done = json.load(open(path, encoding="utf-8"))
except Exception as e:
    print(f"FEHLER: ungueltiges JSON: {e}")
    sys.exit(1)

errors, longs = 0, 0
for k in todo:
    if k not in done:
        print(f"FEHLT: {k}")
        errors += 1
for k, de in done.items():
    if k not in src:
        print(f"UNBEKANNTER SCHLUESSEL: {k}")
        errors += 1
        continue
    de = ssde.norm(de)
    for e in ssde.check_unit(k, src[k], de):
        print(f"FEHLER {k}: {e}")
        errors += 1
    if ssde.too_long(src[k], de):
        print(f"ZU LANG {k}: {len(de)} statt {len(src[k])} Zeichen")
        longs += 1

# Hervorhebungen: Script-Strings, die im englischen #text vorkommen, muessen im deutschen #text vorkommen
for k, de in done.items():
    if "#script#" in k:
        rid = k.split("#")[0]
        en_text, de_text = src.get(f"{rid}#text"), done.get(f"{rid}#text")
        if en_text and de_text and src[k] in en_text and de not in de_text:
            print(f"HERVORHEBUNG {k}: '{de}' kommt im deutschen Text nicht vor")
            errors += 1

ratio = sum(len(v) for v in done.values()) / max(1, sum(len(src[k]) for k in done if k in src))
print(f"--- {len(done)} Eintraege, {errors} Fehler, {longs} zu lang, Laengenverhaeltnis gesamt {ratio:.2f}")
