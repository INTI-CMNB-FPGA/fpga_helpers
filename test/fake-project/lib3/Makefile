#!/usr/bin/make

##[ Variables ]################################################################

ODIR=../temp
FLAGS = --work=lib3 --workdir=$(ODIR)

##[ Rules ]####################################################################

vpath %.o $(ODIR)

%.o: %.vhdl
	ghdl -a $(FLAGS) $<

##[ Targets ]##################################################################

all: $(ODIR) com1_pkg1_lib3.o

##[ Dependencies ]#############################################################

pkg1_lib3.o: com1_pkg1_lib3.vhdl
com1_pkg1_lib3.o: pkg1_lib3.o

##[ Extra targets ]############################################################

$(ODIR):
	mkdir -p $(ODIR)
	
clean:
	rm -fr $(ODIR)
