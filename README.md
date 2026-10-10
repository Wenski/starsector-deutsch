# Starsector - Deutsche Übersetzung (Projekt)

## Aufbau
| Ort | Inhalt |
|---|---|
| `../starsector-core/` | Originalspiel - wird **nie** verändert (nur gelesen) |
| `../mods/Deutsch/` | Erzeugter Mod (wird bei jedem Build komplett neu geschrieben) |
| `source/` | Extrahierte englische Texte (`schluessel -> englisch`) |
| `translations/` | Deutsche Übersetzungen (`schluessel -> deutsch`) - **das eigentliche Arbeitsergebnis** |
| `work/todo`, `work/done` | Arbeitspakete für Übersetzer |
| `GLOSSAR.md` | Verbindliche Begriffe und Stilregeln |
| `core-checksums-vorher.sha256` | Prüfsummen des Originalspiels vor Projektbeginn |

## Befehle (im Ordner `deutsch-projekt`)
```
python -I tools/ssde.py status     # Fortschritt
python -I tools/ssde.py import     # fertige Pakete aus work/done prüfen + übernehmen
python -I tools/ssde.py build      # Mod nach ../mods/Deutsch schreiben
python -I tools/ssde.py selftest   # Werkzeug-Selbsttest
```
Der Import lehnt Übersetzungen ab, bei denen Platzhalter (`$faction`, `%s`, ...) fehlen oder verändert sind,
oder die Zeichen enthalten, die die Spielschriften nicht darstellen können.

## Zurücksetzen
- **Spiel wieder auf Englisch:** Im Starsector-Launcher unter "Mods" die "Deutsche Übersetzung" deaktivieren
  (oder den Ordner `mods/Deutsch` löschen - er kann jederzeit per `build` neu erzeugt werden).
- **Originalspiel prüfen:** `cd ../starsector-core && sha256sum -c --quiet ../deutsch-projekt/core-checksums-vorher.sha256`
  (keine Ausgabe = unverändert; `starsector.log` ändert sich bei jedem Spielstart und ist ausgenommen).
- **Übersetzungsstand zurückdrehen:** jeder Schritt ist ein Git-Commit.
  `git log --oneline` zeigt die Historie, `git checkout <commit> -- translations/` stellt einen alten Stand wieder her,
  danach `build`.

## Was (noch) nicht übersetzt wird
- Texte, die im Java-Code fest eingebaut sind (`starfarer.api.jar`, `starfarer_obf.jar`): Hauptmenü, viele
  Bildschirm-Beschriftungen, Intel-Texte, Kolonie-Panels. Diese erfordern Jar-Patching (eigene Phase).
- Platzhalter wie `$faction` werden vom Spiel mit englischen Wörtern gefüllt ("Hegemony").
- Fraktionsnamen (`data/world/factions/*.faction`) und Codex-Einträge - folgen später.

## Missionen (ab 0.3.0)
Titel (`descriptor.json`), Briefing (`mission_text.txt`) und Flottentexte/Ziele (`MissionDefinition.java`).
In den Java-Dateien werden nur die Strings in `setFleetTagline`/`addBriefingItem` ersetzt; Umlaute als `ä`-Escapes.
Import und Build prüfen, dass jedes Literal gültiges Java bleibt.
