.DEFAULT_GOAL: all

SHELL := /bin/bash
PICA ?= pica

DUMPFILE = DNBGNDtitel.dat.gz
PARTITIONS = data/partitions
USERDIR = data/user
TEMPDIR = data/tmp
SCRIPTS = scripts

#
# PREPARE
#

.PHONY: prepare
prepare:
	@mkdir -p $(PARTITIONS) $(USERDIR) $(TEMPDIR)

#
# PARTITIONS
#

partitions: $(DUMPFILE)
	$(PICA) partition "002@.0" --skip-invalid $< -o $(PARTITIONS)

#
# USER DUMPS
#

USEROBJ := T.dat titel.dat gnd.dat

$(USERDIR)/T.dat: partitions
	$(PICA) cat $(PARTITIONS)/T*.dat -o $@

$(USERDIR)/gnd.dat: $(USERDIR)/T.dat
	$(PICA) filter "!008@.a? && 007K.a == 'gnd'" $< -o $@

$(USERDIR)/titel.dat: $(DUMPFILE)
	$(PICA) filter -s -v "002@.0 =^ 'T'" $< -o $@

#
# CSV DATA
#

USEROBJ += 041A_9.csv entity_types_stats.csv

$(USERDIR)/041A_9.csv: $(USERDIR)/titel.dat
	$(PICA) filter "041A/*.9?" $< -o $(TEMPDIR)/041A_9.dat
	$(PICA) select "003@.0,041A/*{9?, 9, 7, a}" $(TEMPDIR)/041A_9.dat \
		-H "idn,gnd_id,bbg,name" -o $@

$(USERDIR)/entity_types_stats.csv: $(USERDIR)/gnd.dat
	$(PICA) frequency "002@.0" $< -o $@


user: $(addprefix $(USERDIR)/,$(USEROBJ)) | prepare

#
# ALL
#

all: partitions user | prepare

#
# CLEAN
#

.PHONY: clean
clean:
	-rm -rf $(PARTITIONS) $(USERDIR) $(TEMPDIR)
