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

