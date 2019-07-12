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
###############################################################################

if [ -f $HOME/.fpga_helpers ]; then
   source $HOME/.fpga_helpers
else # Default values
   # ISE
   ISE_64_BITS=1
   ISE_ROOT_DIR=/opt/Xilinx/ise
   # Vivado
   VIVADO_ROOT_DIR=/opt/Xilinx/vivado
   # Quartus
   QUARTUS_ROOT_DIR=/opt/Altera/quartus
   # Libero
   LIBERO_ROOT_DIR=/opt/Microsemi/Libero
   LIBERO_LMGRD_DIR=/opt/Microsemi/Linux_Licensing_Daemon
   LIBERO_LIC_FILE=/opt/Microsemi/License.dat
   LIBERO_LIC_PORT=1702
   LIBERO_LIC_HOST=localhost
   # Add here new tool code
fi

###############################################################################

if [ $# -eq 0 ] || [ $1 == "--quit" ]; then # running interactively
   echo "c. configurations related with vendors tools"
   echo "0. set to use all the available vendors tools"
   echo "1. set to use ISE (Xilinx)"
   echo "2. set to use Vivado (Xilinx)"
   echo "3. set to use Quartus (Altera)"
   echo "4. set to use Libero (Microsemi)"
   # Add here new tool code
   echo "q. quit"
   if [ $# -eq 0 ]; then
      read -n 1 -s OPTION
      case "$OPTION" in
         c)
            CONFIG=1;;
         0)
            ISE=1
            VIVADO=1
            QUARTUS=1
            LIBERO=1;;
         1)
            ISE=1;;
         2)
            VIVADO=1;;
         3)
            QUARTUS=1;;
         4)
            LIBERO=1;;
         # Add here new tool code
         q) ;;
         *)
            echo "fpga_setup (ERROR): '$OPTION' is not a valid option."
            HELP=1
      esac
   fi
elif [ $# -eq 1 ]; then # running with a option
   OPTION=$1
   if [ $OPTION == "--help" ]; then
      HELP=1
   elif [ $OPTION == "--config" ]; then
      CONFIG=1
   elif [ $OPTION == "--all" ]; then
      ISE=1
      VIVADO=1
      QUARTUS=1
      LIBERO=1
   elif [ $OPTION == "--ise" ]; then
      ISE=1
   elif [ $OPTION == "--vivado" ]; then
      VIVADO=1
   elif [ $OPTION == "--quartus" ]; then
      QUARTUS=1
   elif [ $OPTION == "--libero" ]; then
      LIBERO=1
   # Add here new tool code
   else
      echo "fpga_setup (ERROR): '$OPTION' is not a valid option."
      HELP=1
   fi
else # running with more than a option
   echo "fpga_setup (ERROR): too many parameters."
   HELP=1
fi

if [[ $HELP ]]; then
   echo "FPGA Setup Help:"
   echo "* Execute fpga_setup without arguments to run interactively."
   echo "* Available options when run with arguments (choose only one):"
   echo "--config     : configurations related with vendors tools"
   echo "--all        : set to use all the available vendors tools"
   echo "--ise        : set to use ISE (Xilinx)"
   echo "--vivado     : set to use Vivado (Xilinx)"
   echo "--quartus    : set to use Quartus (Altera)"
   echo "--libero     : set to use Libero (Microsemi)"
   # Add here new tool code
fi

if [[ $CONFIG ]]; then
   echo "fpga_setup (INFO): you can use 'tab' to autocomplete options for paths and files"
fi

###############################################################################
# ISE                                                                         #
###############################################################################

if [[ $CONFIG ]]; then
   echo "* Configure Xilinx ISE:"
   read -e -p "ISE ROOT DIR:                 " -i $ISE_ROOT_DIR ISE_ROOT_DIR
   read -e -p "ISE 64 BITS (0|1):            " -i $ISE_64_BITS  ISE_64_BITS
   until [ $ISE_64_BITS == 0 ] || [ $ISE_64_BITS == 1 ]
      do read -e -p "ISE 64 BITS (0|1):            " -i $ISE_64_BITS ISE_64_BITS; done
fi
if [[ $ISE ]]; then
   echo -n "* Setting Xilinx ISE... "
   if [ $ISE_64_BITS == 1 ]; then ISE_BITS=64; else ISE_BITS=; fi
   ISE_BIN_DIR=${ISE_ROOT_DIR}/ISE/bin/lin${ISE_BITS}
   export PATH=$PATH:$ISE_BIN_DIR
   echo "Done"
   SET=1
fi

###############################################################################
# Vivado                                                                      #
###############################################################################

if [[ $CONFIG ]]; then
   echo "* Configure Xilinx Vivado:"
   read -e -p "VIVADO ROOT DIR:              " -i $VIVADO_ROOT_DIR VIVADO_ROOT_DIR
fi
if [[ $VIVADO ]]; then
   echo -n "* Setting Xilinx Vivado... "
   VIVADO_BIN_DIR=${VIVADO_ROOT_DIR}/bin
   export PATH=$PATH:$VIVADO_BIN_DIR
   echo "Done"
   SET=1
fi

###############################################################################
# Quartus                                                                     #
###############################################################################

if [[ $CONFIG ]]; then
   echo "* Configure Altera Quartus:"
   read -e -p "QUARTUS ROOT DIR:             " -i $QUARTUS_ROOT_DIR QUARTUS_ROOT_DIR
fi
if [[ $QUARTUS ]]; then
   echo -n "* Setting Altera Quartus... "
   QUARTUS_BIN_DIR=${QUARTUS_ROOT_DIR}/quartus/bin
   export PATH=$PATH:$QUARTUS_BIN_DIR
   echo "Done"
   SET=1
fi

###############################################################################
# Libero                                                                  #
###############################################################################

if [[ $CONFIG ]]; then
   echo "* Configure Microsemi Libero:"
   read -e -p "LIBERO ROOT DIR:              " -i $LIBERO_ROOT_DIR  LIBERO_ROOT_DIR
   read -e -p "LIBERO LICENSE PORT:          " -i $LIBERO_LIC_PORT  LIBERO_LIC_PORT
   read -e -p "LIBERO LICENSE HOST:          " -i $LIBERO_LIC_HOST  LIBERO_LIC_HOST
   if [ $LIBERO_LIC_HOST == "localhost" ]; then
      read -e -p "LIBERO LICENSE FILE:          " -i $LIBERO_LIC_FILE  LIBERO_LIC_FILE
      read -e -p "LIBERO LMGRD DIR:             " -i $LIBERO_LMGRD_DIR LIBERO_LMGRD_DIR
   fi
fi
if [[ $LIBERO ]]; then
   echo -n "* Setting Microsemi Libero... "
   LIBERO_BIN_DIR=${LIBERO_ROOT_DIR}/Libero/bin
   export PATH=$PATH:$LIBERO_BIN_DIR
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu
   export LM_LICENSE_FILE=$LIBERO_LIC_PORT@$LIBERO_LIC_HOST
   if [ $LIBERO_LIC_HOST == "localhost" ]; then
      if [ -z `pidof lmgrd` ]; then
         echo -n "Launcingh Microsemi License manager... "
         $LIBERO_LMGRD_DIR/lmgrd -c $LIBERO_LIC_FILE -l /tmp/libero-license.log
      else
         echo -n "Microsemi License manager is already running... "
      fi
   fi
   echo "Done"
   SET=1
fi

###############################################################################
# Add here new tool name                                                      #
###############################################################################
# Add here new tool code
###############################################################################

if [[ $CONFIG ]]; then
   echo "# FPGA Helpers Configuration file"        >  $HOME/.fpga_helpers
   echo "ISE_64_BITS=$ISE_64_BITS"                 >> $HOME/.fpga_helpers
   echo "ISE_ROOT_DIR=$ISE_ROOT_DIR"               >> $HOME/.fpga_helpers
   echo "VIVADO_ROOT_DIR=$VIVADO_ROOT_DIR"         >> $HOME/.fpga_helpers
   echo "QUARTUS_ROOT_DIR=$QUARTUS_ROOT_DIR"       >> $HOME/.fpga_helpers
   echo "LIBERO_ROOT_DIR=$LIBERO_ROOT_DIR"         >> $HOME/.fpga_helpers
   echo "LIBERO_LMGRD_DIR=$LIBERO_LMGRD_DIR"       >> $HOME/.fpga_helpers
   echo "LIBERO_LIC_FILE=$LIBERO_LIC_FILE"         >> $HOME/.fpga_helpers
   echo "LIBERO_LIC_PORT=$LIBERO_LIC_PORT"         >> $HOME/.fpga_helpers
   echo "LIBERO_LIC_HOST=$LIBERO_LIC_HOST"         >> $HOME/.fpga_helpers
   echo "Configurations saved in $HOME/.fpga_helpers"
   # Add here new tool code
fi

if [[ $SET ]]; then
   echo "fpga_setup (INFO): You are entering in a new SHELL with settings applied."
   $SHELL
fi
