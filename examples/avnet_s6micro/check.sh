#!/bin/sh
echo "################################################ Checking cores with ghdl"
mkdir -p temp
ghdl -a --work=examples --workdir=temp ../hdl/blinking.vhdl
ghdl -a --work=examples --workdir=temp ../hdl/examples_pkg.vhdl
ghdl -a -Ptemp          --workdir=temp top.vhdl
echo "################################################ Done"

echo "################################################ Checking ISE"
make TOOL=ise run

echo "################################################ Done"
