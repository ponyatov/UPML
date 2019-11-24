
CWD = $(CURDIR)
MODULE = $(notdir $(CWD))

PY  = $(CWD)/bin/python3
PIP = $(CWD)/bin/pip3

run: $(PY) $(MODULE).py $(MODULE).ini
	$^

doc: doc/wambook.pdf
doc/wambook.pdf:
	wget -c -O $@ http://wambook.sourceforge.net/wambook.pdf

update: 
	git pull -v
	$(PIP) install -U    pip
	$(PIP) install -U -r requirements.txt
	$(MAKE) requirements.txt

.PHONY: requirements.txt
requirements.txt:
	$(PIP) freeze | egrep -v "(terminado|0.0.0)" > $@

