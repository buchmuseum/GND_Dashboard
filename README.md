# GND Dashboard

Das Python Meetup der [DNB](https://dnb.de/) erstellt anlässlich der [GNDcon II](https://gnd.network/Webs/gnd/SharedDocs/Veranstaltungen/DE/GNDCon2_0/210607_gndCon2_0_node.html;jsessionid=BE0B31B0EB2494AFB8386584F91BF141.internet281) ein interaktives Dashboard.

## Abhängigkeiten

* [GNU Make](https://www.gnu.org/software/make/)
* [pica-rs](https://github.com/deutsche-nationalbibliothek/pica-rs)

## Erzeugung der Daten

Um die statistischen Auswertungen zu erstellen, wird ein aktueller Abzug der
Katalogdaten (in PICA+) benötigt. Diese Datei ist im Projektverzeichnis unter
`DNBGNDtitel.dat.gz` abzulegen.

Die Auswertungen werde wie folgt erzeugt:

```bash
$ make -j4 all
$ tree -L 1 data/
data/
├── partitions
├── pica
├── tmp
└── user

4 directories, 0 files
```

Alle erzeugten Artefakte können mit `make clean` gelöscht werden.

## Auswertungen

## Allgemein

* [gnd_entity_count.csv](stats/gnd_entity_count.csv) — Anzahl Entitäten in der GND
* [gnd_entity_types.csv](stats/gnd_entity_types.csv) — Verteilung Entitätentypen
* [title_gnd_links.csv](stats/title_gnd_links.csv) — Anzahl GND-Verknüpfungen in DNB-Titeldaten
* [title_gnd_links_unique.csv](stats/title_gnd_links_unique.csv) — Anzahl der verknüpften GND-Entitäten in DNB-Titeldaten
* [title_gnd_top10.csv](stats/title_gnd_top10.csv) — Top10 GND-Entitäten in den DNB-Titeldaten

## Entitätstypen

* ..

## Alt

| Datei                            | Bemerkung                                           |
| -------------------------------- | --------------------------------------------------- |
| `stats/gnd_mean.csv`             | Durschnittl. Anzahl verknüpfter Entitäten           |
| `stats/T[bfgpsu]_top10.csv`      | Top-10 verknüpfte Entitäten (pro Typ)               |
| `stats/T[bfgpsu]_mean.csv`       | Durschnittl. Anzahl verknüpfter Entitäten (pro Typ) |
| `stats/gnd_systematik_top10.csv` | Top-10 GND-Systematik-Nummern                       |
| `stats/gnd_rel_count.csv`        | Anzahl der Relationen innerhalb der GND             |
