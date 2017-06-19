# Directory with bitstreams to test FPGA prog

## Test ISE with Avnet S6 Micro board

* FPGA
```
python ../../src/fpga_prog.py -b avnet_s6micro -t ise s6micro.bit
```
* SPI
```
python ../../src/fpga_prog.py -b avnet_s6micro -t ise -d spi s6micro.bit
```
