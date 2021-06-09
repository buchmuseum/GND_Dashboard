.DEFAULT_GOAL: all

SHELL := /bin/bash
PICA ?= pica

DUMPFILE = DNBGNDtitel.dat.gz
USERDIR = data/user
STATSDIR = stats
SCRIPTS = scripts

#
# PREPARE
#

.PHONY: prepare
prepare:
	@mkdir -p $(USERDIR) $(STATSDIR)

#
# USER DUMPS
#

TITLE_LINK_OBJS :=
TITLE_LINK_OBJS += 022A_9.csv # In Manifestation verkörpertes Werk
TITLE_LINK_OBJS += 028A_9.csv # Person, Familie - 1. geistiger Schöpfer
TITLE_LINK_OBJS += 028C_9.csv # Person, Familie - weitere geistige Schöpfer, ..
TITLE_LINK_OBJS += 029A_9.csv # Körperschaft, Konferenz - 1. geistiger Schöpfer
TITLE_LINK_OBJS += 029F_9.csv # Körperschaft, Konferenz - weitere geistige Schöpfer,...
TITLE_LINK_OBJS += 032X_9.csv # Besetzung
TITLE_LINK_OBJS += 033A_9.csv # Veröffentlichungsangabe
TITLE_LINK_OBJS += 033D_9.csv # Verlagsort, Verlag in Ansetzungsform (DMA)
TITLE_LINK_OBJS += 033E_9.csv # Vertriebsangabe
TITLE_LINK_OBJS += 033H_9.csv # Verbreitungsort in normierter Form
TITLE_LINK_OBJS += 039B_9.csv # Beziehung zu einer größeren Einheit
TITLE_LINK_OBJS += 039C_9.csv # Beziehung zu einer kleineren Einheit
TITLE_LINK_OBJS += 039D_9.csv # Beziehung auf Manifestationsebene - außer Reproduktionen
TITLE_LINK_OBJS += 039E_9.csv # Vorgänger-Nachfolger-Beziehung auf Werkebene
TITLE_LINK_OBJS += 039H_9.csv # Reproduktion - gleiche physische Form
TITLE_LINK_OBJS += 039I_9.csv # Reproduktion - andere physische Form
TITLE_LINK_OBJS += 039S_9.csv # Teil-Ganzes-Beziehung auf Werkebene
TITLE_LINK_OBJS += 039T_9.csv # Verknüpfung zum rezensierten Werk
TITLE_LINK_OBJS += 039U_9.csv # Verknüpfung zur Rezension
TITLE_LINK_OBJS += 039V_9.csv # Chronologische Verknüpfung / Vorgänger
TITLE_LINK_OBJS += 039W_9.csv # Chronologische Verknüpfung / Nachfolger
TITLE_LINK_OBJS += 039X_9.csv # Beziehung auf Expressionsebene
TITLE_LINK_OBJS += 039Y_9.csv # Verknüpfung zu weiteren Bezugswerken, Quellennachweis
TITLE_LINK_OBJS += 039Z_9.csv # Andere Beziehung auf Werk- und Expressionsebene...
TITLE_LINK_OBJS += 041A_9.csv # Schlagwortfolgen gemäß RSWK
TITLE_LINK_OBJS += 044G_9.csv # Literarische Gattung
TITLE_LINK_OBJS += 044P_9.csv # Gestaltungsmerkmale auf bibliografischer Ebene

GND_LINK_OBJS := 022R.csv 028R.csv 029R.csv 030R.csv 041R.csv 065R.csv

USEROBJ := titel.dat gnd.dat gnd.csv
USEROBJ += 0XXR.csv 0XXX_9.csv 044H_9.csv 044K_9.csv Tu_names.csv

user: $(addprefix $(USERDIR)/,$(USEROBJ)) | prepare

$(USERDIR)/gnd.dat: $(DUMPFILE) | prepare
	$(PICA) filter -s "002@.0 =^ 'T' && !008@.a? && 007K.a == 'gnd'" $< -o $@

$(USERDIR)/titel.dat: $(DUMPFILE) | prepare
	$(PICA) filter -s -v "002@.0 =^ 'T'" $< -o $@

$(USERDIR)/gnd.csv: $(USERDIR)/gnd.dat
	$(PICA) select "003@.0,002@.0,001A.0,003U.a" -H "gnd_id,bbg,ser,uri" $< -o $@

$(USERDIR)/Tu_names.csv: $(USERDIR)/gnd.dat
	$(PICA) filter "002@.0 =^ 'Tu' && 022A.a?" $< | $(PICA) select "003@.0,022A.a" -H "gnd_id,name2" -o $@

$(USERDIR)/022A_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "022A/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,022A/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/028A_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "028A/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,028A/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/028C_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "028C/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,028C/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/029A_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "029A/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,029A/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/029F_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "029F/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,029F/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/032X_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "032X/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,032X/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/033A_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "033A/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,033A/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/033D_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "033D/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,033D/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/033E_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "033E/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,033E/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/033H_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "033H/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,033H/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039B_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039B/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039B/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039C_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039C/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039C/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039D_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039D/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039D/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039E_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039E/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039E/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039H_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039H/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039H/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039I_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039I/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039I/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039S_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039S/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039S/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039T_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039T/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039T/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039U_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039U/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039U/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039V_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039V/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039V/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039W_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039W/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039W/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039X_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039X/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039X/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039Y_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039Y/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039Y/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/039Z_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "039Z/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,039Z/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/041A_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "041A/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,041A/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/044G_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "044G/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,044G/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/044P_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "044P/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,044P/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/044H_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "044H/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,044H/*{9? && 7 =^ 'T',9,a}" -o $@
$(USERDIR)/044K_9.csv: $(USERDIR)/titel.dat; $(PICA) filter "044K/*{9? && 7 =^ 'T'}" $< | $(PICA) select "003@.0,044K/*{9? && 7 =^ 'T',9,a}" -o $@

$(USERDIR)/0XXX_9.csv: $(addprefix $(USERDIR)/,$(TITLE_LINK_OBJS))
	cat $^ > $@

$(USERDIR)/022R.csv: $(USERDIR)/gnd.dat ; $(PICA) filter "022R.9?" $< | $(PICA) select "003@.0,022R{9?, 9, a, 4}" -o $@
$(USERDIR)/028R.csv: $(USERDIR)/gnd.dat ; $(PICA) filter "028R.9?" $< | $(PICA) select "003@.0,028R{9?, 9, a, 4}" -o $@
$(USERDIR)/029R.csv: $(USERDIR)/gnd.dat ; $(PICA) filter "029R.9?" $< | $(PICA) select "003@.0,029R{9?, 9, a, 4}" -o $@
$(USERDIR)/030R.csv: $(USERDIR)/gnd.dat ; $(PICA) filter "030R.9?" $< | $(PICA) select "003@.0,030R{9?, 9, a, 4}" -o $@
$(USERDIR)/041R.csv: $(USERDIR)/gnd.dat ; $(PICA) filter "041R.9?" $< | $(PICA) select "003@.0,041R{9?, 9, a, 4}" -o $@
$(USERDIR)/065R.csv: $(USERDIR)/gnd.dat ; $(PICA) filter "065R.9?" $< | $(PICA) select "003@.0,065R{9?, 9, a, 4}" -o $@

$(USERDIR)/0XXR.csv: $(addprefix $(USERDIR)/,$(GND_LINK_OBJS))
	cat $^ > $@

#
# STATS
#

STATSOBJ := gnd_entity_types.csv gnd_entity_count.csv gnd_systematik.csv
STATSOBJ += gnd_relation_count.csv title_count.csv

stats: $(addprefix $(STATSDIR)/,$(STATSOBJ)) title-analysis gnd-analysis | prepare

$(STATSDIR)/gnd_entity_count.csv: $(USERDIR)/gnd.dat
	wc -l $< | cut -d" " -f1 > $@

$(STATSDIR)/title_count.csv: $(USERDIR)/titel.dat
	wc -l $< | cut -d" " -f1 > $@

$(STATSDIR)/gnd_relation_count.csv: $(USERDIR)/0XXR.csv
	wc -l $< | cut -d" " -f1 > $@

$(STATSDIR)/gnd_entity_types.csv: $(USERDIR)/gnd.dat
	$(PICA) frequency "002@.0" $< -o $@

title-analysis: $(USERDIR)/0XXX_9.csv $(USERDIR)/044H_9.csv $(USERDIR)/044K_9.csv $(USERDIR)/gnd.csv $(STATSDIR)/title_count.csv $(USERDIR)/Tu_names.csv
	$(SCRIPTS)/title.py

$(STATSDIR)/gnd_systematik.csv: $(USERDIR)/gnd.dat
	$(PICA) frequency "042A.a" $< -o $@

$(STATSDIR)/gnd_systematik_Ts.csv: $(USERDIR)/gnd.dat
	$(PICA) filter "002@.0 =^ 'Ts'" $< | $(PICA) frequency "042A.a" -o $@

gnd-analysis: $(USERDIR)/0XXR.csv $(STATSDIR)/gnd_systematik.csv $(STATSDIR)/gnd_systematik_Ts.csv
	$(SCRIPTS)/gnd.py


#
# ALL
#

all: user stats | prepare

#
# CLEAN
#

.PHONY: clean
clean:
	-rm -rf $(USERDIR) $(STATSDIR)
