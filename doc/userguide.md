# Introduction

FPGA Helpers are a set of **Tcl** (*Tool Command Language*) and **Python** CLI
(*Command-line Interfaces*) scripts, which helps to use the FPGA development
tools from the command line in a *vendor independent* way.

Two **Tcl** scripts and one *Makefile* solves the support of multiple tools:
* *synthesis.tcl:* solves Synthesis, Implementation and Bitstream Generation.
* *programming.tcl:* solves programming of FPGAs and/or memories.
* *Makefile:* run the needed script with the adequate interpreter.
* *options.tcl [generated]:* project options file, where to indicate the used FPGA, files,
memories parameters and particular options of the tool.

> Implementation involve optimizations, technological mapping, *place & route* (P&R)
> and *static timing analysis* (STA).

> The *Makefile* assumes that the tool to be executed is well installed, has a valid
> license configured and is included in the system path.

The **Python** CLIs helps to use the **Tcl**, either by incorporating them into the project
(in which case they become part of it) or by executing them for specific tasks:
* *fpga_setup (Linux only):* prepare the system to run the vendor tools.
* *fpga_wizard:* generates the project files (*options.tcl* and an auxiliar *Makefile*).
* *fpga_synt*: run synthesis based on a project file generated with a vendor tool.
* *fpga_prog:* transfer a bitstream to a FPGA or memory.
* *fpga_deps [WIP]:* collects automatically HDL files which are part of a project.

> The **Python** scripts are never part of the project files. For convenience and
> ease of use is recommended to be installed, but can be used standalone.

> The **Tcl** files can be used without the use of the **Python** scripts,
> creating manually the project files.

# Installation

Run in the root directory of FPGA Helpers (where is `setup.py`):
* Python3: `pip3 install .`
* Python2: `pip install .`

> If `pip3` is not installed, you need `python3-pip` (or `python-pip` for `pip`).

> FPGA Helpers can also be used standalone (without installation).

# Tcl

Considerations:
* The **Tcl** scripts can be included in a project in different ways:
  * Cloning it or adding as submodule the repository. Useful when we want an updated version.
  * Adding it to a local directory of the project, to be shared. Useful to ensure that works
  with a particular version.
  * Adding it in each directory where you want to do synthesis and programming. Only recommended
  when you will modify the files.
* A *options.tcl* file is needed in each directory where you want to do synthesis and programming.
* When the main *Makefile* is in another directory, other auxiliar *Makefile* is needed.

## synthesis.tcl

* The **Tcl** interpreter is automatically detected, but can be specified.
* The task to run can be specified with `-task`. The available values are:
  * `syn`: synthesis.
  * `imp`: implementation (optimizations, mapping, P&R, STA).
  * `bit`: [default] bitstream generation.
* If a vendor project file is detected, it is used.
* If not detected:
  * Functions *fpga_device* and *fpga_file* are available to be used in *options.tcl*.
  * Parameters of *options.tcl* are used to create a new project.
  * Argument `-opt` is used to select a predefined optimization. The available values are
  `none` (default, no optimization is used), `area`, `power` y `speed`.

> The GUI of the vendor tool can be used to create a project file and after that,
> you can run this script to do the synthesis process.

## programming.tcl

* The **Tcl** interpreter is automatically detected, but can be specified.
* Most tools do not support **Tcl** for programming. This script make support files when needed,
prepares commands to be executed and do a system call.
* The device to be programmed can be specified with `-dev`. The available values are `fpga`
(default), `spi` y `bpi`.
* The options of the devices, such as name, width bits (when a memory) and the **JTAG** chain
position, are obtained from *options.tcl*.
* The *path/name* of the bitstream can be specified with `-bit`.

> Libero SoC uses the project file to find the bitstream.

## Makefile (main)

* Each interpreter:
  * Has its own name and path inside the directory of the tool.
  * Is running with different options.
  * Pass options to the **Tcl** script in different ways.
* This file provides:
  * Run of *synthesis.tcl* and *programming.tcl* with any supported interpreter.
  * Options to delete the generated files.
  * Options to run a terminal of the interpreter or open the project in the vendor tool GUI.
* The tool to use can be specified in the variable *TOOL*.
Available values are `vivado`, `ise`, `quartus` and `libero`.
* The task to do can be specified in the variable *TASK*.
Available values are the same as `-task` in *synthesis.tcl*.
* The optimization to use can be specified in the variable *OPT*.
Available values are the same as `-opt` in *synthesis.tcl*.
* The device to be programmed can be specified in the variable *DEV*.
Available values are the same as `-dev` in *programming.tcl*.
* The bitstream is auto detected (when generated).

## options.tcl

Here, a self-documented example is provided:

```
# For Synthesis ###############################################################

# Function: fpga_device   <FPGA> [-tool <TOOL>]     Return: none
#   Use -tool <TOOL> to specify FPGAs from different vendors.
#   Useful when comparing synthesis results between vendors.
# Function: fpga_file     <FILE> [-lib <LIBRARY>]   Return: none
#   Use -lib to specify a library which is not work (only VHDL).
# Function: fpga_file     <FILE> [-top <TOPNAME>]   Return: none
#   Use -top to specify as top level and the component name.
# Constant: $FPGA_TOOL                              Name of the running tool
#   Useful when comparing synthesis results between vendors.

fpga_device "XC7A100T-3-CSG324" -tool "vivado"
fpga_device "XC6SLX9-2-CSG324"  -tool "ise"
fpga_device "5CGXFC7C7F23C8"    -tool "quartus"
fpga_device "M2S090TS-1-FG484"  -tool "libero"

fpga_file "core_file.vhdl"      -lib "LIB_NAME"
fpga_file "package_file.vhdl"   -lib "LIB_NAME"
fpga_file "top_file.vhdl"       -top "TOP_NAME"

# This part could be useful when comparing synthesis results between vendors.
# Add here needed particular options for each vendor tool

#if {$FPGA_TOOL == "ise"} {
#   # Customize with commands supported by ISE. Example:
#   project set "FSM Encoding Algorithm" "Sequential" -process "Synthesize - XST"
#} elseif {$FPGA_TOOL == "vivado"} {
#   # Customize with commands supported by Vivado. Example:
#   set_property "steps.synth_design.args.fsm_extraction" "sequential" [get_runs synth_1]
#} elseif {$FPGA_TOOL == "quartus"} {
#   # Customize with commands supported by Quartus. Example:
#   set_global_assignment -name STATE_MACHINE_PROCESSING SEQUENTIAL
#} elseif {$FPGA_TOOL == "libero"} {
#   # Customize with commands supported by Libero-SoC.
#}

# For Programming #############################################################

# _pos:   position in jtag chain
# _width: data bits
# _name:  name of the memory

set fpga_pos  1
set spi_width 1
set spi_name  W25Q64BV
set bpi_width 8
set bpi_name  28F128J3D
```

Considerations:
* *fpga_device*, *fpga_file* and the variables with devices options are in charge of providing
the vendor independent feature.
* If we do not compare results between vendors, *fpga_device* is used without specifying a tool.
* In this file we can add other options and **Tcl** commands, own of each tool. In a comparation,
use the constant *$FPGA_TOOL*.

## Makefile (auxiliary)

* If the main *Makefile* is in the same directory as *options.tcl*, modify the default values when
needed.
* If the main *Makefile* is in another directory, an auxiliary *Makefile* is needed. Example:

```Makefile
#!/usr/bin/make

# You can set here variables such as TOOL, TASK, OPT and DEV if you
# want to change the predefined values. Do it before the include.
TOOL=ise

TCLPATH=../../fpgahelpers/tcl
include $(TCLPATH)/Makefile

# You can add here extra targets if you need.
```

# Python

## FPGA Setup (Linux only)
In Linux systems, once the vendor's tools are installed, to execute them extra steps are required
(run license server, add the necessary environment variables to the system *PATH* so the main
*Makefile* could know them). This could be made by:
* Running the required actions manually each time you need to use them.
* Having it automated, e.g. using *.bashrc*.
* Using *fpga_setup*.

> Having the console tools *PATHs* automated precharged may be counterproductive, sometimes
> system libraries and others applications can crash with the vendors libraries.

* It's a **Bash** *script* with two main purposes:
  * *PATHs* and license servers configurations (creates a .fpga_helpers file on the user home).
  * Prepares a terminal to execute the selected tools.

When it's run without arguments, an interactive menu is provided. To see the available options,
use `--help`.

## FPGA Wizard

Creates *options.tcl* and an auxiliary *Makefile* when needed, based on answering a few questions:
* It provides an interactive menu interface.
* Questions are self-documented.
* *TAB completion* supported (double **TAB** key hitting enables options or autocomplete).
* Finds and detects the *top level* file if in the same directory as executed.
* Allows the selection of a board (preconfigured options) or charging the data and features of the device being programmed.

## FPGA Synt

The manufacturer's GUI tool can be used to make a project and then *fpga_synt* can be use to
execute synthesis, implementation, and *bitstream* generation.
The project file can be specified as an argument or is autodetected if in the same directory.
Manufacturer's tool to be used is accordingly the project file found and must be ready to be executed.

## FPGA Prog

If there is a generated *bitsream*, *fpga_prog* can be used to transfer to the FPGA or a memory
without the need of project creation. There are options to choose the tool to use, the *bitstream*,
the device to be programed, the board to use, or device specific features (position, name, bits).
The manufacturer's tool must be ready to be executed.

# Examples

## Example 1: FPGA Setup (Linux only)

* When a new tool is installed, or when something in the system change (new license file, the tool
path, etc), a configuration is needed. Run `$ fpga_setup --config` for that.
* Each time the main *Makefile* is used (invoked from the auxiliar, when *fpga_synt* or *fpga_prog*
are used) a configured terminal is needed. To have all the tools available, run `$ fpga_setup --all`
and to use one in particular, run `$ fpga_setup --TOOLNAME`.
* Also an interactive menu is available: `$ fpga_setup`.
* Run `$ fpga_setup --help` to see the help.

## Example 2: FPGA Synth

If we have a project file generated with the GUI of a vendor tool:
* Auto detect the project file and generates the bitstream: `$ fpga_synt`.
* Run the synthesis of a Vivado project file: `$ fpga_synt --task=syn PROJECT_FILE.xpr`
* Run `$ fpga_synt --help` to see the help.

## Example 3: FPGA Prog

If we have a bitstream:
* Using ISE to programming the SPI memory of the board *Avnet Spartan 6 MicroBoard*:
`$ fpga_prog --tool=ise --device=spi --borad=avnet_s6micro BITSTREAM.bit`
* To see the help and the list of available board: `$ fpga_prog --help`

## Example 4: FPGA Wizard

* Files:
  * *core_file.vhdl* (in library LIB_NAME).
  * *package_file.vhdl* (in library LIB_NAME).
  * *top_file.vhdl* (*top level* with entity TOP_NAME).
  * *s6micro.ucf* (*constraints* IO of the board *Avnet Spartan 6 MicroBoard*).
* Tool to use: ISE.
* Path to **Tcl** files: they are in `<FPGA_HELPERS_ROOT>/fpgahelpers/tcl`.

```
$ fpga_wizard 
INSTRUCTIONS: left EMPTY for default option and press TAB for autocomplete.
* TOOL to be used? [vivado] > ise
NOTE: if there are no Tcl files in the target path, they are created.
* Path to the Tcl files? [../tcl] > ../fpgahelpers/tcl/
* Top Level file? [top.vhdl] > 
* Add files to the project (empty file to FINISH).
  * Path to the file [FINISH] > core_file.vhdl
  * In library [None] > LIB_NAME
  * Path to the file [FINISH] > package_file.vhdl
  * In library [None] > LIB_NAME
  * Path to the file [FINISH] > s6micro.ucf
  * In library [None] > 
  * Path to the file [FINISH] > 
* Board to be used? [None] > avnet_s6micro
fpga_wizard (INFO): directory ../fpgahelpers/tcl was created
fpga_wizard (INFO): Makefile was copy to ../fpgahelpers/tcl
fpga_wizard (INFO): synthesis.tcl was copy to ../fpgahelpers/tcl
fpga_wizard (INFO): programming.tcl was copy to ../fpgahelpers/tcl
fpga_wizard (INFO): Makefile and options.tcl were generated
```

The final *options.tcl* is:
```
set fpga_name xc6slx9-csg324
set fpga_pos  1
set spi_name  N25Q128
set spi_width 4

fpga_device   $fpga_name

fpga_file     core_file.vhdl                 -lib LIB_NAME
fpga_file     package_file.vhdl              -lib LIB_NAME
fpga_file     s6micro.ucf
fpga_file     top_file.vhdl                  -top TOP_NAME
```

The final auxiliary *Makefile* is:
```
#!/usr/bin/make
#Generated with fpga_wizard v0.3.0

TOOL    = ise
TCLPATH = ../../../fpgahelpers/tcl/
include $(TCLPATH)/Makefile
```

And now we can:
* Get help with: `make help`
* Run synthesis with default values: `make run`
* Run synthesis changing some values: `make TASK=imp OPT=speed run`
* Run programming with default values: `make prog`
* Run programming changing some values: `make DEV=spi prog`
* Delete generated files `make clean`.

## Example 5: Multi Vendor Project

* Files:
  * *core_file.vhdl* (in library LIB_NAME).
  * *package_file.vhdl* (in library LIB_NAME).
  * *top_file.vhdl* (*top level* with entity TOP_NAME).
  * *s6micro.ucf* (*constraints* IO of the board *Avnet Spartan 6 MicroBoard*).
  * *de0nano.tcl* (*constraints* IO of the board *Terasic DE0-Nano development and education board*).
* Tool to use: ISE and Quartus.
* Path to **Tcl** files: they are in ../tcl (were copied to a shared local directory).

We do the file *options.tcl*:
```
fpga_file     core_file.vhdl                 -lib LIB_NAME
fpga_file     package_file.vhdl              -lib LIB_NAME
fpga_file     top_file.vhdl                  -top TOP_NAME

if {$FPGA_TOOL == "ise"} {
   fpga_file     s6micro.ucf
   set fpga_name xc6slx9-csg324
   set fpga_pos  1
   set spi_name  N25Q128
   set spi_width 4
} elseif {$FPGA_TOOL == "quartus"} {
   fpga_file     de0nano.tcl
   set fpga_name EP4CE22F17C6
   set fpga_pos  1
   set spi_name  EPCS64
   set spi_width 4
}

fpga_device   $fpga_name
```

We do the auxiliary *Makefile*:
```
#!/usr/bin/make
TCLPATH = ../tcl/
include $(TCLPATH)/Makefile
```

And now we can:
* Get the bitstream with ISE: `make TOOL=ise run`
* Get the bitstream with Quartus: `make TOOL=quartus run`
* Programming the FPGA with ISE: `make TOOL=ise prog`
* Programming the FPGA with Quartus: `make TOOL=quartus prog`
* Delete all the generated files: `make clean-multi`.

> Is not possible do programming any board with any vendor tool. In the
> example, we assumed that the needed board is connected in each case.
