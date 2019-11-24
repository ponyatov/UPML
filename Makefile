
CWD = $(CURDIR)
MODULE = $(notdir $(CWD))

PY  = $(CWD)/bin/python3
PIP = $(CWD)/bin/pip3

run: $(PY) $(MODULE).py
	$^

doc: doc/wambook.pdf
doc/wambook.pdf:
	wget -c -O $@ http://wambook.sourceforge.net/wambook.pdf
