## weaves
# Test make file for MInfo.py module testing.

PKG := $(notdir $(PWD))

PYTHON ?= python3
UUT ?= 
X_LOGFILE ?= test.log
SDIR ?= tests/media
PYTHONIOENCODING=utf-8
PYTEST ?= pytest
RLWRAP ?= rlwrap
TEST_FLAGS ?= -f
TOP ?= $(PWD)

PYTHONPATH=.:$(TOP)/tests:/usr/lib/python3/dist-packages
export PYTHONPATH

export SDIR
export X_LOGFILE

all::
	true

TEST_FLAGS ?= -v -c 

ifeq ($(PYTEST),unittest)
DISCOVER0 := discover
TEST_FLAGS += -f
RLWRAP ?= rlwrap
endif


ifneq ($(UUT),)

check::
	:> $(X_LOGFILE)
	$(RLWRAP) $(PYTHON) -m $(PYTEST) $(TEST_FLAGS) -v tests.$(UUT) 2>&1 | tee make.log

else

check::
	:> $(X_LOGFILE)
	$(PYTHON) -m $(PYTEST) $(DISCOVER0) tests 2>&1 | tee make.log

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
	-$(SHELL) -c "cd $(HOME)/.local; pip3 uninstall --yes $(PKG)"

dist-local:
	python setup.py sdist

install: uninstall dist-local
	pip3 install --no-deps -e . --user

clean::
	-$(SHELL) -c "find . -type d -name __pycache__ -exec rm -rf {} \;"
	-$(SHELL) -c "find . -type f -name '*.log' -delete "
	-$(SHELL) -c "find . -type f -name '*~' -delete "
	-$(SHELL) -c "find . -type d -name '*egg*' -exec rm -rf {} \; "
	rm -f $(wildcard dist/*)
	rm -f ChangeLog AUTHORS

