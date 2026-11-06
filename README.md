# Starsector - Deutsche Übersetzung

Inoffizielle deutsche Übersetzung für [Starsector](https://fractalsoftworks.com/) **0.98a-RC8**.
Übersetzt sind Dialoge (`rules.csv`), Beschreibungen, Tooltips, Tipps, Schiffe, Waffen, Fertigkeiten,
Missionen und der Codex. Die Spieldateien selbst werden **nicht** verändert.

## Installation (für Spieler)
1. Unter [Releases](../../releases) die neueste `Deutsch.zip` herunterladen.
2. In den Ordner `mods` der Starsector-Installation entpacken (danach gibt es `Starsector/mods/Deutsch/mod_info.json`).
3. Im Starsector-Launcher unter "Mods" die **Deutsche Übersetzung** aktivieren.

Zurück auf Englisch: Mod im Launcher deaktivieren oder den Ordner `mods/Deutsch` löschen.

## Was (noch) nicht übersetzt wird
- Texte, die im Java-Code fest eingebaut sind (`starfarer.api.jar`, `starfarer_obf.jar`): Hauptmenü, viele
  Bildschirm-Beschriftungen, Intel-Texte, Kolonie-Panels. Diese erfordern Jar-Patching (eigene Phase).
- Platzhalter wie `$faction` werden vom Spiel mit englischen Wörtern gefüllt ("Hegemony").
- Fraktionsnamen (`data/world/factions/*.faction`) - folgen später.

Fehler oder holprige Formulierungen gefunden? Gerne als [Issue](../../issues) melden.

---

## Für Mitwirkende

### Aufbau
| Ort | Inhalt |
|---|---|
| `<Spielordner>/starsector-core/` | Originalspiel - wird **nie** verändert (nur gelesen) |
| `<Spielordner>/mods/Deutsch/` | Erzeugter Mod (wird bei jedem Build komplett neu geschrieben) |
| `translations/` | Deutsche Übersetzungen (`schluessel -> deutsch`) - **das eigentliche Arbeitsergebnis** |
| `source/` | Extrahierte englische Texte (`schluessel -> englisch`), lokal per `extract` erzeugt, nicht im Repo |
| `work/todo`, `work/done` | Arbeitspakete für Übersetzer (lokal, nicht im Repo) |
| `tools/` | Extraktion, Import, Prüfung und Build |
| `GLOSSAR.md` | Verbindliche Begriffe und Stilregeln |
| `ANLEITUNG_UEBERSETZER.md` | Anleitung für Übersetzungspakete |

Die englischen Originaltexte gehören Fractal Softworks und sind deshalb nicht im Repository enthalten.

### Einrichtung
Python 3 wird benötigt. Den Starsector-Ordner (der `starsector-core` enthält) angeben, entweder per
Umgebungsvariable `STARSECTOR_DIR` oder als einzelne Zeile in `starsector_pfad.txt` im Projektordner
(diese Datei ist lokal und wird nicht eingecheckt), z.B.:
```
E:\Spiele\Starsector
```

### Befehle (im Projektordner)
```
python -I tools/ssde.py extract    # englische Texte nach source/ extrahieren (einmalig nach dem Klonen)
python -I tools/ssde.py status     # Fortschritt
python -I tools/ssde.py import     # fertige Pakete aus work/done prüfen + übernehmen
python -I tools/ssde.py build      # Mod nach <Spielordner>/mods/Deutsch schreiben
python -I tools/ssde.py selftest   # Werkzeug-Selbsttest
```
Der Import lehnt Übersetzungen ab, bei denen Platzhalter (`$faction`, `%s`, ...) fehlen oder verändert sind,
oder die Zeichen enthalten, die die Spielschriften nicht darstellen können.

### Missionen (ab 0.3.0)
Titel (`descriptor.json`), Briefing (`mission_text.txt`) und Flottentexte/Ziele (`MissionDefinition.java`).
In den Java-Dateien werden nur die Strings in `setFleetTagline`/`addBriefingItem` ersetzt; Umlaute als Unicode-Escapes (z.B. `\u00e4` für ä).
Import und Build prüfen, dass jedes Literal gültiges Java bleibt.

### Codex (ab 0.4.0)
`data/codex/*.txt` zeilenweise: Steuerzeilen (BEGIN/CATEGORY-IDs, ICON, IMAGE, COLOR, RESET, END, RELATED, FONT, TEST, #) bleiben byte-identisch;
Linkziele in `{{rel:ziel|Label}}` werden beim Import geprüft. Tastennamen und `{{Intel}}` bleiben englisch.

## Lizenz
Werkzeuge (`tools/`) und Übersetzungstexte: MIT-Lizenz, siehe [LICENSE](LICENSE).
Starsector sowie alle Originalinhalte des Spiels sind Eigentum von Fractal Softworks. Dies ist ein inoffizielles Fan-Projekt.
