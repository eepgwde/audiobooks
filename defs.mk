## weaves
# Common defines for the Makefile .mk files we have

# It's hard to get this from the Python config files.
# This package has 3 packages too.
-include pkg.def

H_FLAGS ?= -n -l -v

H_PROG ?= $(PYTHON) src/pitono/audio/_audlibroj.py

clean-local::
	$(RM) audiobooks.log

check-local:: clean-local
	$(H_PROG)	--tmp /var/tmp -o /a/l/SI-media/share/x-books/walser.m4b --files $(PKG_SRC)/tests/p1.lst --cover $(PKG_SRC)/tests/walser.jpg  $(H_FLAGS) -c "remove,write,cover,chapters"
