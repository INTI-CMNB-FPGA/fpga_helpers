# FPGA Helpers

A Free Software project which consist on a bunch of scripts which helps to use FPGA development
tools in a vendor independent way.

This project is mainly developed and mantained by the *FPGA team* of the
*Centre of Nano and Microelectronics* [CMNB](http://www.inti.gob.ar/microynanoelectronica/) of the
*National Institute of Industrial Technology* [INTI](http://www.inti.gob.ar/).
Contributions are welcome.

The target development platform is Debian GNU/Linux, but it is probably easy to run in others OS.

## Overview

The main objectives are:
* Be friendly with version control systems.
* Provide a vendor independent use mode.
* Get reproducibility and repeatability.
* Use less system resources.

The project is divided in two part:
1. The directory tcl contains Tcl scripts for synthesis and programming, and also a Makefile.
   These three files do the magic to support several tools in a vendor independent way.
   The idea is that become part of the project.
2. The directory src contains Python and Bash scripts that helps to generate project files and run
   in an effective way the Tcl scripts for certain tasks.

For more information read [tcl/README.md](tcl/README.md) and [src/README.md](src/README.md).

## License

FPGA Helpers is licensed under the GPL3. See [LICENSE](LICENSE) for details.
