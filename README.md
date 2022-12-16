# knit_script

## Set Up
### Install Development Version (from local source code)
```
$ git clone https://github.com/mhofmann-Khoury/knit_script.git
$ pip install -e knit_script   
```
This will clone the [repository](https://github.com/mhofmann-Khoury/knit_script) to your machine and then install the system for active development to your python 
interpreter associated with pip. This will give you access to knit_script from anywhere on your machine as other 
standard python libraries.

### Install Stable Version from PyPI

```
$ pip install knit_script
```
 
### Adding DAT compiler for command line interpreting
Note the location that your pip install creates site packages. Often 
`C:\Users\<user_name>\AppData\Roaming\Python\Python39\site-packages\knit_script`. In the knit_script_interpreter 
folder at this location you will need to put in your own copy of the knitout_to_dat.js file. This is not provide 
with this distribution because it contains copyrighted material.

### Instructions for updating PyPi Distribution:
 See [reference](https://towardsdatascience.com/how-to-upload-your-python-package-to-pypi-de1b363a1b3)

### Using knit_script from command line (Unix) # todo, untested
```
$knit_script -k <name for knitout to generate> -d <name for dat file to generate, optional> <name of knit_script file>
```
For example, when in the directory of tests\calibration samples we can generate a stockinette dat file by running
```
$ knit_script -k stst_knitout.k -d stst_dat.dat stst.ks
```

### Using knit_script from command line (windows)
Index into the knit_script directory to access knit_script.bat or add knit_script.bat to your system PATH
```
$knit_script.bat -k <name for knitout to generate> -d <name for dat file to generate, optional> <name of knit_script file>
```
For example, when in the directory of tests\calibration samples we can generate a stockinette dat file by running
```
$ knit_script.bat -k stst_knitout.k -d stst_dat.dat stst.ks
```

### Using knit_script Interpreter from Python
To just generate a knitout file from knit_script, use the following

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

## Knit Script DSL
Knitscript is a scripting language designed to offer the computing convenience of standard languages (e.g., Python 3)
with quality of life features specific to V-Bed Machine knitting. The language is built on a virtual machine model 
of a v-bed knitting machine similar to those assumed by knitout. Unlike knitout, knit script offers variables, 
control structures, functions, access to imported python libraries and much more. Knit Script interprets down to 
knitout operations that have been validated and should run without error on your machine. 

### Carriage Passes

The core knitting control structure of KnitScript is the control pass structure. A carriage pass is a set of 
consecutive needle operations (e.g., knit, tuck, miss, split, drop, xfer) that happen in one pass of the machine 
carriage. The direction that the carriage passes over the needles will determine the order that these operations 
occur. A carriage pass moving from left (needle 0) to right (max needle) (e.g., Rightward, Increasing, +, -->) will 
execute the operations on needles 0 to the max needle. A reverse carriage pass (e.g., Leftward, Decreasing, -, <--) 
will execute in the opposite order. Carriage passes are the unit of time we use to measure knitting programs and, as 
such, efficient use of carriage passes is essential to writing good knitting instructions. Knit script lets you 
disambiguate which needles you want to do an operation on from the direction you want to move in the carriage pass 
control structures. 

V-bed knitting allows for two types of carriage passes: those that involve yarn carriers and those that don't. Let's 
first look at those that require a yarn carrier. 

The direction that a yarn moves must be specified by the programmer. Dragging a yarn from the left to the right will 
produce different knitted structures than pulling it from left to right. Most of the time we want to drag the yarn 
in the opposite direction that we last knit it in. 

#### Directed Carriage Passes
A directed carriage pass is described with a `direction` and list of `operations` applied to `needles` as follows:

```KnitScript
in <direction> direction:{
    <operaton> <needles>;
    ...
    <operation> <needles>;
}
```

For example, we can knit the first even front needles up to `f10` in a Leftward direction:
```KnitScript
in Leftward direction:{
    knit Front_Needles[0:10:2];
}
```

In the same carriage pass, we can knit every other back needle:
```KnitScript
in Leftward direction:{
    knit Front_Needles[0:10:2];
    knit Back_Needles[1:10:2];
}
```
Note that this will knit one carriage pass with needles in the following order: `f0 b1 f2 b3...f8 b9`. This is 
because KnitScript ignores the order that needles are provide to an operation and instead sorts them into the 
order that they will be knit in the carriage pass direction (e.g., `Leftward` and increasing). If we change the 
direction of this pass to be `Rightward` it will knit in the following order `b9 f8 b7 f6...b1 f0`. This means that 
you don't have to keep track of the order needles are knit in. This is especially useful when rapidly switching 
between knitting directions.

You can mix operations that involve a yarn carrier into one carriage pass. Let's say you want to knit every even 
needle on the front and tuck the odd needles:

```KnitScript
in Rightward direction:{
    knit Front_Needles[0:10:2];
    tuck Front_Needles[1:10:2];
}
```

As a general rule, you want to reverse direction between carriage passes that involve a yarn carrier. Otherwise, the 
yarn will be dragged across the whole piece creating long floats. However, because knit script lets you write 
carriage passes in functions and jump around your code base you may not know where the carriage was last left. No 
fear, we have keywords for that. You can knit in the `current` or `reverse` direction. The `current` direction will 
repeat the last carriage pass direction run in with a yarn carrier. `reverse` will apply it in the reverse direction.
So to knit our front needles back and forth over 10 rows we can write:

```KnitScript
for r in range(0, 10):{
    in reverse direction:{
        knit Front_Needles[0:10];
    }
}
```

The needles you pass to an operation can be any iterable of needles. If you provide integers they will be cast 
to front needles (e.g., `knit range(0,3)` -> `f0 f1 f2`). The needle list can come from a variable or as we have 
been showing from the following global sets of needles: `Front_Needles`, `Back_Needles`, `Needles`. The `Needles` 
keyword will sort the loops for all-needle knitting which may not be possible on all machines. 

But what if you don't want to keep track of which needles are currently holding loops, the ones you want to knit on? 
We have keyword for that! `Loops` will give you the set of all needles that currently hold a loop. `Front_Loops` and 
`Back_Loops` will give you the set of all front/back needles that hold loops.

#### Un-Directed Carriage Passes
Xfer and drop operations don't involve a yarn and as a result the direction of the carriage pass will not affect 
your knitted object. Knitting machines tend to always do drops in a Rightward pass. Xfers seem to happen in whatever 
direction they feel like, depending on how your machine is configured. Because of this you will do these operations 
in a different control structure with optional parameters for the racking and target bed.

```KnitScript
drop <needles>;
xfer <needles> across;
xfer <needles> across to <Front|Back> bed;
xfer <needles> <n> to <Left|Right> to <Front|Back> bed;
```
Here are a few concrete examples:
Transfer all loops on needles to the opposite bed:
```KnitScript
xfer Loops across;
```
Transfer all loops in set of needles to front bed. If a needle in the set is already on the front it won't transfer 
(its already on the front bed).
```KnitScript
xfer needles across to Front bed;
```

Transfer all front loops to the left by 2 needles.
```KnitScript
xfer Front_Loops 2 to Left;
```

A key feature of xfer and drop passes is that the direction the carriage passes will not affect the values of 
`current` or `reverse` for directed carriage passes. So we can do xfers without loosing track of back and forth 
knitting operations. Let's say we want to alternate knitting rows on the front and back (garter stitch for hand 
knitting). 

```KnitScript
for r in range(0, height):{
    in reverse direction:{
        knit Loops;
    }
    xfer Loops across;
}
```

Reverse switches back and forth between Leftward and Rightward with each pass even though we have the transfer pass. 
This might introduce some necessary no-operation carriage passes, knit script handles those for you. 

### Carriers and Yarn Management

[//]: # (TODO)

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
The knit script interpreter which manages parsing and interpreting knit_script patterns. Parsing is managed through 
the [Parglare parsing toolkit](http://www.igordejanovic.net/parglare/0.16.0/).

### tests
Test classes for evaluating the interpreter and parsing knit_script samples. Calibration samples are used for 
calibrating allowable gauge on a machine. Paper samples demonstrate different basic techniques of sheet knittting. 