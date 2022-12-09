# KnitScript

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