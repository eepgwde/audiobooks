## weaves
# Test make file for MInfo.py module testing.

PYTHON ?= python3
UUT ?= 
PKG ?= audiobooks
X_LOGFILE ?= $(PKG).log
SDIR ?= tests/media
PYTHONIOENCODING=utf-8

export SDIR
export X_LOGFILE

all::
	true

ifneq ($(UUT),)

check::
	:> $(X_LOGFILE)
	$(PYTHON) -m unittest -v tests.$(UUT)

else

check::
	:> $(X_LOGFILE)
	$(PYTHON) -m unittest discover -v -s tests

endif 

clean::
	$(RM) $(wildcard *.pyc *.log *~ nohup.out)

distclean::
	$(RM) -rf html
	$(RM) $(wildcard *.json)

## Install

.PHONY: uninstall dist-local

uninstall::
	rm -f $(wildcard dist/*.tar.gz)
	-$(shell -c "cd $(HOME)/.local; -pip3 uninstall --yes $(PKG)")

dist-local:
	python setup.py sdist

install: uninstall dist-local
	pip3 install $(wildcard dist/*.tar.gz) --user
