#!/usr/bin/make

##[ Variables ]################################################################

ODIR=../temp
FLAGS = --work=lib1 --workdir=$(ODIR)

##[ Rules ]####################################################################

vpath %.o $(ODIR)

%.o: %.vhdl
	ghdl -a $(FLAGS) $<

##[ Targets ]##################################################################

all: $(ODIR) com2_pkg1_lib1.o com1_pkg2_lib1.o

##[ Dependencies ]#############################################################

pkg1_lib1.o: com1_pkg1_lib1.vhdl com2_pkg1_lib1.vhdl com3_pkg1_lib1.vhdl
com1_pkg1_lib1.o com3_pkg1_lib1.o: pkg1_lib1.o
com2_pkg1_lib1.o: com1_pkg1_lib1.o

pkg2_lib1.o: com1_pkg2_lib1.vhdl
com1_pkg2_lib1.o: pkg2_lib1.o

##[ Extra targets ]############################################################

$(ODIR):
	mkdir -p $(ODIR)
	
clean:
	rm -fr $(ODIR)
