# GND Dashboard

Das Python Meetup der [DNB](https://dnb.de/) erstellt anlässlich der [GNDcon II](https://gnd.network/Webs/gnd/SharedDocs/Veranstaltungen/DE/GNDCon2_0/210607_gndCon2_0_node.html;jsessionid=BE0B31B0EB2494AFB8386584F91BF141.internet281) ein interaktives Dashboard.

## Abhängigkeiten

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandas](https://pandas.pydata.org/)
* [pica-rs](https://github.com/deutsche-nationalbibliothek/pica-rs)

## Erzeugung der Daten

Um die statistischen Auswertungen zu erstellen, wird ein aktueller Abzug der
Katalogdaten (in PICA+) benötigt. Diese Datei ist im Projektverzeichnis unter
`DNBGNDtitel.dat.gz` abzulegen.

Die Auswertungen werde wie folgt erzeugt:

```bash
$ make -j4 all
$ tree -L 1 data/
stats/
├── gnd_entity_count.csv
├── gnd_entity_types.csv
├── gnd_relation_count.csv
├── gnd_systematik.csv
├── title_gnd_links.csv
├── title_gnd_links_unique.csv
├── title_gnd_mean.csv
├── title_gnd_mean_Tb.csv
├── title_gnd_mean_Tf.csv
├── title_gnd_mean_Tg.csv
├── title_gnd_mean_Tp.csv
├── title_gnd_mean_Ts.csv
├── title_gnd_mean_Tu.csv
├── title_gnd_top10.csv
├── title_gnd_top10_Tb.csv
├── title_gnd_top10_Tf.csv
├── title_gnd_top10_Tg.csv
├── title_gnd_top10_Tp.csv
├── title_gnd_top10_Ts.csv
└── title_gnd_top10_Tu.csv

0 directories, 20 files
```

Alle erzeugten Artefakte können mit `make clean` gelöscht werden.

## Auswertungen

### Allgemein

* [gnd_entity_count.csv](stats/gnd_entity_count.csv) — Anzahl Entitäten in der GND
* [gnd_entity_types.csv](stats/gnd_entity_types.csv) — Verteilung Entitätentypen
* [gnd_releation_count.csv](stats/gnd_relation_count.csv) — Anzahl Relationen in der GND (Felder 028R, 029R, 030R, 022R, 041R, 065R)
* [gnd_classification_all.csv](stats/gnd_classification_all.csv) — Verteilung der GND-Systematik (Feld 042A.a)
* [gnd_classification_top10.csv](stats/gnd_classification_top10.csv) — Top10 GND-Systematik
* [gnd_codes_all.csv](stats/gnd_codes_all.csv) — Verteilung der Releation-Codes
* [gnd_codes_top10.csv](stats/gnd_codes_top10.csv) — Top10 Verteilung der Releation-Codes
* [title_gnd_links.csv](stats/title_gnd_links.csv) — Anzahl GND-Verknüpfungen in DNB-Titeldaten
* [title_gnd_links_unique.csv](stats/title_gnd_links_unique.csv) — Anzahl der verknüpften GND-Entitäten in DNB-Titeldaten
* [title_gnd_top10.csv](stats/title_gnd_top10.csv) — Top10 GND-Entitäten in den DNB-Titeldaten
* [title_gnd_mean.csv](stats/title_gnd_mean.csv) — Durchschnittliche Anzahl an GND-Verknüpfungen pro DNB-Titeldatensatz

### Nach Entitätstyp

* [title_gnd_top10_T{bfgpsu}.csv](stats/title_gnd_top10_Tp.csv) — Top10 GND-Entitäten in den DNB-Titeldaten (pro Entitätstyp)
* [title_gnd_mean_T{bfgpsu}.csv](stats/title_gnd_mean_Tp.csv) — Durchschnittliche Anzahl an GND-Verknüpfungen pro DNB-Titeldatensatz (pro Entitätstyp)
