# FPGA Helpers [![License](https://img.shields.io/github/license/INTI-CMNB-FPGA/fpga_helpers.svg)](LICENSE) ![Version](https://img.shields.io/github/tag/INTI-CMNB-FPGA/fpga_helpers.svg)

A set of **Tcl** and **Python** scripts which helps to use FPGA development tools from the command line in a vendor independent way.

> WARNING! WARNING! WARNING! WARNING! WARNING! 
>
> This project has been discontinued and superseded by [PyFPGA](https://gitlab.com/rodrigomelo9/pyfpga)
>
> The aim is similar but in this new project, the workflow is solved by Python scripts using the provided API.

* [Documentation](doc).

# Why from the command line?

* To be friendly with version control systems.
* To get reproducibility and repeatability.
* To consume less system resources.

# Why Tcl?

The tasks of the vendor's tools can be achieved using a chain of command line programs, where the output from one is the input of another. However, we prefer Tcl because:

* All the vendors tools supports Tcl (*Tool Command Language*) scripting, with additional own commands, so a lot of code can be shared.
* Instead of learn and use several small programs, we only study some new commands.
* Each small program uses a particular project file, but with Tcl a unique file can be shared.

This features seems better for a vendor independent implementation.

# Vendor independent?

> The development is done under a Debian GNU/Linux system, but the **Tcl** scripts
> are supported by the interpreter of each development tool. Thus, FPGA Helpers must
> work in any system with **make** and **Python** installed on (OS independent).

One of the important aim of the project is to provide a vendor-independent experience.

# Status

![GNU/Linux support](https://img.shields.io/badge/Linux-Supported-green.svg)
![MacOS support](https://img.shields.io/badge/MacOS-Untested-yellow.svg)
![Windows support](https://img.shields.io/badge/Window-Untested-yellow.svg)
![Other](https://img.shields.io/badge/Other-Unknown-red.svg)

![Vivado tool](https://img.shields.io/badge/Tool-Vivado-blue.svg)
![Vivado version](https://img.shields.io/badge/Version-2016.4-yellow.svg)
![Vivado devices](https://img.shields.io/badge/Devices-fpga-yellow.svg)
![Vivado cable](https://img.shields.io/badge/Cable-auto&nbsp;detected&nbsp;by&nbsp;HW&nbsp;manager-green.svg)

![ISE tool](https://img.shields.io/badge/Tool-ISE-blue.svg)
![ISE version](https://img.shields.io/badge/Version-14.7-green.svg)
![ISE devices](https://img.shields.io/badge/Devices-fpga,spi,bpi-green.svg)
![ISE cable](https://img.shields.io/badge/Cable-auto&nbsp;detected&nbsp;by&nbsp;Impact-green.svg)

![Quartus tool](https://img.shields.io/badge/Tool-Quartus-blue.svg)
![Quartus version](https://img.shields.io/badge/Version-15.0-orange.svg)
![Quartus devices](https://img.shields.io/badge/Devices-fpga-yellow.svg)
![Quartus cable](https://img.shields.io/badge/Cable-Usb&nbsp;Blaster-green.svg)

![LiberoSoC tool](https://img.shields.io/badge/Tool-Libero&nbsp;SoC-blue.svg)
![LiberoSoC version](https://img.shields.io/badge/Version-11.7-yellow.svg)
![LiberoSoC devices](https://img.shields.io/badge/Devices-fpga-green.svg)
![LiberoSoC cable](https://img.shields.io/badge/Cable-FlashPro5&nbsp;in&nbsp;spi_slave&nbsp;mode-yellow.svg)

![LiberoIDE tool](https://img.shields.io/badge/Tool-Libero&nbsp;IDE-blue.svg)
![LiberoIDE version](https://img.shields.io/badge/Version-Unsupported-red.svg)

![Diamond tool](https://img.shields.io/badge/Tool-Diamond-blue.svg)
![Diamond version](https://img.shields.io/badge/Version-Unsupported-red.svg)

![IceCube2 tool](https://img.shields.io/badge/Tool-IceCube2-blue.svg)
![IceCube2 version](https://img.shields.io/badge/Version-Unsupported-red.svg)

![OpenFlow tool](https://img.shields.io/badge/Tool-Yosis+Arachne+IceStorm-blue.svg)
![OpenFlow version](https://img.shields.io/badge/Version-Unsupported-red.svg)

![Other tool](https://img.shields.io/badge/Tool-Other-blue.svg)
![Other version](https://img.shields.io/badge/Version-Unsupported-red.svg)
