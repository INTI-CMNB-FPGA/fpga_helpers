#!/bin/bash
#
# FPGA Setup, part of FPGA Helpers
# Copyright (C) 2016 INTI, Rodrigo A. Melo <rmelo@inti.gob.ar>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

if [ -f $HOME/.fpga_helpers ]; then
   source $HOME/.fpga_helpers
else # Default values
   # ISE
   ISE_64_BITS=1
   ISE_ROOT_DIR=/opt/Xilinx/ise
   # Vivado
   VIVADO_ROOT_DIR=/opt/Xilinx/vivado
   # Quartus2
   QUARTUS2_ROOT_DIR=/opt/Altera/quartus2
   # Libero-SoC
   LIBEROSOC_ROOT_DIR=/opt/Microsemi/Libero
   LIBEROSOC_LMGRD_DIR=/opt/Microsemi/Linux_Licensing_Daemon
   LIBEROSOC_LIC_FILE=/opt/Microsemi/License.dat
   LIBEROSOC_LIC_PORT=1702
   LIBEROSOC_LIC_HOST=localhost
   # Add here new tool code
fi

###############################################################################

OPTION=$1

HELP=0
CONFIG=0
SETTING=0

if [ $# -ne 1 ]; then
   SETTING=1
   echo "Select what TOOL Suite must be set:"
   echo "0. All the available"
   echo "1. ISE (Xilinx)"
   echo "2. Vivado (Xilinx)"
   echo "3. Quartus2 (Altera)"
   echo "4. Libero-SoC (Microsemi)"
   # Add here new tool code
   read -n 1 -s OPTION
   case "$OPTION" in
      0) OPTION="--all";;
      1) OPTION="--ise";;
      2) OPTION="--vivado";;
      3) OPTION="--quartus2";;
      4) OPTION="--libero-soc";;
      # Add here new tool code
      *) OPTION="--none";;
   esac
elif [ $OPTION == "--help" ]; then
   HELP=1
   echo "FPGA Setup Help:"
   echo "* All:"
   echo "  --config-all"
   echo "  --all"
elif [[ $OPTION =~ .*config.* ]]; then
   CONFIG=1
else
   SETTING=1
fi

###############################################################################
# ISE                                                                         #
###############################################################################

if [ $HELP -gt 0 ]; then
   echo "* ISE:"
   echo "  --config-ise"
   echo "  --ise"
fi
if [ $CONFIG -gt 0 ]; then
   if [ $OPTION == "--config-all" ] || [ $OPTION == "--config-ise" ]; then
      CONFIG=2
      echo "* Configure Xilinx ISE:"
      read -e -p "ISE ROOT DIR:                 " -i $ISE_ROOT_DIR ISE_ROOT_DIR
      read -e -p "ISE 64 BITS (0|1):            " -i $ISE_64_BITS  ISE_64_BITS
      until [ $ISE_64_BITS == 0 ] || [ $ISE_64_BITS == 1 ]
         do read -e -p "ISE 64 BITS (0|1):            " -i $ISE_64_BITS ISE_64_BITS; done
   fi
fi
if [ $SETTING -gt 0 ]; then
   if [ $OPTION == "--all" ] || [ $OPTION == "--ise" ]; then
      SETTING=2
      echo -n "* Setting Xilinx ISE... "
      if [ $ISE_64_BITS == 1 ]; then ISE_BITS=64; else ISE_BITS=; fi
      ISE_BIN_DIR=${ISE_ROOT_DIR}/ISE/bin/lin${ISE_BITS}
      export PATH=$PATH:$ISE_BIN_DIR
      echo "Done"
   fi
fi

###############################################################################
# Vivado                                                                      #
###############################################################################

if [ $HELP -gt 0 ]; then
   echo "* Vivado:"
   echo "  --config-vivado"
   echo "  --vivado"
fi
if [ $CONFIG -gt 0 ]; then
   if [ $OPTION == "--config-all" ] || [ $OPTION == "--config-vivado" ]; then
      CONFIG=2
      echo "* Configure Xilinx Vivado:"
      read -e -p "VIVADO ROOT DIR:              " -i $VIVADO_ROOT_DIR VIVADO_ROOT_DIR
   fi
fi
if [ $SETTING -gt 0 ]; then
   if [ $OPTION == "--all" ] || [ $OPTION == "--vivado" ]; then
      SETTING=2
      echo -n "* Setting Xilinx Vivado... "
      VIVADO_BIN_DIR=${VIVADO_ROOT_DIR}/bin
      export PATH=$PATH:$VIVADO_BIN_DIR
      echo "Done"
   fi
fi

###############################################################################
# Quartus2                                                                    #
###############################################################################

if [ $HELP -gt 0 ]; then
   echo "* Quartus2:"
   echo "  --config-quartus2"
   echo "  --quartus2"
fi
if [ $CONFIG -gt 0 ]; then
   if [ $OPTION == "--config-all" ] || [ $OPTION == "--config-quartus2" ]; then
      CONFIG=2
      echo "* Configure Altera Quartus2:"
      read -e -p "QUARTUS2 ROOT DIR:            " -i $QUARTUS2_ROOT_DIR QUARTUS2_ROOT_DIR
   fi
fi
if [ $SETTING -gt 0 ]; then
   if [ $OPTION == "--all" ] || [ $OPTION == "--quartus2" ]; then
      SETTING=2
      echo -n "* Setting Altera Quartus2... "
      QUARTUS2_BIN_DIR=${QUARTUS2_ROOT_DIR}/quartus/bin
      export PATH=$PATH:$QUARTUS2_BIN_DIR
      echo "Done"
   fi
fi

###############################################################################
# Libero-SoC                                                                  #
###############################################################################

if [ $HELP -gt 0 ]; then
   echo "* Libero-SoC:"
   echo "  --config-libero-soc"
   echo "  --libero-soc"
fi
if [ $CONFIG -gt 0 ]; then
   if [ $OPTION == "--config-all" ] || [ $OPTION == "--config-libero-soc" ]; then
      CONFIG=2
      echo "* Configure Microsemi Libero-Soc:"
      read -e -p "LIBERO SOC ROOT DIR:          " -i $LIBEROSOC_ROOT_DIR  LIBEROSOC_ROOT_DIR
      read -e -p "LIBERO SOC LICENSE PORT:      " -i $LIBEROSOC_LIC_PORT  LIBEROSOC_LIC_PORT
      read -e -p "LIBERO SOC LICENSE HOST:      " -i $LIBEROSOC_LIC_HOST  LIBEROSOC_LIC_HOST
      if [ $LIBEROSOC_LIC_HOST == "localhost" ]; then
         read -e -p "LIBERO SOC LICENSE FILE:      " -i $LIBEROSOC_LIC_FILE  LIBEROSOC_LIC_FILE
         read -e -p "LIBERO SOC LMGRD DIR:         " -i $LIBEROSOC_LMGRD_DIR LIBEROSOC_LMGRD_DIR
      fi
   fi
fi
if [ $SETTING -gt 0 ]; then
   if [ $OPTION == "--all" ] || [ $OPTION == "--libero-soc" ]; then
      SETTING=2
      echo -n "* Setting Microsemi Libero-SoC... "
      LIBEROSOC_BIN_DIR=${LIBEROSOC_ROOT_DIR}/Libero/bin
      export PATH=$PATH:$LIBEROSOC_BIN_DIR
      export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu
      export LM_LICENSE_FILE=$LIBEROSOC_LIC_PORT@$LIBEROSOC_LIC_HOST
      if [ $LIBEROSOC_LIC_HOST == "localhost" ]; then
         if [ -z `pidof lmgrd` ]; then
            echo -n "Launcingh Microsemi License manager... "
            $LIBEROSOC_LMGRD_DIR/lmgrd -c $LIBEROSOC_LIC_FILE -l /tmp/libero-soc-license.log
         else
            echo -n "Microsemi License manager is already running... "
         fi
      fi
      echo "Done"
   fi
fi

###############################################################################
# Add here new tool code                                                      #
###############################################################################
# Add here new tool code

###############################################################################

if [ $CONFIG -eq 1 ] || [ $SETTING -eq 1 ]; then
   echo "ERROR: unsupported option. "
   echo "Use --help to see a list of supported options."
fi

if [ $CONFIG -eq 2 ]; then
   echo "# FPGA Helpers Configuration file"        >  $HOME/.fpga_helpers
   echo "ISE_64_BITS=$ISE_64_BITS"                 >> $HOME/.fpga_helpers
   echo "ISE_ROOT_DIR=$ISE_ROOT_DIR"               >> $HOME/.fpga_helpers
   echo "VIVADO_ROOT_DIR=$VIVADO_ROOT_DIR"         >> $HOME/.fpga_helpers
   echo "QUARTUS2_ROOT_DIR=$QUARTUS2_ROOT_DIR"     >> $HOME/.fpga_helpers
   echo "LIBEROSOC_ROOT_DIR=$LIBEROSOC_ROOT_DIR"   >> $HOME/.fpga_helpers
   echo "LIBEROSOC_LMGRD_DIR=$LIBEROSOC_LMGRD_DIR" >> $HOME/.fpga_helpers
   echo "LIBEROSOC_LIC_FILE=$LIBEROSOC_LIC_FILE"   >> $HOME/.fpga_helpers
   echo "LIBEROSOC_LIC_PORT=$LIBEROSOC_LIC_PORT"   >> $HOME/.fpga_helpers
   echo "LIBEROSOC_LIC_HOST=$LIBEROSOC_LIC_HOST"   >> $HOME/.fpga_helpers
   # Add here new tool code
fi

if [ $SETTING -eq 2 ]; then
   echo "You are entering in a new SHELL with settings applied."
   $SHELL
fi
