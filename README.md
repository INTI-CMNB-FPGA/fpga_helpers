# FPGA Helpers

[![License](https://img.shields.io/github/license/INTI-CMNB-FPGA/fpga_helpers.svg)](LICENSE)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-green.svg)

![GNU/Linux support](https://img.shields.io/badge/Linux-Ok-green.svg)
![Windows support](https://img.shields.io/badge/Window-Untested-yellow.svg)
![Other](https://img.shields.io/badge/Other-Unknown-red.svg)

![Vivado version](https://img.shields.io/badge/Vivado-2016.4-green.svg)
![ISE version](https://img.shields.io/badge/ISE-14.7-green.svg)
![Quartus version](https://img.shields.io/badge/Quartus-15.0-green.svg)
![Libero-SoC version](https://img.shields.io/badge/LiberoSoC-11.7-green.svg)
![Libero-IDE version](https://img.shields.io/badge/LiberoIDE-Unsupported-red.svg)
![Diamond version](https://img.shields.io/badge/Diamond-NotYet-red.svg)
![IceCube2 version](https://img.shields.io/badge/IceCube2-NotYet-red.svg)
![OpenFlow version](https://img.shields.io/badge/Yosis+Arachne+IceStorm-NotYet-red.svg)

A set of **Tcl** and **Python** scripts which helps to use FPGA development tools from command line
in a vendor independent way.

This project is mainly developed and mantained by the *FPGA team* of the
*Centre of Nano and Microelectronics* [CMNB](http://www.inti.gob.ar/microynanoelectronica/) of the
*National Institute of Industrial Technology* [INTI](http://www.inti.gob.ar/).

# Why from command line?

* To be friendly with version control systems.
* To provide a vendor independent use mode.
* To get reproducibility and repeatability.
* To consume less system resources.

# Why Tcl instead of a chain of programs?

The tasks of the vendor's tools can be achieved using a chain of command line programs, where the
output from one is the input of another. However, we prefer Tcl because:

* All the vendors tools supports Tcl (*Tool Command Language*) scripting, with additional own
commands, so a lot of code can be shared.
* Instead of learn and use several small programs, we only study some new commands.
* Each small program uses a particular project file, but with Tcl a unique file can be shared.

This features seems better for a vendor independent implementation.
