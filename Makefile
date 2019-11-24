
CWD = $(CURDIR)
MODULE = $(notdir $(CWD))

PY  = $(CWD)/bin/python3
PIP = $(CWD)/bin/pip3

run: $(PY) $(MODULE).py
	$^