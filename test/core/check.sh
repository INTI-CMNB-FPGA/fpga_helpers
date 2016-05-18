#!/bin/sh
mkdir -p temp
echo "Checking core_file.vhdl"
ghdl -a --work=LIB_NAME --workdir=temp core_file.vhdl
echo "Checking package_file.vhdl"
ghdl -a --work=LIB_NAME --workdir=temp package_file.vhdl
echo "Checking top_file.vhdl"
ghdl -a -Ptemp          --workdir=temp top_file.vhdl
echo "Done"
rm -fr temp
