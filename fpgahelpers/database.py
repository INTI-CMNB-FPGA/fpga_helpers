#!/usr/bin/python
#
# Data shared between FPGA Helpers
# Copyright (C) 2017-2019 INTI
# Copyright (C) 2017-2019 Rodrigo A. Melo
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

__version__ = "0.4.0"

_tools = {
    'vivado'  : {
        'prj' : 'xpr'
    },
    'ise'     : {
        'prj' : 'xise'
    },
    'quartus' : {
        'prj' : 'qpf'
    },
    'libero'  : {
        'prj' : 'prjx'
    }
}

_devices = ['fpga', 'spi', 'bpi', 'xcf', 'detect', 'unlock']

_fpga_pos  = range(1,10)

_spi_width = [1, 2, 4]
_bpi_width = [8, 16, 32, 64]
_mem_width = _spi_width + _bpi_width

_boards = {
    'avnet_s6micro' : {
        'full_name' : 'Avnet Spartan-6 FPGA LX9 MicroBoard',
        'fpga_name' : 'xc6slx9-2-csg324',
        'fpga_pos'  : '1',
        'spi_name'  : 'N25Q128',
        'spi_width' : '4',
        'spi_size'  : '128Mb'
    },
    'digilent_atlys' : {
        'full_name' : 'Digilent Atlys - Comprehensive Spartan 6 Design Platform',
        'fpga_name' : 'xc6slx45-3-csg324',
        'fpga_pos'  : '1',
        'spi_name'  : 'N25Q128',
        'spi_width' : '4',
        'spi_size'  : '128Mb'
    },
    'gaisler_xc6s' : {
        'full_name' : 'Gaisler Research GR-XC6S',
        'fpga_name' : 'xc6slx75-2-fgg484',
        'fpga_pos'  : '1',
        'spi_name'  : 'W25Q64BV',
        'spi_width' : '4',
        'spi_size'  : '64Mb'
    },
    'microsemi_m2s090ts' : {
        'full_name' : 'Microsemi M2S090TS-EVAL-KIT',
        'fpga_name' : 'm2s090ts-1-fg484',
        'fpga_pos'  : '1'
    },
    'terasic_de0nano' : {
        'full_name' : 'Terasic DE0-Nano development and education board',
        'fpga_name' : 'EP4CE22F17C6',
        'fpga_pos'  : '1',
        'spi_name'  : 'EPCS64',
        'spi_width' : '1',
        'spi_size'  : '4Mb'
    },
    'xilinx_ml605' : {
        'full_name' : 'Xilinx Virtex 6 ML605',
        'fpga_name' : 'xc6vlx240t-1-ff1156',
        'fpga_pos'  : '2',
        'bpi_name'  : '28F256P30',
        'bpi_width' : '16',
        'bpi_size'  : '256Mb'
    },
    'xilinx_sp601' : {
        'full_name' : 'Xilinx Spartan 6 SP601',
        'fpga_name' : 'xc6slx16-2-csg324',
        'fpga_pos'  : '1',
        'spi_name'  : 'W25Q64BV',
        'spi_width' : '4',
        'spi_size'  : '64Mb',
        'bpi_name'  : '28F128J3D',
        'bpi_width' : '8',
        'bpi_size'  : '16Mb'
    }
}
