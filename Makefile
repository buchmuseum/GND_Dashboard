.DEFAULT_GOAL: all

SHELL := /bin/bash
PICA ?= pica

DUMPFILE = DNBGNDtitel.dat.gz
PARTITIONS = data/partitions
USERDIR = data/user
TEMPDIR = data/tmp
STATSDIR = stats
SCRIPTS = scripts

#
# PREPARE
#

.PHONY: prepare
prepare:
	@mkdir -p $(PARTITIONS) $(USERDIR) $(TEMPDIR) $(STATSDIR)

#
# PARTITIONS
#

partitions: $(DUMPFILE) | prepare
	$(PICA) partition "002@.0" --skip-invalid $< -o $(PARTITIONS)

#
# USER DUMPS
#

USEROBJ := T.dat titel.dat gnd.dat 041A_9.csv
USEROBJ += 022R.csv 028R.csv 029R.csv 030R.csv 041R.csv 065R.csv 0XXR.csv

user: $(addprefix $(USERDIR)/,$(USEROBJ)) | prepare

# $(USERDIR)/T.dat: partitions
$(USERDIR)/T.dat:
	$(PICA) cat $(PARTITIONS)/T*.dat -o $@

$(USERDIR)/gnd.dat: $(USERDIR)/T.dat
	$(PICA) filter "!008@.a? && 007K.a == 'gnd'" $< -o $@

$(USERDIR)/titel.dat: $(DUMPFILE)
	$(PICA) filter -s -v "002@.0 =^ 'T'" $< -o $@

$(USERDIR)/041A_9.csv: $(USERDIR)/titel.dat
	$(PICA) filter "041A/*.9?" $< -o $(TEMPDIR)/041A_9.dat
	$(PICA) select "003@.0,041A/*{9?, 9, 7, a}" $(TEMPDIR)/041A_9.dat \
		-H "idn,gnd_id,bbg,name" -o $@

$(USERDIR)/022R.csv: $(USERDIR)/gnd.dat
	$(PICA) filter "022R.9?" $< | $(PICA) select "003@.0,022R{9?, 9, 7, a, 4}" -H "idn,gnd_id,bbg,name,code" -o $@

$(USERDIR)/028R.csv: $(USERDIR)/gnd.dat
	$(PICA) filter "028R.9?" $< | $(PICA) select "003@.0,028R{9?, 9, 7, a, 4}" -H "idn,gnd_id,bbg,name,code" -o $@

$(USERDIR)/029R.csv: $(USERDIR)/gnd.dat
	$(PICA) filter "029R.9?" $< | $(PICA) select "003@.0,029R{9?, 9, 7, a, 4}" -H "idn,gnd_id,bbg,name,code" -o $@

$(USERDIR)/030R.csv: $(USERDIR)/gnd.dat
	$(PICA) filter "030R.9?" $< | $(PICA) select "003@.0,030R{9?, 9, 7, a, 4}" -H "idn,gnd_id,bbg,name,code" -o $@

$(USERDIR)/041R.csv: $(USERDIR)/gnd.dat
	$(PICA) filter "041R.9?" $< | $(PICA) select "003@.0,041R{9?, 9, 7, a, 4}" -H "idn,gnd_id,bbg,name,code" -o $@

$(USERDIR)/065R.csv: $(USERDIR)/gnd.dat
	$(PICA) filter "065R.9?" $< | $(PICA) select "003@.0,065R{9?, 9, 7, a, 4}" -H "idn,gnd_id,bbg,name,code" -o $@

$(USERDIR)/0XXR.csv: $(USERDIR)/022R.csv $(USERDIR)/028R.csv $(USERDIR)/029R.csv $(USERDIR)/030R.csv $(USERDIR)/041R.csv $(USERDIR)/065R.csv
	cat $^ > $@

#
# STATS
#

STATSOBJ := gnd_entity_types.csv gnd_entity_count.csv gnd_systematik.csv gnd_rel_count.csv
stats: $(addprefix $(STATSDIR)/,$(STATSOBJ)) title-analysis | prepare

$(STATSDIR)/gnd_entity_count.csv: $(USERDIR)/gnd.dat
	wc -l $< | cut -d" " -f1 > $@

$(STATSDIR)/gnd_entity_types.csv: $(USERDIR)/gnd.dat
	$(PICA) frequency "002@.0" $< -o $@

title-analysis: $(USERDIR)/041A_9.csv
	$(SCRIPTS)/title.py $<

$(STATSDIR)/gnd_systematik.csv: $(USERDIR)/gnd.dat
	$(PICA) frequency "042A.a" $< -o $@
	$(SCRIPTS)/gnd_systematik.py $@


$(STATSDIR)/gnd_rel_count.csv: $(USERDIR)/0XXR.csv
	wc -l $< | cut -d" " -f1 > $@

#
# ALL
#

all: user stats | prepare

#
# CLEAN
#

.PHONY: clean
clean:
	-rm -rf $(PARTITIONS) $(USERDIR) $(TEMPDIR) $(STATSDIR)
