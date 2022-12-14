# KnitScript

## Set Up
### Install Development Version (from local source code)
```
$ git clone https://github.com/mhofmann-Khoury/knit_script.git
$ pip install -e KnitScript   
```
This will clone the repository to your machine and then install the system for active development to your python 
interpreter associated with pip. This will give you access to KnitScript from anywhere on your machine as other 
standard python libraries.

### Install Stable Version from PyPI

```
$ pip install KnitScript
```
 
### Adding DAT compiler for command line interpreting
Note the location that your pip install creates site packages. Often 
`C:\Users\<user_name>\AppData\Roaming\Python\Python39\site-packages\KnitScript`. In the knit_script_interpreter 
folder at this location you will need to put in your own copy of the knitout_to_dat.js file. This is not provide 
with this distribution because it contains copyrighted material.

### Instructions for updating PyPi Distribution:
 See [reference](https://towardsdatascience.com/how-to-upload-your-python-package-to-pypi-de1b363a1b3)

### Using knitscript from command line (Unix) # todo, untested
```
$knitscript -k <name for knitout to generate> -d <name for dat file to generate, optional> <name of knitscript file>
```
For example, when in the directory of tests\calibration samples we can generate a stockinette dat file by running
```
$ knitscript -k stst_knitout.k -d stst_dat.dat stst.ks
```

### Using knitscript from command line (windows)
Index into the KnitScript directory to access knitscript.bat or add knitscript.bat to your system PATH
```
$knitscript.bat -k <name for knitout to generate> -d <name for dat file to generate, optional> <name of knitscript file>
```
For example, when in the directory of tests\calibration samples we can generate a stockinette dat file by running
```
$ knitscript.bat -k stst_knitout.k -d stst_dat.dat stst.ks
```

### Using KnitScript Interpreter from Python
To just generate a knitout file from KnitScript, use the following

```python
from knit_script.interpret import knit_script_to_knitout

knit_graph = knit_script_to_knitout('<pattern file>', '<knitout file name>')
```

To also generate a data file use:

```python
from knit_script.interpret import knitscript_to_knitout_to_dat

knit_graph = knitscript_to_knitout_to_dat('<pattern file>', '<knitout file name>', '<dat file name>')
```

Additional examples of accessing the interpreter can be seen in the Test Cases

### Dat Compiler:
To work with a Shima Seiki Knitting machine you will need code to convert your knitout (.k) files into DAT (.dat) 
files. The DAT compiler we use for testing our samples is closed-source and not included in this project. You will 
need to bring your own to work with these machines. Install the compiler as a single javascript file called 
"knitout_to_dat.js" in the knit_script_interpreter package. The Setup.py file will load this into your python 
distribution. 

### Kniterate Compiler:
We have not tested these samples on a kniterate machine however the knitout to [kniterate compiler](https://github.com/textiles-lab/knitout-backend-kniterate/) is available and 
should work with our standardized knitout files. 

## Packages

### knit_graphs
The knit_graphs package holds the components of a Knit_Graph representation of a knitted structure. Knit Graphs are 
collections of loops connected on yarns and pulled through each other to form a node-link graph structure. Networkx 
graphs are used to represent yarns and knit graphs. This provides a variety of common graph algorithms for 
manipulating and searching in a knit graph. For more details on Loop based knit graphs reference [KnitPick](https://dl.acm.org/doi/abs/10.1145/3332165.3347886)

### knitting_machine
The knitting_machine package holds components of the machine state for a v-bed knitting machine. Knitout operations 
can be performed on this virtual machine set which will either produce a knit graph representing the knitted object 
or result in machine knitting errors. For more details on the basic representations of a knitting machine reference 
[a compiler for Machine Knitting](https://dl.acm.org/doi/10.1145/2897824.2925940). For more details on knitout 
operations reference the [knitout specification](https://textiles-lab.github.io/knitout/knitout.html).

### interpreter
The knit script interpreter which manages parsing and interpreting knitscript patterns. Parsing is managed through 
the [Parglare parsing toolkit](http://www.igordejanovic.net/parglare/0.16.0/).

### tests
Test classes for evaluating the interpreter and parsing knitscript samples. Calibration samples are used for 
calibrating allowable gauge on a machine. Paper samples demonstrate different basic techniques of sheet knittting. 