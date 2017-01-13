It is a Free Software development under the terms of GPL3. If you want to contribute, please take account of the following considerations.

# Languages
* The preferred language for documentation is English. However, the main authors are spanish speakers, so some initial versions could be in this language.
* The main scripting language is Python, but others languages such as Bash, Perl, Ruby and also C programs, are allowed.

# Coding Style
* CONSTANTS
* COMPOUND_CONSTANTS
* variables
* compoundVariables
* Use spaces, no tabs
* No trailing spaces
* Blocks: try to follows the blank space column. Example:
```
  if (...):
     do_something
```

# Git logs
* Please, write logs only in English language.
* The structure must be:
```
directory: short comment

[Optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description optional long description.]
```
* If you touch files of several directories, but the important things are in one, that is the important 'directory'. If there is more than one important change in different directories, please consider to do multiple commits.

# Versioning
* Format: MAYOR.MINOR.MICRO[-dev]
* MAYOR: big changes.
* MINOR: small  changes.
* MICRO: very little changes or bug fixes.
* -dev:  indicates development version of MAYOR.MINOR.MICRO (usually for MAYOR or MINOR changes).
* Example: 1.9.0-dev is the development version which will be 1.9.0.