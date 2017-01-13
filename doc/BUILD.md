All this must be done on fpga_helpers root directory.

* Delete previous generated files
```$ ./bootstrap clean```

* AutoTools
```
$ ./bootstrap
$ ./configure
$ make
```
  * For tarball generation:
```$ make dist```
  * For installation:
```$ make install```

* Debian Package (it also run AutoTools for tarball generation)
```$ make -f Makfile.debian deb```
