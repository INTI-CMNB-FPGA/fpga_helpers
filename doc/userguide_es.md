# Introducción

FPGA Helpers es un conjunto de *scripts* **Tcl** (*Tool Command Language*) y **Python**, que
ayudan a utilizar las herramientas de desarrollo desde línea de comandos y de manera
*vendor independent*. Las tareas que permiten realizar son:
* Síntesis.
* Implementación (optimizaciones, mapeo tecnológico, *place & route*, *static timing analysis*).
* Generación de *bitstreams*.
* Programación de FPGAs o memorias.

Dos *scripts* **Tcl** son los que dan soporte a las tareas disponibles y los que resuelven la
independencia de proveedor. Están acompañados por un Makefile que facilita su ejecución.
Hace falta generar un tercer *script* **Tcl** para especificar opciones (FPGA, archivos, etc).
Un proyecto basado en la utilización de FPGA Helpers debería incorporar estos archivos bajo control
de versiones o *tarball*.

> El Makefile asume que la herramienta que ejecutará está bien instalada, con una licencia
> válida configurada y se encuentra en el *PATH* de ejecutables del sistema.

Los *scripts* **Python** están para generar el archivo de opciones o ejecutar los **Tcl** para
tareas específicas. Nunca pasan a formar parte de los archivos de proyecto y deberían estar
instalados a nivel de sistema por comodidad y facilidad de uso.

# Instalación

FPGA Helpers es desarrollado bajo sistemas Debian GNU/Linux.
Los *scripts* **Tcl** son soportados por los interpretes de cada herramienta de desarrollo y
deberían ser independientes del Sistema Operativo.
Adicionalmente se precisa soporte de la utilidad *make* y el interprete *python*.

## GNU/Linux en general

Desde el repositorio, una vez clonado:
```
$ ./bootstrap
$ ./configure
$ make
# make install
```

Desde el *tarball*, una vez descargado y descomprimido:
```
$ ./configure
$ make
# make install
```

> Instalación típica suministrada por **Autotools**, por lo que soporta argumentos como
> *--prefix* y *--bindir*.

## Debian/Ubuntu y derivados

Una vez descargado el paquete deb:
```
# dpkg -i fpga-helpers_X.Y.Z-N_all.deb
```

## Windows

No hay una versión oficial de Windows, pero debería alcanzar con instalar un Shell de Linux.
Imagino que una buena opción es instalar [Git For Windows](https://git-for-windows.github.io).
Para *Windows 10 Anniversary Update* y posteriores, está disponible
[Windows Subsystem for Linux](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide).
También se puede probar con proyectos más maduros como [Cygwin](https://www.cygwin.com).

# Tcl

Los *scripts* *synthesis.tcl*, *programming.tcl* y el *Makefile* que automatiza su uso, son los
archivos que resuelven el uso de las herramientas de los fabricantes. Son de soporte y no
debería hacer falta modificarlos. La FPGA utilizada, archivos de proyectos, datos de memorias
y opciones particulares de la herramienta, se definen en el archivo *options.tcl*, que debe ser
generado según el caso.

> La parte **Tcl** de FPGA Helpers puede ser utilizada sin necesidad de los *script* *Python*,
> manipulando manualmente los archivos.

Hay diversas formas de incluir los archivos de soporte dentro de un proyecto:
* El repositorio FPGA Helpers puede ser clonado o incluido como submódulo, y sus archivos **Tcl**
utilizados directamente. En esta opción se estará utilizando siempre la versión más actual.
* Los archivos **Tcl** pueden copiarse a un directorio local del proyecto y ser utilizados desde
allí.
* Los archivos **Tcl** pueden copiarse en cada directorio donde se desee realizar síntesis y
programación. Sólo recomendable si se piensa modificar los **Tcl** o el *Makefile*.

Deberá haber un archivo *options.tcl* por cada directorio donde se desee realizar síntesis y
programación. Si el *Makefile* de soporte no se encuentre en el mismo directorio, deberá agregarse
otro *Makefile* que lo incluya.

## Características de los archivos de soporte

*synthesis.tcl*
* Detecta automáticamente el interprete **Tcl** que lo está ejecutando.
* La tarea a ejecutar puede ser especificada con el argumento `-task`. Los valores posibles son:
  * `syn`: síntesis lógica.
  * `imp`: implementación (optimizaciones, mapeo, P&R, STA).
  * `bit`: [default] generación de *bitstream*.
* Si detecta que existe un archivo de proyecto de la herramienta, lo utiliza.
> Se puede utilizar la interfaz gráfica de la herramienta para hacer el proyecto y utilizar este
> *script* para realizar el proceso de síntesis.
* Si no detecta un archivo de proyecto de la herramienta:
  * Provee las funciones *fpga_device* y *fpga_file* para ser utilizadas en *options.tcl*.
  * Utiliza los parámetros del archivo *options.tcl* para crear un nuevo proyecto.
  * Utiliza el argumento `-opt` para seleccionar optimizaciones predefinidas. Los valores posibles
  son `user` (default, no utiliza optimizaciones predefinidas), `area`, `power` y `speed`.

*programming.tcl*
* Detecta automáticamente el interprete **Tcl** que lo está ejecutando.
* La mayoría de las herramientas no poseen soporte **Tcl** para programar. Aquí armamos archivos
de soporte cuando hace falta, preparamos los comandos a ejecutar y finalmente se utiliza `exec`.
* El dispositivo a ser programado puede especificarse con el argumento `-dev`.
  Los valores posibles son `fpga` (default), `spi` y `bpi`.
* Opciones de los dispositivos, tales como nombre, cantidad de bits y posición en la cadena
**JTAG**, se especifican en *options.tcl*.
* El *path/name* del *bitstream* a utilizar se especifica con el argumento `-bit`.
> Libero SoC usa el archivo de proyecto para encontrarlo.

*Makefile*
* Cada interprete:
  * Tiene su propio nombre y locación dentro del directorio de la herramienta.
  * Se llama con diferentes argumentos.
  * Pasa los argumentos al *script* **Tcl** de maneras diferentes.
* Este archivo provee:
  * Ejecución de *synthesis.tcl* y *programming.tcl* con cualquier interprete soportado.
  * Opciones para borrar los archivos generados.
  * Opciones para ejecutar una consola del interprete o abrir el proyecto en la GUI de la
  herramienta.
* La herramienta a utilizar se puede especificar en la variable *TOOL*.
Valores posibles son `vivado`, `ise`, `quartus` y `libero`.
* La tarea a realizar se puede especificar en la variable *TASK*.
Los valores posibles son los del argumento `-task` de *synthesis.tcl*.
* La optimización predefinida a utilizar se puede especificar en la variable *OPT*.
Los valores posibles son los del argumento `-opt` de *synthesis.tcl*.
* El dispositivo a programar se puede especificar en la variable *DEV*.
Los valores posibles son los del argumento `-dev` de *programming.tcl*.
* El *bitstream* es auto detectado (cuando ya fue generado).

> El Makefile asume que la herramienta que ejecutará está bien instalada, con una licencia
> válida configurada y se encuentra en el *PATH* de ejecutables del sistema.

## Archivos a generar

A continuación un ejemplo completo y documentado de *options.tcl* para usar como ejemplo:
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

Notar que:
* *fpga_device*, *fpga_file* y las variables con opciones de dispositivos, son las que logran
la independencia del proveedor.
* Si no se realiza una comparación entre fabricantes, *fpga_device* se utiliza una única vez y sin
especificar la herramienta.
* En este archivo se puede agregar otras opciones y comandos **Tcl** propias de la herramienta que
se utilice. Si se trata de una comparación, utilizar la constante *$FPGA_TOOL* según el caso.

Si el *Makefile* de soporte se incluye en el mismo directorio que *options.tcl*, modificar la
variable *TOOL* según la herramienta que se vaya a utilizar.

Si el *Makefile* de soporte se encuentra en otro directorio, hace falta un *Makefile* local al
directorio. Ejemplo:
```Makefile
#!/usr/bin/make

# You can set here variables such as TOOL, TASK, OPT and DEV if you
# want to change the predefined values. Do it before the include.
TOOL=ise
TCLPATH=../../fpga_helpers/tcl
include $(TCLPATH)/Makefile

# You can add here extra targets if you need.
```

## Ejemplos

Con todos los archivos ubicados y listos para utilizar, dentro del directorio donde se realizará
la síntesis y/o programación:

* Obtener ayuda con: `make help`
* Ejecutar síntesis con valores predefinidos: `make run`
* Ejecutar síntesis cambiando valores de las variables del *Makefile*:
`make TOOL=quartus TASK=imp OPT=speed run`
* Ejecutar programación con valores predefinidos:`make prog`
* Ejecutar programación cambiando valores de las variables del *Makefile*:
`make TOOL=libero DEV=spi prog`
* Para eliminar archivos generados: `make clean`, `make clean-all` or `make clean-multi`.

# Python

Estos *scripts* sirven para ayudar a generar *options.tcl* y el *Makefile* local, o para ejecutar
tareas especificas que utilizan por debajo los archivos **Tcl** de soporte, pero no pasan a formar
parte del proyecto y no hace falta utilizarlos si se manipulan a mano los mencionados archivos. Se
recomienda instalarlos a nivel de sistema (donde dejan de tener el sufijo *.py*) pero también se
pueden ejecutar con el interprete de *Python* y el *PATH* al *script*.

Los Helpers actuales son:

* *fpga_setup*:  prepara el sistema para ejecutar las herramientas de los fabricantes (sólo Linux).
* *fpga_wizard*: genera los archivos de proyecto *options.tcl* y *Makefile*.
* *fpga_synt*:   ejecuta síntesis en base a un archivo de proyecto generado con la herramienta del
fabricante.
* *fpga_prog*:   transfiere un *bitstream* a una FPGA o memoria.
* *fpga_deps*:   recoge automáticamente archivos HDL que forman parte de un proyecto [WIP].

## FPGA Setup (sólo Linux)

> El Makefile asume que la herramienta que ejecutará está bien instalada, con una licencia
> válida configurada y se encuentra en el *PATH* de ejecutables del sistema.

Esto puede ser realizado:
* Corriendo manualmente las acciones requeridas;
* Automáticamente, utilizando por ejemplo *.bashrc*;
* Utilizando *fpga_setup*.

Ejemplos de uso:
* Hay configuraciones por defecto de *PATHS* y servidores de licencia, que pueden cambiarse con:
```
$ fpga_setup --configure
```
* Para preparar la consola para ejecutar todas las herramientas disponibles:
```
$ fpga_setup --all
```
* Para preparar la consola para ejecutar una herramienta en particular:
```
$ fpga_setup --vivado
```
* Se pueden ver las opciones disponibles con la opción *--help*.
* O utilizar un menú interactivo si se invoca sin opciones.

## FPGA Wizard

Se ejecuta sin argumentos y despliega un menú interactivo con unas pocas preguntas (explicadas):
```
$ fpga_wizard
```

Se obtiene *options.tcl* y el *Makefile* local. Ver la sección *Tcl* para ver como utilizarlos.

## FPGA Synt

Se puede realizar un proyecto utilizando la GUI de la herramienta del fabricante y luego utilizar
*fpga_synt* para ejecutar síntesis, implementación y generación de *bitstream*.
El archivo de proyecto puede ser especificado o se auto detecta si está en el directorio donde
se ejecuta.
La herramienta del fabricante que se utiliza es acorde al archivo de proyecto encontrado y debe
estar lista para ser ejecutada.

Ejemplo:
* Generacióm de *bitstream* auto detectando archivo de proyecto:
```
$ fpga_synt
```
* Ejecutar sólo la síntesis de un proyecto de Vivado:
```
$ fpga_synt --task=syn PROJECT_FILE.xpr
```

Ver valores posibles de argumento `-task` de *synthesis.tcl* para otras opciones.

## FPGA Prog

Si se tiene un *bitsream* se puede utilizar *fpga_prog* para transferirlo a la FPGA o memoria sin
la necesidad de crear un proyecto. Tiene opciones para especificar la herramienta a utilizar,
el *bitstream*, el dispositivo a programar (ver valores del argumento `-dev` de *programming.tcl*)
y la placa a utilizar o datos sobre el dispositivo (posición, nombre, bits).

Ejemplos:
* Utilizando ISE para programar la SPI de la placa Avnet Spartan 6 MicroBoard:
```
$ fpga_prog --tool=ise --device=spi --borad=avnet_s6micro BITSTREAM.bit
```
* Ayuda y lista de placas disponibles:
```
$ fpga_prog --help
```

La herramienta del fabricante debe estar lista para ser ejecutada.
