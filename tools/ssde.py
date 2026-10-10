"""Starsector Deutsch - Extraktions-, Import- und Build-Werkzeug.

Liest NUR aus starsector-core und schreibt NUR in deutsch-projekt/ und mods/Deutsch/.

  python -I tools/ssde.py extract            englische Quelltexte nach source/ extrahieren
  python -I tools/ssde.py chunk <file> <n>   offene Texte in Arbeitspakete (work/todo) aufteilen
  python -I tools/ssde.py import             fertige Pakete (work/done) pruefen und uebernehmen
  python -I tools/ssde.py build              mods/Deutsch aus Original + Uebersetzungen erzeugen
  python -I tools/ssde.py status             Fortschritt anzeigen
  python -I tools/ssde.py selftest           Build ohne Uebersetzungen muss inhaltsgleich sein
"""
import csv, io, json, os, re, shutil, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.dirname(ROOT)
CORE = os.path.join(GAME, "starsector-core")
MOD = os.path.join(GAME, "mods", "Deutsch")
SRC = os.path.join(ROOT, "source")
TRN = os.path.join(ROOT, "translations")
TODO = os.path.join(ROOT, "work", "todo")
DONE = os.path.join(ROOT, "work", "done")

# Datei -> (Schluesselspalten, uebersetzbare Spalten)
CSV_FILES = {
    "data/strings/descriptions.csv": (["id", "type"], ["text1", "text2", "text3", "text4", "text5"]),
    "data/campaign/abilities.csv": (["id"], ["name", "desc"]),
    "data/campaign/commodities.csv": (["id"], ["name", "desc"]),
    "data/campaign/industries.csv": (["id"], ["name", "desc"]),
    "data/campaign/market_conditions.csv": (["id"], ["name", "desc"]),
    "data/campaign/special_items.csv": (["id"], ["name", "desc"]),
    "data/campaign/submarkets.csv": (["id"], ["name", "desc"]),
    "data/characters/personalities.csv": (["id"], ["name", "desc"]),
    "data/characters/skills/aptitude_data.csv": (["id"], ["name", "description"]),
    "data/characters/skills/skill_data.csv": (["id"], ["name", "description", "author"]),
    "data/hullmods/hull_mods.csv": (["id"], ["name", "desc", "short", "sModDesc"]),
    "data/hulls/ship_data.csv": (["id"], ["designation"]),
    "data/hulls/wing_data.csv": (["id"], ["role desc"]),
    "data/weapons/weapon_data.csv": (["id"], ["name", "primaryRoleStr", "speedStr", "trackingStr",
                                              "accuracyStr", "customPrimary", "customAncillary"]),
    "data/shipsystems/ship_systems.csv": (["id"], ["name"]),
    "data/campaign/rules.csv": (["id"], ["text", "options", "script"]),
}
JSON_FILES = [
    "data/strings/strings.json",
    "data/strings/tooltips.json",
    "data/strings/tips.json",
]
# Script-Befehle in rules.csv, deren "..."-Argumente sichtbarer Text sind
SCRIPT_TEXT_CMDS = {"AddText", "AddTextSmall", "SetTooltip", "Highlight", "SetTextHighlights",
                    "SetTooltipHighlights"}

# Zeichen, die die Spiel-Schriften (insignia/orbitron) nicht haben -> ASCII
NORMALIZE = {"‘": "'", "’": "'", "‚": "'", "“": '"', "”": '"', "„": '"',
             "«": '"', "»": '"', "–": "-", "—": "-", "…": "...", " ": " "}
ALLOWED_EXTRA = set("äöüÄÖÜßéèàáóíçêôâîûåøæÉñ°·×")


def norm(s):
    for a, b in NORMALIZE.items():
        s = s.replace(a, b)
    return s


def read_text(path):
    b = open(path, "rb").read()
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("cp1252")  # einige Originaldateien enthalten verirrte cp1252-Bytes


def jdump(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def jload(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def side(rel):  # data/strings/strings.json -> strings__strings.json
    return rel[len("data/"):].replace("/", "__").rsplit(".", 1)[0] + ".json"


# ---------------------------------------------------------------- CSV

def csv_rows(rel):
    return list(csv.reader(io.StringIO(read_text(os.path.join(CORE, rel)), newline="")))


OPT_RE = re.compile(r"^(\s*(?:-?\d+\s*:\s*)?[^:\s\"]+:)(.*)$")
SCRIPT_STR_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


def script_units(script):
    """(zeilennr, stringnr, start, end, text) fuer sichtbare Strings in Script-Zeilen."""
    out, pos = [], 0
    for ln, line in enumerate(script.split("\n")):
        m = re.match(r"\s*([A-Za-z]+)", line)
        if m and m.group(1) in SCRIPT_TEXT_CMDS:
            for si, sm in enumerate(SCRIPT_STR_RE.finditer(line)):
                if re.search(r"[A-Za-z]", sm.group(1)):
                    out.append((ln, si, pos + sm.start(1), pos + sm.end(1), sm.group(1)))
        pos += len(line) + 1
    return out


def csv_units(rel):
    """Liefert (schluessel, englisch) fuer alle uebersetzbaren Zellen/Teile."""
    keys, cols = CSV_FILES[rel]
    rows = csv_rows(rel)
    head = rows[0]
    ki = [head.index(k) for k in keys]
    for row in rows[1:]:
        if not row or len(row) <= max(ki) or not row[ki[0]] or row[ki[0]].startswith("#"):
            continue
        rk = "|".join(row[i] for i in ki)
        for c in cols:
            ci = head.index(c)
            if ci >= len(row) or not row[ci].strip():
                continue
            val = row[ci]
            if c == "options":
                for line in val.split("\n"):
                    m = OPT_RE.match(line.rstrip("\r"))
                    if m and m.group(2).strip():
                        oid = m.group(1).split(":")[-2].strip()
                        yield f"{rk}#options#{oid}", m.group(2)
            elif c == "script":
                for ln, si, a, b, t in script_units(val):
                    yield f"{rk}#script#{ln}.{si}", t
            else:
                if re.search(r"[A-Za-z]", val):
                    yield f"{rk}#{c}", val


def csv_apply(rel, tr):
    keys, cols = CSV_FILES[rel]
    text = read_text(os.path.join(CORE, rel))
    term = "\r\n" if "\r\n" in text.split("\n", 1)[0] + "\n" or text.split("\n", 1)[0].endswith("\r") else "\n"
    rows = list(csv.reader(io.StringIO(text, newline="")))
    head = rows[0]
    ki = [head.index(k) for k in keys]
    used = 0
    for row in rows[1:]:
        if not row or len(row) <= max(ki) or not row[ki[0]] or row[ki[0]].startswith("#"):
            continue
        rk = "|".join(row[i] for i in ki)
        for c in cols:
            ci = head.index(c)
            if ci >= len(row) or not row[ci].strip():
                continue
            val = row[ci]
            if c == "options":
                lines = val.split("\n")
                for i, line in enumerate(lines):
                    cr = "\r" if line.endswith("\r") else ""
                    m = OPT_RE.match(line.rstrip("\r"))
                    if m and m.group(2).strip():
                        oid = m.group(1).split(":")[-2].strip()
                        t = tr.get(f"{rk}#options#{oid}")
                        if t is not None:
                            lines[i] = m.group(1) + t + cr
                            used += 1
                row[ci] = "\n".join(lines)
            elif c == "script":
                parts, last = [], 0
                for ln, si, a, b, t in script_units(val):
                    n = tr.get(f"{rk}#script#{ln}.{si}")
                    if n is not None:
                        parts += [val[last:a], n]
                        last = b
                        used += 1
                parts.append(val[last:])
                row[ci] = "".join(parts)
            else:
                t = tr.get(f"{rk}#{c}")
                if t is not None:
                    row[ci] = t
                    used += 1
        for i, v in enumerate(row):  # Originaltext ebenfalls auf darstellbare Zeichen normalisieren
            row[i] = norm(v)
    out = io.StringIO(newline="")
    csv.writer(out, lineterminator=term).writerows(rows)
    return out.getvalue(), used


# ---------------------------------------------------------------- JSON (tolerant: #-Kommentare, Kommas, nackte Schluessel)

def json_strings(s):
    """(pfad, start, end, rohinhalt) fuer alle String-WERTE (nicht Schluessel)."""
    out, stack, i, n = [], [], 0, len(s)
    pending_key = None

    def path():
        return ".".join(str(e["k"] if e["t"] == "o" else e["i"]) for e in stack)

    while i < n:
        c = s[i]
        if c == "#":
            while i < n and s[i] != "\n":
                i += 1
            continue
        if c == '"':
            j = i + 1
            while s[j] != '"':
                j += 2 if s[j] == "\\" else 1
            raw = s[i + 1:j]
            k = j + 1
            while k < n and s[k] in " \t\r\n":
                k += 1
            if k < n and s[k] == ":" and stack and stack[-1]["t"] == "o":
                stack[-1]["k"] = raw
            else:
                out.append((path(), i + 1, j, raw))
            i = j + 1
            continue
        if c in "{[":
            stack.append({"t": "o", "k": None} if c == "{" else {"t": "a", "i": 0})
        elif c in "}]":
            stack.pop()
        elif c == "," and stack and stack[-1]["t"] == "a":
            stack[-1]["i"] += 1
        elif (c.isalpha() or c == "_") and stack and stack[-1]["t"] == "o":
            j = i
            while j < n and (s[j].isalnum() or s[j] in "_$."):
                j += 1
            k = j
            while k < n and s[k] in " \t":
                k += 1
            if k < n and s[k] == ":":
                stack[-1]["k"] = s[i:j]
            i = j
            continue
        i += 1
    return out


def junesc(raw):
    return json.loads('"' + raw + '"')


def jesc(text):  # Nicht-ASCII als \\uXXXX -> unabhaengig von der Dateikodierung
    return json.dumps(text, ensure_ascii=True)[1:-1]


def is_texty(v):
    if not re.search(r"[A-Za-z]", v):
        return False
    if re.fullmatch(r"[a-z0-9_.\-/$]+", v) or re.search(r"\.(png|jpg|ogg|wav|fnt|json|csv)$", v):
        return False
    return True


def json_units(rel):
    s = read_text(os.path.join(CORE, rel))
    for p, a, b, raw in json_strings(s):
        v = junesc(raw)
        if is_texty(v):
            yield p, v


def json_apply(rel, tr):
    s = read_text(os.path.join(CORE, rel))
    parts, last, used = [], 0, 0
    for p, a, b, raw in json_strings(s):
        if p in tr:
            parts += [s[last:a], jesc(norm(tr[p]))]
            last = b
            used += 1
    parts.append(s[last:])
    return norm("".join(parts)), used


# ---------------------------------------------------------------- Pruefungen

TOK_RE = re.compile(r"\$[A-Za-z_]\w*(?:\.\w+)*|%[-#+0,(]*\d*(?:\.\d+)?[sdfxX%]|\\n|<[^>]+>|\{\{|\}\}|\{[^{}]*\}")  # {{...}} = Hervorhebung mit sichtbarem Text


def is_choice(tok):
    """Wortwahl-Platzhalter wie $heOrShe, $factionIsOrAre, $onOrAt (CamelCase ...XOrY) liefern englische Woerter."""
    return tok.startswith("$") and bool(re.search(r"[A-Za-z]Or[A-Z][a-z]*$", tok.split(".")[-1]))


def too_long(en, de):
    """Laengenwarnung: deutlich laenger als das Original (kurze Texte strenger)."""
    return len(de) > len(en) * (1.3 if len(en) < 60 else 1.25) + 4


def check(en, de):
    """Liste von Fehlern (leer = ok)."""
    errs = []
    if not de.strip():
        errs.append("leer")
    # $market / $Market sind beide gueltig (Gross-/Kleinschreibung des eingesetzten Wortes)
    a = Counter(t.lower() if t.startswith("$") else t for t in TOK_RE.findall(en))
    b = Counter(t.lower() if t.startswith("$") else t for t in TOK_RE.findall(de))
    # Wortwahl-Platzhalter ($heOrShe, $shipOrFleet ...) liefern englische Woerter -> duerfen entfallen
    choice = {t.lower() for t in TOK_RE.findall(en) if is_choice(t)}
    missing = {t: n for t, n in (a - b).items() if t not in choice}
    extra = dict(b - a)
    if missing or extra:
        errs.append(f"Platzhalter abweichend: fehlt {missing} zuviel {extra}")
    if sum(l.strip() == "OR" for l in en.split("\n")) != sum(l.strip() == "OR" for l in de.split("\n")):
        errs.append("Anzahl der OR-Zeilen (Textvarianten) abweichend")
    fa = [t for t in TOK_RE.findall(en) if t.startswith("%") and t != "%%"]
    fb = [t for t in TOK_RE.findall(de) if t.startswith("%") and t != "%%"]
    if fa != fb and Counter(fa) == Counter(fb):
        errs.append(f"Reihenfolge der %-Platzhalter vertauscht: {fa} -> {fb}")
    bad = {ch for ch in norm(de) if ord(ch) > 127 and ch not in ALLOWED_EXTRA}
    if bad:
        errs.append(f"nicht darstellbare Zeichen {sorted(bad)}")
    if en.count("\n") == 0 and "\n" in de:
        errs.append("neuer Zeilenumbruch")
    return errs


def check_unit(key, en, de):
    errs = check(en, de)
    if "#script#" in key and re.search(r'(?<!\\)"', de):
        errs.append("unmaskiertes Anfuehrungszeichen in Script-String")
    if "#options#" in key and "\n" in de:
        errs.append("Zeilenumbruch in Option")
    if key.startswith("java#") and not re.fullmatch(
            r'(?:[^"\\\r\n]|\\[btnfr"\'\\]|\\u[0-9a-f]{4})*', java_esc(norm(de))):
        errs.append("kein gueltiges Java-Stringliteral (Backslash/Zeilenumbruch?)")
    return errs


# ---------------------------------------------------------------- Befehle

# ---------------------------------------------------------------- Missionen

def mission_files():
    base = os.path.join(CORE, "data", "missions")
    out = []
    for m in sorted(os.listdir(base)):
        if os.path.isfile(os.path.join(base, m, "mission_text.txt")):
            out += [f"data/missions/{m}/descriptor.json", f"data/missions/{m}/mission_text.txt",
                    f"data/missions/{m}/MissionDefinition.java"]
    return out


JAVA_TEXT_RE = re.compile(r'api\.(?:setFleetTagline|addBriefingItem)\((?:[^;"]*,\s*)?"((?:[^"\\]|\\.)*)"\s*\)')


def java_units(rel):
    s = read_text(os.path.join(CORE, rel))
    for i, m in enumerate(JAVA_TEXT_RE.finditer(s)):
        yield f"java#{i}", m.group(1).replace('\\"', '"')


def java_esc(text):  # Anfuehrungszeichen maskieren, Nicht-ASCII als \\uXXXX (Kodierung egal)
    text = re.sub(r'(?<!\\)"', '\\"', text)
    return "".join(c if ord(c) < 128 else f"\\u{ord(c):04x}" for c in text)


def java_apply(rel, tr):
    s = read_text(os.path.join(CORE, rel))
    parts, last, used = [], 0, 0
    for i, m in enumerate(JAVA_TEXT_RE.finditer(s)):
        t = tr.get(f"java#{i}")
        if t is not None:
            lit = java_esc(norm(t))
            # muss ein gueltiges Java-Stringliteral bleiben (sonst Absturz beim Kompilieren der Mission)
            assert re.fullmatch(r'(?:[^"\\\r\n]|\\[btnfr"\'\\]|\\u[0-9a-f]{4})*', lit), f"{rel}: ungueltiges Literal {lit!r}"
            parts += [s[last:m.start(1)], lit]
            last = m.end(1)
            used += 1
    parts.append(s[last:])
    return "".join(parts), used


def txt_units(rel):
    yield "text", read_text(os.path.join(CORE, rel))


def txt_apply(rel, tr):
    t = tr.get("text")
    return norm(t if t is not None else read_text(os.path.join(CORE, rel))), int(t is not None)


def all_files():
    return list(CSV_FILES) + JSON_FILES + mission_files()


def units(rel):
    if rel.endswith(".csv"):
        return csv_units(rel)
    if rel.endswith(".java"):
        return java_units(rel)
    if rel.endswith(".txt"):
        return txt_units(rel)
    if rel.endswith("descriptor.json"):  # nur der Titel ist Anzeigetext
        return ((k, v) for k, v in json_units(rel) if k == "title")
    return json_units(rel)


def apply_any(rel, tr):
    if rel.endswith(".csv"):
        return csv_apply(rel, tr)
    if rel.endswith(".java"):
        return java_apply(rel, tr)
    if rel.endswith(".txt"):
        return txt_apply(rel, tr)
    return json_apply(rel, tr)


def cmd_extract():
    for rel in all_files():
        u = {}
        for k, v in units(rel):
            assert k not in u, f"doppelter Schluessel {rel} {k}"
            u[k] = norm(v)
        jdump(u, os.path.join(SRC, side(rel)))
        print(f"{rel}: {len(u)} Texte")


def cmd_status():
    tot_s = tot_d = 0
    for rel in all_files():
        s = jload(os.path.join(SRC, side(rel)), {})
        t = jload(os.path.join(TRN, side(rel)), {})
        cs = sum(len(v) for v in s.values())
        cd = sum(len(v) for k, v in s.items() if k in t)
        tot_s += cs
        tot_d += cd
        print(f"{rel:48s} {len(t):6d}/{len(s):6d} Texte  {100 * cd / max(cs, 1):5.1f}% Zeichen")
    print(f"GESAMT {100 * tot_d / tot_s:.1f}% der Zeichen uebersetzt")


def cmd_chunk(rel, size):
    s = jload(os.path.join(SRC, side(rel)))
    t = jload(os.path.join(TRN, side(rel)), {})
    os.makedirs(TODO, exist_ok=True)
    base = side(rel)[:-5]
    taken, nums = set(), [-1]
    for fn in os.listdir(TODO):
        if fn.startswith(base + "--"):
            taken |= set(jload(os.path.join(TODO, fn)))
            nums.append(int(fn.rsplit("--", 1)[1][:3]))
    t = dict(t, **{k: None for k in taken})
    chunk, n, cur, last_row = {}, max(nums) + 1, 0, None
    first = n
    for k, v in s.items():
        row = k.split("#")[0] if rel.endswith(".csv") else None
        if k in t:
            continue
        if cur >= size and row != last_row:  # eine Regel nie auf zwei Pakete verteilen
            jdump(chunk, os.path.join(TODO, f"{base}--{n:03d}.json"))
            chunk, cur, n = {}, 0, n + 1
        chunk[k] = v
        cur += len(v)
        last_row = row
    if chunk:
        jdump(chunk, os.path.join(TODO, f"{base}--{n:03d}.json"))
        n += 1
    print(f"{n - first} Pakete fuer {rel} (ab Nr. {first})")


def cmd_import(only=None):
    by_base = {side(r)[:-5]: r for r in all_files()}
    ok_total = 0
    for fn in sorted(os.listdir(DONE)) if os.path.isdir(DONE) else []:
        if not fn.endswith(".json") or (only and not any(fn.startswith(o) for o in only)):
            continue
        rel = by_base[fn.split("--")[0]]
        src = jload(os.path.join(SRC, side(rel)))
        todo = jload(os.path.join(TODO, fn), {})
        try:
            done = jload(os.path.join(DONE, fn))
        except Exception as e:
            print(f"!! {fn}: ungueltiges JSON: {e}")
            continue
        tr = jload(os.path.join(TRN, side(rel)), {})
        ok = bad = 0
        for k, de in done.items():
            if k not in src:
                print(f"!! {fn}: unbekannter Schluessel {k}")
                bad += 1
                continue
            de = norm(de)
            if "\r\n" in src[k]:  # Zeilenumbrueche wie im Original (CRLF)
                de = re.sub(r"(?<!\r)\n", "\r\n", de)
            if not re.search(r"%\s+\w", src[k]):  # dt. "50 %" -> "50%" (sonst Formatierungsfehler-Gefahr)
                de = re.sub(r"(\d) %", r"\g<1>%", de)
            errs = check_unit(k, src[k], de)
            if errs:
                print(f"!! {fn}: {k}: {'; '.join(errs)}")
                bad += 1
                continue
            tr[k] = de
            ok += 1
        missing = [k for k in todo if k not in done]
        jdump(tr, os.path.join(TRN, side(rel)))
        long_ = sum(1 for k in done if k in tr and too_long(src[k], tr[k]))
        print(f"{fn}: {ok} uebernommen, {bad} abgelehnt, {len(missing)} fehlen, {long_} deutlich laenger")
        ok_total += ok
        if bad == 0 and not missing:
            os.remove(os.path.join(DONE, fn))
            if os.path.exists(os.path.join(TODO, fn)):
                os.remove(os.path.join(TODO, fn))
    print(f"insgesamt {ok_total} uebernommen")


def cmd_prefill():
    """Setzt Standardtexte (tools/standardtexte.json) fuer alle exakt passenden Dialog-Eintraege."""
    std = jload(os.path.join(ROOT, "tools", "standardtexte.json"))
    rel = "data/campaign/rules.csv"
    src = jload(os.path.join(SRC, side(rel)))
    tr = jload(os.path.join(TRN, side(rel)), {})
    n = 0
    for k, v in src.items():
        de = std.get(v.strip())
        if de is not None and "#text" not in k:
            de = v[:len(v) - len(v.lstrip())] + de + v[len(v.rstrip()):]
            if not check_unit(k, v, de):
                tr[k] = de
                n += 1
    jdump(tr, os.path.join(TRN, side(rel)))
    print(f"{n} Standardtexte gesetzt")


def cmd_review():
    """Schreibt work/review.json: zu lange Texte und Hervorhebungen, die im Text nicht mehr vorkommen."""
    out = {"zu_lang": [], "hervorhebung_fehlt": []}
    for rel in all_files():
        src = jload(os.path.join(SRC, side(rel)), {})
        tr = jload(os.path.join(TRN, side(rel)), {})
        for k, v in tr.items():
            if k in src and too_long(src[k], v):
                out["zu_lang"].append([side(rel), k, src[k], v])
    rel = "data/campaign/rules.csv"
    tr = jload(os.path.join(TRN, side(rel)), {})
    rows = csv_rows(rel)
    h = rows[0]
    for row in rows[1:]:
        if len(row) < len(h) or not row[0] or row[0].startswith("#"):
            continue
        text = tr.get(f"{row[0]}#text")
        if text is None:
            continue
        lines = row[h.index("script")].split("\n")
        for ln, si, a, b, t in script_units(row[h.index("script")]):
            cmd = lines[ln].split()[0]
            de = tr.get(f"{row[0]}#script#{ln}.{si}")
            if cmd in ("Highlight", "SetTextHighlights") and t in row[h.index("text")] and de and de not in text:
                out["hervorhebung_fehlt"].append([row[0], f"{row[0]}#script#{ln}.{si}", t, de])
    jdump(out, os.path.join(ROOT, "work", "review.json"))
    print({k: len(v) for k, v in out.items()})


def cmd_build(dest=MOD, empty=False):
    replace, written, files = [], [], []
    for rel in all_files():
        tr = {} if empty else jload(os.path.join(TRN, side(rel)), {})
        if not tr and not empty:
            continue
        src = jload(os.path.join(SRC, side(rel)), {})
        tr = {k: v for k, v in tr.items() if k in src and not check_unit(k, src[k], v)}
        text, used = apply_any(rel, tr)
        out = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        files.append(rel)
        # .txt/.java ueberschreiben per Pfad; "replace" nur fuer zusammengefuehrte CSV/JSON
        if not rel.startswith("data/missions/") or rel.endswith(".json"):
            replace.append(rel)
        written.append(f"{rel}: {used} Texte")
    info = {
        "id": "deutsch_uebersetzung",
        "name": "Deutsche Übersetzung",
        "author": "Christian Wenski",
        "utility": "true",
        "version": "0.3.0",
        "description": "Deutsche Übersetzung der Spieltexte (Dialoge, Beschreibungen, Tooltips, Missionen). "
                       "Verändert keine Dateien des Spiels - zum Zurücksetzen einfach deaktivieren.",
        "gameVersion": "0.98a-RC8",
        "replace": replace,
    }
    with open(os.path.join(dest, "mod_info.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(info, f, ensure_ascii=True, indent=1)
    print("\n".join(written))
    return files


def cmd_selftest():
    tmp = os.path.join(ROOT, "work", "selftest")
    shutil.rmtree(tmp, ignore_errors=True)
    for rel in cmd_build(tmp, empty=True):
        a = read_text(os.path.join(CORE, rel))
        b = read_text(os.path.join(tmp, rel))
        if rel.endswith(".csv"):
            ra = [[norm(c) for c in r] for r in csv.reader(io.StringIO(a, newline=""))]
            rb = list(csv.reader(io.StringIO(b, newline="")))
            assert ra == rb, f"CSV-Roundtrip abweichend: {rel}"
            a = b
        else:
            assert norm(a) == b, f"Roundtrip abweichend: {rel}"
            a = norm(a)
        # Probe: jeden Text durch Markierung ersetzen und pruefen, dass nur Textstellen betroffen sind
        src = jload(os.path.join(SRC, side(rel)))
        probe = {k: "XX" + v for k, v in src.items()}
        text, used = apply_any(rel, probe)
        assert used == len(src), f"{rel}: {used} != {len(src)}"
        if rel.endswith(".csv"):
            keys, cols = CSV_FILES[rel]
            ra = list(csv.reader(io.StringIO(a, newline="")))
            rb = list(csv.reader(io.StringIO(text, newline="")))
            assert len(ra) == len(rb)
            h = ra[0]
            for x, y in zip(ra, rb):
                for i, (p, q) in enumerate(zip(x, y)):
                    if h[i] not in cols:
                        assert p == q, f"{rel}: Spalte {h[i]} veraendert"
        print(f"OK {rel}")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "extract":
        cmd_extract()
    elif c == "status":
        cmd_status()
    elif c == "chunk":
        cmd_chunk(sys.argv[2], int(sys.argv[3]))
    elif c == "import":  # optional: nur Pakete mit diesen Namensanfaengen (laufende Uebersetzer nicht stoeren)
        cmd_import(sys.argv[2:] or None)
    elif c == "build":
        cmd_build()
    elif c == "prefill":
        cmd_prefill()
    elif c == "review":
        cmd_review()
    elif c == "selftest":
        cmd_selftest()
