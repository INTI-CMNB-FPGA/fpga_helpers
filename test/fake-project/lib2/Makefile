#!/usr/bin/make

##[ Variables ]################################################################

ODIR=../temp
FLAGS = --work=lib2 --workdir=$(ODIR)

##[ Rules ]####################################################################

vpath %.o $(ODIR)

%.o: %.vhdl
	ghdl -a $(FLAGS) $<

##[ Targets ]##################################################################

all: $(ODIR) com1_pkg1_lib2.o

##[ Dependencies ]#############################################################

pkg1_lib2.o: com1_pkg1_lib2.vhdl
com1_pkg1_lib2.o: pkg1_lib2.o

##[ Extra targets ]############################################################

$(ODIR):
	mkdir -p $(ODIR)
	
clean:
	rm -fr $(ODIR)
