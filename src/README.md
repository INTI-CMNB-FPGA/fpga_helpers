# Helpers

* fpga_setup:  set the system to execute the vendor's tool.
* fpga_wizard: generates options.tcl and Makefile (project files).
* fpga_synt:   run synthesis based on the project file of the vendor's tool.
* fpga_prog:   transfer a bitstream to a FPGA or memory.
* fpga_deps:   collect HDL files of the project [WIP].

## FPGA Setup

The Makefile which run the Tcl scripts for synthesis and programming assume that the vendor's tool
is well configured and available in the system path.

It can be done:
* Running manually the needed actions; or ...
* Automatically, for example using bashrc; or ...
* Using *fpga_setup*.

There are default configuration of paths and license servers (when needed), which can be changed
running:
```
$ fpga_setup --configure
```
To prepare a console to run all the available vendors tools:
```
$ fpga_setup --all
```

There are specific options for each tool, such as --vivado, --quartus, and more.
You can use --help to see available options.
You can use an interactive menu running *fpga_setup* without options.

## FPGA Wizard

The project files, options.tcl and Makefile, can be obtained with this helper, based on a few
questions. It has no arguments:
```
$ fpga_wizard
```

Read [tcl/README.md](../tcl/README.md) to see how to use the obtained files.

## FPGA Synt

You can make a project using the vendor's tool GUI, and after that, use *fpga_synt* to run
synthesis, implementation and bitstream generation.

The project file can be specified or is autodected if present in the same directory.
The vendor's tool to use is according to the project file (must be ready to run).

For example, to run only synthesis of a Vivado project file:
```
$ fpga_synt --task=syn PROJECT_FILE.xpr
```

Other available tasks are **imp** (implementation) and **bit** (bitstream generation) which is the
default when not specified.

## FPGA Prog

If you have a bistream, *fpga_prog* can be used to transfer it to a FPGA or memory.

It has options to specify the vendor's tool to use, the bitstream, the target device (FPGA, SPI,
BPI), and also a board or data about the target device (position, name and width when a memory).

Example of using ISE to program the SPI of an Avnet Spartan 6 MicroBoard:
```
$ fpga_prog --tool=ise --device=spi --borad=avnet_s6micro BITSTREAM.bit
```

For help and to see a list of available boards:
```
$ fpga_prog --help
```

The vendor's tool to use must be ready to run.
