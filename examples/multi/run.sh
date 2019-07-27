#!/bin/sh
mkdir -p temp
echo "################################################ Checking ISE"
make TOOL=ise run > ise_output
echo "################################################ Checking Vivado"
make TOOL=vivado run > vivado_output
echo "################################################ Checking Quartus"
make TOOL=quartus run > quartus_output
echo "################################################ Checking Libero"
make TOOL=libero run > libero_output
echo "################################################ Deleting generated files"
rm -fr temp
make clean-multi
echo "################################################ Done"
