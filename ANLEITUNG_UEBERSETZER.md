# Anleitung für Übersetzungspakete (Starsector -> Deutsch)

Du übersetzt Texte des Weltraumspiels **Starsector** (2D-Flottenkampf/Handel/Erkundung, düstere Post-Kollaps-Sci-Fi) ins Deutsche.

## Ablauf
1. Lies `E:\Spiele\Starsector\deutsch-projekt\GLOSSAR.md` vollständig. Glossar und Stilregeln sind verbindlich.
2. Lies dein Paket `work/todo/<name>.json` (ein JSON-Objekt `{schluessel: englischer Text}`).
3. Schreibe `work/done/<name>.json` (gleicher Dateiname) mit **exakt denselben Schlüsseln** und dem deutschen Text als Wert. Jeden Schlüssel übernehmen, keinen auslassen, keinen hinzufügen.
4. Die Ausgabe muss gültiges JSON sein (UTF-8, Anführungszeichen im Text als `\"` maskieren, Zeilenumbrüche als `\n`). Prüfe die Datei danach mit:
   `python -I -c "import json,sys; json.load(open(sys.argv[1],encoding='utf-8')); print('ok')" <datei>`
4b. Danach **Selbstprüfung**: `python -I tools/pruefe_paket.py work/done/<name>.json` (im Projektordner).
   Alle FEHLER und HERVORHEBUNG-Meldungen beheben; ZU LANG-Meldungen möglichst kürzen. Ziel: Längenverhältnis gesamt <= 1.15.
   Wiederholen, bis 0 Fehler. (Das Skript ändert nichts - übernommen wird erst durch den Koordinator.)
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

## LÄNGE (wichtig!)
Die deutsche Fassung soll **ungefähr so lang sein wie das Original** - Ziel: höchstens ca. 10-15 % länger,
bei kurzen Texten (Buttons, Optionen, Namen, Tooltips) möglichst **nicht länger** als das Englische.
Die UI hat feste Breiten; zu lange Texte werden abgeschnitten oder umbrechen hässlich.
- Knapp formulieren: Füllwörter streichen, Nominalstil vermeiden, kurze Synonyme wählen
  ("Höchstgeschwindigkeit" -> "Tempo", "verringert" -> "senkt", "Explosionsschutztüren" -> "Druckschotts").
- Übliche Abkürzungen sind bei kurzen Labels erlaubt: "max.", "min.", "ca.", "z.B.", "Std.", "Ballist.", "Org.".
- Bei Dialogen: lieber Satzbau vereinfachen, als Inhalt zu streichen. Inhalt/Informationen nie weglassen.
- Das Werkzeug meldet Texte, die deutlich länger sind (>30 % bei kurzen, >25 % bei langen Texten).

## Dialoge (rules.csv) - Schlüssel und Sonderregeln
- `regelId#text` = erzählender Dialogtext. `regelId#options#optionId` = Antwortoption/Button (kurz!).
  `regelId#script#Z.S` = Text in einem Script-Befehl (AddText, SetTooltip, Highlight ...).
- Einträge mit demselben `regelId` gehören zusammen - immer gemeinsam betrachten.
- **Hervorhebungen:** Ein Script-String einer Regel, der wörtlich im englischen `#text` derselben Regel vorkommt,
  ist eine Hervorhebung (Highlight). Die Übersetzung muss dann **wörtlich (gleiche Schreibung, gleicher Kasus)
  in deinem übersetzten #text** vorkommen. Notfalls den Text so formulieren, dass es passt.
- **Zeilen, die nur `OR` enthalten**, trennen Zufallsvarianten - exakt so stehen lassen (gleiche Anzahl).
- Anführungszeichen in `#script#`-Strings müssen als `\"` im Text stehen (in JSON also `\\\"`); am besten vermeiden.
- Optionen: kein Zeilenumbruch. Optionen in "..." sind wörtliche Rede des Spielers -> ebenfalls in "...".
- **Wortwahl-Platzhalter** liefern englische Wörter: `$heOrShe`/`$HeOrShe` (he/she), `$hisOrHer`, `$himOrHer`,
  `$himOrHerself`, `$manOrWoman`, `$brotherOrSister`, `$playerSirOrMadam` (sir/ma'am), `$shipOrFleet`, `$aOrAn`
  sowie Varianten mit Präfix (z.B. `$gaTJ_heOrShe`). Diese **dürfen (und sollen meist) wegfallen**:
  Satz neutral bauen - z.B. Name/Rang verwenden, sofern `$personName`/`$PersonName`/`$personLastName`/`$rank`/`$post`
  im SELBEN Eintrag schon vorkommt (dann darf man es nicht zusätzlich einfügen, nur umstellen - Platzhalter dürfen
  NICHT neu hinzukommen), sonst neutrale Umschreibung ("Ihr Gegenüber", "die Kommandantin/der Kommandant" vermeiden ->
  "die Person", "das Gegenüber", Passiv, direkte Rede ohne Pronomen). `$playerSirOrMadam` -> "Kapitän".
  `$shipOrFleet` -> "Flotte" oder neutral ("Ihr Verband").
- Alle anderen Platzhalter (`$personName`, `$post`, `$rank`, `$faction`, `$marketName`, `$global.xyz` ...) müssen
  in gleicher Anzahl erhalten bleiben. `$post`/`$rank` werden mit englischen Rängen gefüllt ("Commander",
  "Administrator") - so einbauen, dass das gut lesbar bleibt (z.B. "der/die $post" vermeiden -> "$post $personLastName").
- Duzen/Siezen: Fremde und Untergebene siezen den Spieler. Raue Typen (Piraten, Gauner, Pfad-Fanatiker) dürfen
  den Spieler duzen, wenn das zur Figur passt - innerhalb einer Szene konsistent bleiben.
- Spielmechanik-Texte (Kosten, Mengen, Reputation) knapp und eindeutig.

## Qualität
- Natürliches Deutsch, Sinn vor Wörtlichkeit, Ton erhalten (Lore-Texte sind oft trocken-ironisch oder pseudo-historisch).
- Einheitlich bleiben: gleiche englische Begriffe -> gleiche deutsche Begriffe innerhalb deines Pakets.
- Keine typografischen Anführungszeichen/Gedankenstriche/Auslassungszeichen - nur `"` `'` `-` `...`.
- Keine Anmerkungen, keine Kommentare im JSON.

Am Ende kurz melden: Dateiname, Anzahl Einträge, und ggf. unsichere Entscheidungen (max. 5 Stichpunkte).

## Standard-Optionen (bereits zentral übersetzt - in deinen Texten genauso verwenden)
Continue = Weiter · Leave = Gehen · Back = Zurück · Accept = Annehmen · Decline/Refuse = Ablehnen ·
Cut the comm link / Cut the comms = Verbindung trennen · Say nothing = Schweigen · Never mind = Schon gut ·
End the conversation = Gespräch beenden · Explore = Erkunden · Wait = Warten · Follow = Folgen ·
shuttle = Fähre · comm link / comms = Verbindung / Kommunikation · bribe = Bestechung
