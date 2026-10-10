# Glossar & Stilregeln - Starsector Deutsch

## Stil
- Anrede des Spielers: **"Sie"** (formell, militärischer Ton). Erzähltext in 2. Person: "Sie sehen...", "Ihre Flotte...".
- NPCs untereinander und raue Charaktere (Piraten, Schmuggler) dürfen "du"/"ihr" verwenden, wenn es zur Szene passt; gegenüber dem Spieler standardmäßig "Sie".
- Natürliches, flüssiges Deutsch, kein Wort-für-Wort. Ton und Charakter (Sarkasmus, Pathos, Bürokratensprache) erhalten.
- Möglichst kompakt formulieren - UI-Felder haben feste Breite. Kurze Labels (Buttons, Namen) kurz halten.
- Umlaute und ß verwenden (ä ö ü Ä Ö Ü ß).
- **Nur gerade Anführungszeichen `"` und `'`**, nur Bindestrich `-` (keine „deutschen" Anführungszeichen, keine Gedankenstriche –/—, kein …). Die Spielschriften haben diese Zeichen nicht.
- Wenn das Original direkte Rede in "..." setzt, ebenso "..." verwenden.

## Technische Regeln (zwingend)
- Platzhalter exakt übernehmen, gleiche Anzahl: `$faction`, `$playerName`, `$fleetOrShip`, `$heOrShe`, `%s`, `%d`, `%,d`, `%.1f`, `%%`, `\n` (als Zeichenfolge Backslash+n), `<...>`, `{...}`.
- Platzhalter dürfen umgestellt werden (Satzbau), aber nicht verändert/übersetzt/gelöscht werden.
- Achtung: Platzhalter werden vom Spiel mit **englischen** Wörtern gefüllt (z.B. `$faction` = "Hegemony", `$heOrShe` = "he"). Sätze so bauen, dass das grammatisch möglichst wenig stört (z.B. "Die $faction-Flotte" statt Kasus-abhängiger Konstruktionen).
- Proper names / Eigennamen NICHT übersetzen: Schiffsklassen (Onslaught, Hammerhead, Paragon...), Waffenmarken-Eigennamen (z.B. "Hellbore", "Sabot", "Harpoon"), Planeten, Systeme, Stationen, Personen, Schiffsnamen (ISS ..., HSS ...).
- Schlüssel (JSON-Keys) niemals ändern. Ist ein Wert erkennbar kein Anzeigetext (Variablenname, ID, Code), ihn unverändert übernehmen.

## Fraktionen
| Englisch | Deutsch |
|---|---|
| Hegemony | Hegemonie |
| Tri-Tachyon (Corporation) | Tri-Tachyon (Konzern) |
| Persean League | Perseanische Liga |
| Sindrian Diktat | Sindrianisches Diktat |
| Luddic Church | Luddische Kirche |
| Luddic Path | Luddischer Pfad |
| Knights of Ludd | Ritter von Ludd |
| Pirates | Piraten |
| Independent(s) | Unabhängige |
| Remnant | Remnant (Eigenname, nicht übersetzen) |
| Domain (of Man) | Domäne (der Menschheit) |
| Domain-era | aus der Domänen-Ära |
| Lion's Guard | Löwengarde |
| Pather | Pfadanhänger |
| Luddic / Luddite | luddisch / Luddit |
| Derelict (Fraktion) | Verlassene |
| Omega | Omega |
| Threat | Bedrohung |
| Shrouded Dweller | Verhüllter Bewohner |

## Orte & Allgemeines
| Englisch | Deutsch |
|---|---|
| the Sector / Persean Sector | der Sektor / Perseanischer Sektor |
| Core Worlds | Kernwelten |
| the Fringe | der Rand |
| Hyperspace | Hyperraum |
| jump point | Sprungpunkt |
| Gate / Gate network | Tor / Tornetzwerk |
| Collapse | der Kollaps |
| AI War(s) | KI-Krieg(e) |
| AI core (Alpha/Beta/Gamma) | KI-Kern (Alpha-/Beta-/Gamma-Kern) |
| Coronal Hypershunt | Koronaler Hypershunt |
| Cryosleeper | Kryoschläfer |
| colony | Kolonie |
| spaceport | Raumhafen |
| market / open market / black market / military market | Markt / Freier Markt / Schwarzmarkt / Militärmarkt |
| tariff | Zoll |
| bar | Bar |
| bounty | Kopfgeld |
| commission | Kommission |
| reputation | Ansehen |
| hostile / inhospitable / suspicious / neutral / favorable / welcoming / friendly / trusting / cooperative / vengeful | feindlich / ungastlich / misstrauisch / neutral / wohlgesonnen / einladend / freundlich / vertrauensvoll / kooperativ / rachsüchtig |
| intel | Intel |
| survey | Vermessung |
| salvage | Bergung / bergen |
| derelict (ship) | Wrack |
| mothball | einmotten |
| transponder | Transponder |
| story point | Storypunkt |
| credits | Credits |
| c206 (Zyklus) | c206 (unverändert) |
| cycle | Zyklus |

## Ressourcen
| Englisch | Deutsch |
|---|---|
| supplies | Vorräte |
| fuel | Treibstoff |
| crew | Besatzung |
| marines | Marines |
| food | Nahrung |
| organics | Organika |
| volatiles | Volatile |
| ore / transplutonic ore | Erz / Transplutonisches Erz |
| rare ore | Seltenes Erz |
| metals / transplutonics | Metalle / Transplutonika |
| heavy machinery | Schwere Maschinen |
| domestic goods | Haushaltswaren |
| luxury goods | Luxusgüter |
| drugs | Drogen |
| organs | Organe |
| harvested organs | Geerntete Organe |
| hand weapons | Handfeuerwaffen |
| AI core | KI-Kern |

## Schiffe & Kampf
| Englisch | Deutsch |
|---|---|
| fleet | Flotte |
| frigate / destroyer / cruiser / capital ship | Fregatte / Zerstörer / Kreuzer / Großkampfschiff |
| battleship / battlecruiser | Schlachtschiff / Schlachtkreuzer |
| carrier / light carrier | Träger / Leichter Träger |
| freighter / tanker / transport / liner | Frachter / Tanker / Transporter / Linienschiff |
| fighter / bomber / interceptor | Jäger / Bomber / Abfangjäger |
| fighter wing | Jägergeschwader |
| drone | Drohne |
| station / battlestation / star fortress | Station / Kampfstation / Sternenfestung |
| hull | Rumpf |
| hullmod / hull modification | Rumpfmodifikation (kurz: Rumpfmod) |
| built-in / s-mod | eingebaut / S-Mod |
| ship system | Schiffssystem |
| armor | Panzerung |
| shield / omni shield / front shield | Schild / Omni-Schild / Frontschild |
| phase cloak / phase ship | Phasentarnung / Phasenschiff |
| flux / hard flux / soft flux | Flux / harter Flux / weicher Flux |
| flux vents / capacitors | Flux-Ventile / Flux-Kondensatoren |
| overload | Überlastung |
| venting | Ablassen (Flux ablassen) |
| ordnance points (OP) | Ausrüstungspunkte (OP) |
| combat readiness (CR) | Kampfbereitschaft (CR) |
| peak performance time | Spitzenleistungszeit |
| deployment points | Einsatzpunkte |
| burn level / max burn | Schubstufe / max. Schubstufe |
| sustained burn / emergency burn | Dauerschub / Notschub |
| go dark | Abtauchen |
| sensor profile / sensor strength | Sensorprofil / Sensorstärke |
| interdiction pulse | Abfangimpuls |
| active sensor burst | Aktiver Sensorstoß |
| weapon slot / mount | Waffenplatz / Halterung |
| small / medium / large | Klein / Mittel / Groß |
| ballistic / energy / missile | ballistisch / Energie / Rakete(n) |
| point defense (PD) | Punktverteidigung (PD) |
| kinetic / high explosive / fragmentation / energy damage | kinetischer / hochexplosiver / Splitter- / Energieschaden |
| EMP | EMP |
| beam | Strahl |
| torpedo | Torpedo |
| officer / captain / admiral / administrator | Offizier / Kapitän / Admiral / Administrator |
| skill / aptitude | Fertigkeit / Talent |
| elite | Elite |
| boarding | Entern |
| disengage / pursue / engage | sich absetzen / verfolgen / angreifen |
| retreat | Rückzug |
| (D) / d-mod | (D) / D-Mod (Defektmodifikation) |
| Low Tech / Midline / High Tech | Low-Tech / Midline / High-Tech (unverändert lassen in Herstellerfeldern) |

## Story-Begriffe (aus den Dialogpaketen - einheitlich verwenden)
| Englisch | Deutsch |
|---|---|
| Provost (Galatia Academy) | Rektor / Rektorin (z.B. "Rektorin Baird") |
| Academician | Akademiker / Akademikerin |
| Galatia Academy | Galatia-Akademie |
| commsplate | Sprechplatte |
| comms ID | Komm-ID |
| Fleet Intelligence (Service) | Flottengeheimdienst |
| Demarchon, Archon, Gens, Warlord, MuniSec, FleetSec | unverändert (Titel/Eigennamen) |
| Gargoyle (Hacker) | Gargoyle - duzt den Spieler, weiblich ("die Beste") |
| Knight(s) of Ludd | Ritter von Ludd |
| Tech / Sensors / Ops (Spitznamen der Brückenoffiziere) | Tech / Sensorik / Ops |
| Archcurate / Subcurate / Curate | Erzkurat(in) / Subkurat(in) / Kurat(in) |
| Knight Initiate / Novice | Ritteranwärter / Novize |
| Providence | die Vorsehung |
| Church of Galactic Redemption (CGR) | Kirche der Galaktischen Erlösung (CGR) |
| High Hegemon | Hoher Hegemon |
| Janus Device | Janus-Gerät |
| Gentes (Plural von Gens) | Gentes |
