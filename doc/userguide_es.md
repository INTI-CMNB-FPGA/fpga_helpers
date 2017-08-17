# Introducción

FPGA Helpers es un conjunto de *scripts* **Tcl** (*Tool Command Language*) y **Python**, que
ayudan a utilizar las herramientas de desarrollo de FPGAs desde línea de comandos y de manera
*vendor independent*.

Dos *scripts* **Tcl**, acompañados de un *Makefile*, resuelven el soporte de múltiples
herramientas:
* *synthesis.tcl:* resuelve la Síntesis, Implementación y Generación del *bitstream*.
* *programming.tcl:* resuelve la programación de FPGAs y/o memorias.
* *Makefile:* ejecuta el *script* necesario con el interprete correspondiente.
* *options.tcl [generado]:* archivo de opciones del proyecto, indica la FPGA utilizada, archivos,
datos de memorias y opciones particulares de la herramienta.

> Implementación implica optimizaciones, mapeo tecnológico, *place & route* (P&R) y
> *static timing analysis* (STA).

> El Makefile asume que la herramienta que ejecutará está bien instalada, con una licencia
> válida configurada y se encuentra en el *PATH* de ejecutables del sistema.

Los *scripts* **Python** ayudan a utilizar a los **Tcl**, ya sea incorporándolos al proyecto
(en cuyo caso, pasan a formar parte del mismo) o ejecutándolos para tareas específicas:
* *fpga_setup (sólo Linux):* prepara el sistema para ejecutar las herramientas de los fabricantes.
* *fpga_wizard:* genera los archivos de proyecto *options.tcl* y un *Makefile* auxiliar.
* *fpga_synt*: ejecuta la síntesis en base a archivo de proyecto generado con la herramienta del
fabricante.
* *fpga_prog:* transfiere un *bitstream* a una FPGA o memoria.
* *fpga_deps [WIP]:* recoge automáticamente archivos HDL que forman parte de un proyecto.

> Los *script* **Python** nunca pasan a formar parte de los archivos de proyecto.
> Por comodidad y facilidad de uso, se recomienda que estén instalados a nivel de
> sistema (sin el sufijo *.py*), pero se pueden utilizar también *standalone*.

> La parte **Tcl** de FPGA Helpers puede ser utilizada sin necesidad de los
> *script* *Python*, manipulando manualmente los archivos.

# Instalación

Considerar que:
* FPGA Helpers es desarrollado bajo sistemas Debian GNU/Linux.
* Los *scripts* **Tcl** son soportados por los interpretes de cada herramienta de desarrollo y
deberían ser independientes del Sistema Operativo.
* Deberían servir en cualquier Sistema Operativo que soporte la utilidad *make* y el interprete
*python*.
* Se pueden utilizar de forma *standalone* (sin instalar).

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

* No hay una versión oficial de Windows, pero debería alcanzar con instalar un Shell de Linux.
* En *Windows 10 Anniversary Update* y posteriores, está disponible
[Windows Subsystem for Linux](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide), que
permite instalar paquetes de Linux (seleccionar compatibilidad con Ubuntu).
* En cualquier versión, debería servir [Git For Windows](https://git-for-windows.github.io).
* También se puede probar un proyecto como [Cygwin](https://www.cygwin.com).

# Tcl

Consideraciones:
* Los *scripts* **Tcl** pueden incluirse en un proyecto de diversas maneras:
  * Clonando o agregando como submódulo al repositorio FPGA Helpers. Útil cuando queremos
  actualizar fácilmente a la versión actual.
  * Agregándolos en un directorio local del proyecto, para ser compartidos. Útil si queremos
  garantizar el uso de una determinada versión.
  * Agregándolos en cada directorio donde se desee realizar síntesis y programación. Sólo
  recomendable si se piensan modificar en cada caso.
* Hace falta un archivo *options.tcl* por cada directorio donde se desee realizar síntesis y
programación.
* Cuando el *Makefile* principal no se encuentre en el mismo directorio, deberá agregarse un
*Makefile* auxiliar que lo incluya.

## synthesis.tcl

* Detecta automáticamente el interprete **Tcl** que lo está ejecutando.
* La tarea a ejecutar puede ser especificada con el argumento `-task`. Los valores posibles son:
  * `syn`: síntesis lógica.
  * `imp`: implementación (optimizaciones, mapeo, P&R, STA).
  * `bit`: [default] generación de *bitstream*.
* Si detecta que existe un archivo de proyecto de la herramienta, lo utiliza.
* Si no detecta un archivo de proyecto de la herramienta:
  * Provee las funciones *fpga_device* y *fpga_file* para ser utilizadas en *options.tcl*.
  * Utiliza los parámetros del archivo *options.tcl* para crear un nuevo proyecto.
  * Utiliza el argumento `-opt` para seleccionar optimizaciones predefinidas. Los valores posibles
  son `none` (default, no utiliza optimizaciones predefinidas), `area`, `power` y `speed`.

> Se puede utilizar la interfaz gráfica de la herramienta para hacer el proyecto y utilizar este
> *script* para realizar el proceso de síntesis.

## programming.tcl

* Detecta automáticamente el interprete **Tcl** que lo está ejecutando.
* La mayoría de las herramientas no poseen soporte **Tcl** para programar. Este *script* arma
archivos de soporte cuando hace falta, prepara los comandos a ejecutar y finalmente realiza una
llamada al sistema.
* El dispositivo a ser programado puede especificarse con el argumento `-dev`.
Los valores posibles son `fpga` (default), `spi` y `bpi`.
* Opciones de los dispositivos, tales como nombre, cantidad de bits y posición en la cadena
**JTAG** los toma de *options.tcl*.
* El *path/name* del *bitstream* a utilizar se especifica con el argumento `-bit`.

> Libero SoC usa el archivo de proyecto para encontrar el *bitstream*.

## Makefile (principal)

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
* El *bitstream* es auto detectado (cuando ya ha sido generado).

## options.tcl

A continuación un ejemplo completo y auto documentado:

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

Consideraciones:
* *fpga_device*, *fpga_file* y las variables con opciones de dispositivos, son las que logran
la independencia del proveedor.
* Si no se realiza una comparación entre fabricantes, *fpga_device* se utiliza una única vez y sin
especificar la herramienta.
* En este archivo se pueden agregar otras opciones y comandos **Tcl** propias de la herramienta que
se utilice. Si se trata de una comparación, utilizar la constante *$FPGA_TOOL* según el caso.

## Makefile (auxiliar)

* Si el *Makefile* principal se incluye en el mismo directorio que *options.tcl*, modificar los
valores por defecto de las variables si hace falta (se encuentran al comienzo).
* Si el *Makefile* principal está en otro directorio, hace falta un *Makefile* auxiliar. Ejemplo:

```Makefile
#!/usr/bin/make

# You can set here variables such as TOOL, TASK, OPT and DEV if you
# want to change the predefined values. Do it before the include.
TOOL=ise

TCLPATH=../../fpga_helpers/tcl
include $(TCLPATH)/Makefile

# You can add here extra targets if you need.
```

# Python

## FPGA Setup (sólo Linux)

En Linux, una vez instalada la herramienta del fabricante, hacen falta acciones adicionales
para poder ejecutarla (correr servidor de licencias en algunos casos, agregarlas al *PATH* del
sistema para que el *Makefile* principal las conozca). Esto puede ser realizado:
* Corriendo manualmente las acciones requeridas cada vez que se van a utilizar;
* Tenerlo automatizado, utilizando por ejemplo *.bashrc*;
* Utilizando *fpga_setup*.

> Tener automáticamente los *PATHs* de las herramientas en una consola puede ser
> contraproducente, dado que aveces usan bibliotecas propias que entran en conflicto
> con otros programas.

* Es un *script* **Bash** que cumple dos funciones:
* Permite configurar *PATHs* y opciones de servidores de licencia (crea archivo .fpga_helpers en
*home* del usuario).
* Prepara una consola para poder ejecutar las herramientas indicadas.

Si se invoca sin argumentos, provee un menú interactivo. Para ver las opciones disponibles,
utilizar *--help*.

## FPGA Wizard

Crea *options.tcl*, y un *Makefile* auxiliar cuando hace falta, a partir de contestar unas pocas
preguntas. La mayoría de ellas, tienen opciones por defecto auto detectadas.

> Esta herramienta no posee argumentos. Es un menú interactivo, con cada opción documentada.

> Esta herramienta soporta *TAB completion*.

## FPGA Synt

Se puede realizar un proyecto utilizando la GUI de la herramienta del fabricante y luego utilizar
*fpga_synt* para ejecutar síntesis, implementación y generación de *bitstream*.
El archivo de proyecto puede ser especificado o se auto detecta si está en el mismo directorio.
La herramienta del fabricante que se utiliza es acorde al archivo de proyecto encontrado y debe
estar lista para ser ejecutada.

## FPGA Prog

Si se tiene un *bitsream* se puede utilizar *fpga_prog* para transferirlo a la FPGA o memoria sin
la necesidad de crear un proyecto. Tiene opciones para especificar la herramienta a utilizar,
el *bitstream*, el dispositivo a programar, la placa a utilizar o datos sobre el dispositivo
(posición, nombre, bits). La herramienta del fabricante debe estar lista para ser ejecutada.

# Ejemplos

## Ejemplo 1: FPGA Setup (sólo Linux)

* Al instalar una nueva herramienta soportada, o si cambia algo en el sistema (archivo de licencia,
*PATH* de la herramienta, etc), hace falta realizar una configuración. Esto se logra ejecutando
`$ fpga_setup --config`.
* Cada vez que se utilice el *Makefile* principal (al usarlo desde el auxiliar, al ejecutar
*fpga_synt* o *fpga_prog*) hace falta estar en una consola configurada. Para disponer de todas
las herramientas, ejecutar `$ fpga_setup --all` y para una en particular, ejecutar
`$ fpga_setup --TOOLNAME`.
* También se puede acceder a un menú interactivo ejecutando simplemente `$ fpga_setup`.
* Para ver la ayuda: `$ fpga_setup --help`.

## Ejemplo 2: FPGA Synth

Teniendo archivos de proyecto generados con la GUI de alguna herramienta soportada:
* Generar el *bitstream* auto detectando archivo de proyecto: `$ fpga_synt`.
* Ejecutar sólo la síntesis especificando el archivo de proyecto de Vivado:
`$ fpga_synt --task=syn PROJECT_FILE.xpr`
* Para ver la ayuda: `$ fpga_synt --help`.

## Ejemplo 3: FPGA Prog

Teniendo ya *bitstreams* generados:
* Utilizar ISE para programar la SPI de la placa Avnet Spartan 6 MicroBoard:
`$ fpga_prog --tool=ise --device=spi --borad=avnet_s6micro BITSTREAM.bit`
* Ayuda y lista de placas disponibles: `$ fpga_prog --help`

## Ejemplo 4: FPGA Wizard

Suponiendo tener los archivos:
* *core_file.vhdl* (entity CORE_NAME, incluido en LIB_NAME).
* *package_file.vhdl* (entity PACKAGE_NAME, incluido en LIB_NAME).
* *top_file.vhdl* (entity TOP_NAME, es el Top Level).
* *s6micro.ucf* (*constraints* IO de placa *Avnet Spartan 6 MicroBoard*).

Vamos a utilizar la herramienta ISE y los **Tcl** directamente habiendo incluido a FPGA Helpers
como submódulo **git**:

```
$ fpga_wizard 
fpga_wizard is a member of FPGA Helpers v0.3.0

Select TOOL to use [vivado]
EMPTY for default option. TAB for autocomplete. Your selection here > ise

Where to get (if exists) or put Tcl files? [../tcl]
EMPTY for default option. TAB for autocomplete. Your selection here > ../fpga_helpers/tcl/

Top Level file? [top_file.vhdl]
EMPTY for default option. TAB for autocomplete. Your selection here > 

Add files to the project (EMPTY to FINISH):
* Path to the file [FINISH]:
EMPTY for default option. TAB for autocomplete. Your selection here > core_file.vhdl
* In library [None]:
EMPTY for default option. TAB for autocomplete. Your selection here > LIB_NAME
* Path to the file [FINISH]:
EMPTY for default option. TAB for autocomplete. Your selection here > package_file.vhdl
* In library [None]:
EMPTY for default option. TAB for autocomplete. Your selection here > LIB_NAME
* Path to the file [FINISH]:
EMPTY for default option. TAB for autocomplete. Your selection here > s6micro.ucf
* In library [None]:
EMPTY for default option. TAB for autocomplete. Your selection here > 
* Path to the file [FINISH]:
EMPTY for default option. TAB for autocomplete. Your selection here > 

Board to be used? [None]
EMPTY for default option. TAB for autocomplete. Your selection here > avnet_s6micro


fpga_wizard (INFO): Makefile and options.tcl were generated
```

El archivo *options.tcl* resultante es:

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

El archivo *Makefile* resultante es:
```
#!/usr/bin/make
#Generated with fpga_wizard v0.3.0

TOOL    = ise
TCLPATH = ../../../fpga_helpers/tcl/
include $(TCLPATH)/Makefile
```

Y a partir de aquí, podemos:
* Obtener ayuda con: `make help`
* Ejecutar síntesis con valores predefinidos: `make run`
* Ejecutar síntesis cambiando valores de las variables del *Makefile*:
`make TASK=imp OPT=speed run`
* Ejecutar programación con valores predefinidos:`make prog`
* Ejecutar programación cambiando valores de las variables del *Makefile*:
`make DEV=spi prog`
* Para eliminar archivos generados: `make clean`.
