import re
import fpgahelpers.database
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fpgahelpers",
    version=fpgahelpers.database.__version__,
    description="CLI utilities for FPGA development in a vendor independent way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rodrigo A. Melo",
    author_email="rodrigomelo9@gmail.com",
    license="GPLv3",
    url="https://github.com/INTI-CMNB-FPGA/fpga_helpers",
    package_data={'': ['tcl/Makefile', 'tcl/*.tcl']},
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fpga_wizard = fpgahelpers.fpga_wizard:main',
            'fpga_synt   = fpgahelpers.fpga_synt:main',
            'fpga_prog   = fpgahelpers.fpga_prog:main'
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Build Tools",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent"
    ],
)
