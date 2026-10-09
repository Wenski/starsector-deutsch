# Anleitung für Übersetzungspakete (Starsector -> Deutsch)

Du übersetzt Texte des Weltraumspiels **Starsector** (2D-Flottenkampf/Handel/Erkundung, düstere Post-Kollaps-Sci-Fi) ins Deutsche.

## Ablauf
1. Lies `E:\Spiele\Starsector\deutsch-projekt\GLOSSAR.md` vollständig. Glossar und Stilregeln sind verbindlich.
2. Lies dein Paket `work/todo/<name>.json` (ein JSON-Objekt `{schluessel: englischer Text}`).
3. Schreibe `work/done/<name>.json` (gleicher Dateiname) mit **exakt denselben Schlüsseln** und dem deutschen Text als Wert. Jeden Schlüssel übernehmen, keinen auslassen, keinen hinzufügen.
4. Die Ausgabe muss gültiges JSON sein (UTF-8, Anführungszeichen im Text als `\"` maskieren, Zeilenumbrüche als `\n`). Prüfe die Datei danach mit:
   `python -I -c "import json,sys; json.load(open(sys.argv[1],encoding='utf-8')); print('ok')" <datei>`
5. Große Pakete darfst du in mehreren Schritten schreiben (z.B. erst Hälfte per Write, dann per Edit ergänzen), solange am Ende eine gültige vollständige Datei steht.

## Schlüssel verstehen
- `id|TYPE#text1` (descriptions): text1 = Hauptbeschreibung, text2/text3 = Zusatztexte (z.B. Kurzbeschreibung, Herstellerzitat). Text ist oft mehrabsätzig (`\n\n`) - Absatzstruktur beibehalten.
- `...#name` = Anzeigename (kurz halten). `#desc` = Beschreibung. `#short` = Kurzbeschreibung. `#sModDesc` = Effekt als eingebaute S-Mod.
- `#designation` = Schiffsklassen-Bezeichnung (z.B. "Destroyer" -> "Zerstörer").
- `#author` (Fertigkeiten) = Quellenangabe eines Zitats - Namen bleiben, nur beschreibende Wörter übersetzen ("final address to the crew of" -> "letzte Ansprache an die Besatzung der").
- Waffen `#primaryRoleStr`/`#speedStr`/`#trackingStr`/`#accuracyStr` = kurze Tabellenwerte ("Anti Armor" -> "Anti-Panzerung", "Point Defense" -> "Punktverteidigung", "Fast" -> "Schnell", "Excellent" -> "Exzellent", "None" -> "Keine", "Perfect" -> "Perfekt").
- JSON-Pfade wie `fleetInteractionDialog.initialAggressive` geben Kontext, wo der Text erscheint.

## Was NICHT übersetzt wird (unverändert übernehmen)
- Eigennamen: Schiffsklassen (Onslaught, Lasher, Paragon, Hammerhead ...), Personen, Planeten, Systeme, Stationen, Schiffsnamen (ISS/HSS/TTS ...). Hersteller-/Technologiestufen wie "Low Tech", "High Tech", "Midline".
- Eigennamen von Waffen sind oft Markennamen (z.B. "Hellbore Cannon" -> "Hellbore-Kanone", "Harpoon MRM" -> "Harpoon MRM", "Sabot SRM" bleibt). Gattungsbegriffe werden übersetzt ("Light Machine Gun" -> "Leichtes Maschinengewehr", "Heavy Mortar" -> "Schwerer Mörser", "Tactical Laser" -> "Taktischer Laser", "Ion Cannon" -> "Ionenkanone", "Flak Cannon" -> "Flak-Kanone").
- Rumpfmodifikationen: Namen übersetzen ("Integrated Targeting Unit" -> "Integrierte Zieleinheit", "Hardened Shields" -> "Gehärtete Schilde"), aber Abkürzungen wie "ITU" beibehalten.
- Platzhalter (siehe Glossar) exakt erhalten. Wird `%s` später durch eine Zahl mit Einheit ersetzt, Satz entsprechend bauen.
- Werte, die erkennbar kein Anzeigetext sind (IDs, Variablen, Code) -> unverändert.

## Qualität
- Natürliches Deutsch, Sinn vor Wörtlichkeit, Ton erhalten (Lore-Texte sind oft trocken-ironisch oder pseudo-historisch).
- Einheitlich bleiben: gleiche englische Begriffe -> gleiche deutsche Begriffe innerhalb deines Pakets.
- Keine typografischen Anführungszeichen/Gedankenstriche/Auslassungszeichen - nur `"` `'` `-` `...`.
- Keine Anmerkungen, keine Kommentare im JSON.

Am Ende kurz melden: Dateiname, Anzahl Einträge, und ggf. unsichere Entscheidungen (max. 5 Stichpunkte).
