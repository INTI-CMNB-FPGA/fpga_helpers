import re
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("fpgahelpers/database.py", "r") as fh:
    version = (re.search(r"__version__ = ['\"]([^'\"]*)['\"]", fh.read(), re.M)).group(1)

setup(
    name="fpgahelpers",
    version=version,
    description="CLI utilities for FPGA development in a vendor independent way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rodrigo A. Melo",
    author_email="rodrigomelo9@gmail.com",
    license="GPLv3",
    url="https://github.com/INTI-CMNB-FPGA/fpga_helpers",
    package_data={'': ['tcl/Makefile', 'tcl/*.tcl']},
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Software Development :: Build Tools",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent"
    ],
)
