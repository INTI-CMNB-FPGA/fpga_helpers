#!/usr/bin/make

##[ Variables ]################################################################

ODIR=../temp
FLAGS = -P$(ODIR) --workdir=$(ODIR)

##[ Rules ]####################################################################

vpath %.o $(ODIR)
vpath %.vhdl FPGA

%.o: %.vhdl
	ghdl -a $(FLAGS) $<

##[ Targets ]##################################################################

all: $(ODIR) top.o

##[ Dependencies ]#############################################################

top.o: core.o

core.o: com2_pkg1_lib1.o com1_pkg1_lib2.o

com2_pkg1_lib1.o:
	make -C ../lib1

com1_pkg1_lib2.o:
	make -C ../lib2

##[ Extra targets ]############################################################

$(ODIR):
	mkdir -p $(ODIR)
	
clean:
	rm -fr $(ODIR)
