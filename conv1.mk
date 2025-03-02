## weaves
# Test make file for PKG testing.
# Part of pitono. Used to build and test weaves

# Now to be used with conda

# To be run from the package directory. References files above.

# Local $(PWD) defs.mk may not be there
-include defs.mk
include ../defs.mk

S_IN ?= 

S_TAG ?= 0
S_BASE := $(TOP)/$(PKG_SRC)/tests/$(S_TAG)
S_OUT ?= $(S_BASE)/media

S_IMG ?= $(shell find $(S_IN) -maxdepth 1 -type f -iname '*.jp*g' -print | head -1)

J_ ?= $(TOP)/aud0

all::
	true

clean::
	true

$(S_BASE)/files.lst:
	find -L "$(S_IN)" -maxdepth 1 -type f -iname '*.mp3' -print > $@

ifeq ($(S_IMG),)
S_IMG += $(PKG_SRC)/tests/walser.jpg
endif


dirs-local::
	test -d "$(S_OUT)" || mkdir -p "$(S_OUT)"

all-sources-local: $(S_BASE)/files.lst
	( cd $(S_OUT); find . -type l -delete; parallel -a $< ln -s {} . )

all-data-local: dirs-local all-sources-local
	@echo S_IMG $(S_IMG)

$(S_BASE)/files.lst1: $(S_OUT)
	find $(S_OUT) -type l -print > $@

$(S_BASE)/files.lst2: $(S_BASE)/files.lst1
	cat $< | $(J_) -d $(S_OUT) ls counted > $@

all-relink-local: $(S_BASE)/files.lst1 $(S_BASE)/files.lst2
	parallel -a $(firstword $+) -a $(lastword $+) --link  mv {1} {2}

all-view-local: $(S_BASE)/files.lst $(S_BASE)/files.lst1 $(S_BASE)/files.lst2 

SFILES0 ?= $(wildcard $(S_OUT)/???-file.mp3)
SFILES1 ?= $(SFILES0:.mp3=.m4a)

$(S_OUT)/%.m4a: $(S_OUT)/%.mp3
	ffmpeg -y -i $< -c:a aac -b:a 128k -vn $@

#	ffmpeg -i $< -c:a libfdk_aac -vn $@


all-local: $(SFILES1)

N_J0 ?= -j4

ifeq ($(MAKECMDGOALS),target)

target: 
	@echo update: $(PWD)
	$(REMAKE) S_TAG=$(S_TAG) S_IN="$(S_IN)" all-data-local
	$(REMAKE) S_TAG=$(S_TAG) all-relink-local
	$(REMAKE) $(N_J0) S_TAG=$(S_TAG) all-local

endif

