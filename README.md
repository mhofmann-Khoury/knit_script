# knit-script

[![PyPI - Version](https://img.shields.io/pypi/v/knit-script.svg)](https://pypi.org/project/knit-script)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/knit-script.svg)](https://pypi.org/project/knit-script)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: MyPy](https://img.shields.io/badge/type_checker-mypy-blue.svg)](https://mypy-lang.org/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A high-level domain-specific programming language for writing V-bed knitting machine instructions.
KnitScript provides an intuitive, Python-like syntax for creating complex knitting patterns while automatically generating optimized knitout code for machine execution.

## 🧶 Overview

KnitScript is a domain-specific programming language designed to make knitting machine programming accessible and intuitive.
While traditional knitout requires low-level instruction management, KnitScript provides:

- **High-level abstractions** for common knitting patterns
- **Automatic optimization** of needle operations and carriage passes
- **Python-like syntax** familiar to programmers
- **Multi-sheet support** for complex fabric structures
- **Comprehensive error handling** with detailed diagnostics

The language compiles to standard knitout format, making it compatible with any machine that supports the knitout specification.

## 🚀 Key Features

### Language Design
- ✅ **Python-inspired syntax** with knitting-specific extensions
- ✅ **Variable scoping** with local, global, and function scopes
- ✅ **Control flow** including loops, conditionals, and functions
- ✅ **Module system** for code organization and reuse

### Knitting Capabilities
- 🧶 **Automatic gauge management** for multi-sheet knitting
- 📐 **Sheet peeling and organization** for complex fabric structures
- 🔄 **Carrier management** with automatic activation/deactivation
- 🎯 **Direction-aware operations** with optimal carriage pass planning

### Development Experience
- 🐛 **Comprehensive error messages** with line numbers and context
- 📊 **Execution analysis** with timing and resource usage
- 📚 **Standard library** with common knitting operations

### Machine Integration
- 🖥️ Built on [virtual-knitting-machine](https://pypi.org/project/virtual-knitting-machine/) for simulation
- 📤 Generates standard [knitout](https://textiles-lab.github.io/knitout/knitout.html) output
- 🔧 Supports Shima Seiki Whole Garment knitting machines
- 📈 Creates [knit-graphs](https://pypi.org/project/knit-graphs/) for fabric analysis

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install knit-script
```

### From Test-PyPi
If you wish to install an unstable release from test-PyPi, note that this will have dependencies on PyPi repository.
Use the following command to gather those dependencies during install.
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ knitout-interpreter
```

### From Source
```bash
git clone https://github.com/your-username/knit-script.git
cd knit-script
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/your-username/knit-script.git
cd knit-script
pip install -e ".[dev]"
pre-commit install
```

## 🏃‍♂️ Quick Start

### Basic Pattern Creation
```knitscript
width = 10; // Basic variable declaration
with Carrier as c1:{ // Carrier is a reserved variable used to set the active working carrier in the code.
  in Leftward direction:{  // Directed Carriage pass statements are used to specify the direction of multiple needle operations.
    tuck Front_Needles[0::width]; // tucks are applied to a given list of needles on the front bed.
  }
  in reverse direction:{ // the reverse keyword is used to keep track of the relative direction of the carriage.
    tuck Front_Needles[1:width];
  }
  for _ in range(10):{ // python functions like range can be used as they would in python code.
    in reverse direction:{
      knit Loops; // Loops variables keep track of the current set of needles holding stitches.
    }
  }
}
cut c1; // The cut operation will outhook the given carrier.
```
```python
"""Convert a simple KnitScript pattern to knitout"""
from knit_script import knit_script_to_knitout

# Convert to knitout
knit_graph, machine = knit_script_to_knitout( pattern="stockinette.ks", out_file_name="stockinette.k", pattern_is_filename=False)
```

### Patterns with Arguments from Python
```knitscript
with Carrier as c1:{ // Carrier is a reserved variable used to set the active working carrier in the code.
  in Leftward direction:{  // Directed Carriage pass statements are used to specify the direction of multiple needle operations.
    tuck Front_Needles[0::width]; // tucks are applied to a given list of needles on the front bed.
  }
  in reverse direction:{ // the reverse keyword is used to keep track of the relative direction of the carriage.
    tuck Front_Needles[1:width];
  }
  for _ in range(height):{ // python functions like range can be used as they would in python code.
    in reverse direction:{
      knit Loops; // Loops variables keep track of the current set of needles holding stitches.
    }
  }
}
cut c1; // The cut operation will outhook the given carrier.
```
```python
"""Convert a simple KnitScript pattern to knitout"""
from knit_script import knit_script_to_knitout

# Convert to knitout
knit_graph, machine = knit_script_to_knitout( pattern="stockinette.ks", out_file_name="stockinette.k", pattern_is_filename=False,
                                              width=10, height=10)
```
Variables from the python environment can be directly loaded into the file, allowing for parameterized runs of the code.


## Language Features

#### Common Python Types
You can create common variables of the basic types of pythons using basic syntax.
```knitscript
width = 20; // ints
height = 10.5; // floats
yarn_color = "blue"; // string
is_finished = True; // bools
pattern_list = [2, 4, 2, 4]; // lists
pattern_dict = {"a": 1, "b": 2}; // dictionaries
```
#### Functions
You can create functions similar to those in Python. Functions include arguments which can have defined defaults.
```knitscript
def alt_tuck_cast_on(width = 10):{
    in Leftward direction:{
      tuck Front_Needles[0::width];
    }
    in reverse direction:{
      tuck Front_Needles[1:width];
    }
}

with Carrier as c1:{
  alt_tuck_cast_on(12); // call to function like a python function
}
```

### Machine Integration

#### Automatic Carrier Management
Changing the "Carrier" variable will declare what carrier or carrier set is being used by subsequent operations.
There is no need to specify inhooks to bring in carriers, if the active carrier is not already inhooked, it will be inhooked when it is next used.
```knitscript
Carrier = c1;
```

Carriers do need to manually be released. Calling "releasehook;" will release any carrier on the yarn-inserting-hook. If there is no hooked carrier, this is a safe no-op.
```knitscript
with Carrier as c1:{
  alt_tuck_cast_on(12);
  releasehook; // The carrier is relaeased if it is in on the yarn inserting hook
}
```

#### Direction and Racking Control
```knitscript
# Direction control
direction = rightward
knit direction  # Uses current direction

# Racking for transfers
racking = 1.0
xfer front_needles 2 right to back
```

#### Multi-Sheet Gauge Support
Sheets and Gauges are used for automatic support of layered knitting where each sheet has loops kept in their own relative layer order.

For example, it can be a useful way to create a ribbed tube without tracking transfers needed to keep the back and front of the tube untangled.
```knitscript
with Carrier as c1, Gauge as 2:{ // set the working gauge to 2 sheets
  With Sheet as s0: { // localize knitting operations to only the first sheet of fabric
    in Leftward direciton:{ // set up the rib pattern on the front of the tube.
      knit Front_Needles[0:width:2];
      knit Back_Needles[1:width:2];
    }
  }
  With Sheet as s1: { // The loops in this sheet will, by default, fall behind those in s0.
    in reverse direciton:{ // directions are not specific to a sheet, but the whole program
      knit Front_Needles[0:width:2]; // these needles will not overlap those in sheet s0.
      knit Back_Needles[1:width:2];
    }
  }
  for _ in range(height):{
    with Sheet as s0:{
      in reverse direction:{ knit Loops;} // these will only be the loops on s0.
    }
    with Sheet as s1:{
      in reverse direction: {knit Loops;} // these will only be the loops on s1
    }
  }
}
```

The relative position of sheets are controlled by their layer at each needle.
For example, we can divide this tube at the halfway point using a push statement.
```knitscript
with Carrier as c1, Gauge as 2:{ // set the working gauge to 2 sheets
  With Sheet as s0: { // localize knitting operations to only the first sheet of fabric
    push Front_Needles[0:width/2] to back; // make the first half of this sheet fall behind other sheets in this region.
    in Leftward direciton:{ // set up the rib pattern on the front of the tube.
      knit Front_Needles[0:width:2];
      knit Back_Needles[1:width:2];
    }
  }
  With Sheet as s1: { // The loops in this sheet will fall behind s0 from width/2 and then in front for the remaining needles.
    in reverse direciton:{ // directions are not specific to a sheet, but the whole program
      knit Front_Needles[0:width:2]; // these needles will not overlap those in sheet s0.
      knit Back_Needles[1:width:2];
    }
  }
  for _ in range(height):{
    with Sheet as s0:{
      in reverse direction:{ knit Loops;} // these will only be the loops on s0.
    }
    with Sheet as s1:{
      in reverse direction: {knit Loops;} // these will only be the loops on s1
    }
  }
}
```

## 📖 Language Reference

### Basic Syntax

KnitScript follows Python conventions with knitting-specific extensions:

```knitscript
// Comments are denoted by two back-slashes (like java or javascript).

// Variable assignment
stitch_count = 40
gauge_setting = 14

// String formatting using python style f strings.
print f"Knitting {stitch_count} stitches at gauge {gauge_setting}";

// Containers are indexed or sliced using python style notation
needles = Front_Needles[0:20:2]; // every other needle starting at 0 and up to 19
first_needle = needles[0]
```

### Variables and Scoping

```knitscript
// Local variables in functions
def knit_section(rows):{ // the rows parameter is local to the function scope.
    row_count = 0;
    for i in range(rows):{
        in reverse direction:{
          knit Loops; // machine scope keywords like "reverse" and "Loops" are not localized to the function.
        }
        row_count = row_count + 1;
    }
    return row_count; // functions can return
}

// Machine state variables
Gauge = 2;        // Number of sheets available to work with.
Sheet = 0;        // The sheet to localize operations to.
Carrier = 1;      // Active carrier
Racking = 0.0;    // Bed alignment
```

### Control Flow

```knitscript
// Conditionals
if stitch_count > 20:{ print "first branch";}
else: {print "second branch";}

// While loops
row = 0
while row < total_rows:{
    row += 1
}

// For loops with ranges
for row in range(10):{
    in reverse direction:{
      knit Loops;
    }
}

# For loops with collections
for needle in front_needles:{
  print needle;
}
```

### Machine Operations

```knitscript
# Basic stitching operations
in reverse direction:{ // The given instructions will be executed in the given direction order, regarless of the list order.
  knit knits; // give it a list of needles to knit
  tuck tucks; // give it a list of needles to tuck
  split splits; // give it a list of needles to split
}

# Transfer operations
xfer Front_Loops across to back bed; // transfer all loops on the front bed to the back bed.
xfer Loops across to back bed; // transfer all loops to the back bed if they are not already there.
xfer Front_Loops 2 to Right to back bed; // transfer all loops on the front bed to the back bed with a righward 2 needle offset.
xfer Front_Loops across to sliders; // transfer to sliders on back bed.

# Drop operations
drop Front_Needles[0:5]; // Drop specific needles
drop Back_Loops // Drop all back needles with loops

# Carrier operations
cut 1;  // Cut carrier 1 with an outhook operation
releasehook; // Release yarn hook
```

## 📚 Standard Library

KnitScript includes a standard library which we continue to expand with common functionality such as cast-ons, bind-offs, and helper functions.

## 📋 Dependencies

### Runtime Dependencies
- `python` >= 3.9
- `parglare` ^0.18.0 - Parser generator for KnitScript grammar
- `knit-graphs` ^0.0.6 - Knitting graph data structures
- `virtual-knitting-machine` ^0.0.13 - Virtual machine simulation
- `knitout-interpreter` ^0.0.5 - Knitout processing and execution

### Development Dependencies
- `mypy` ^1.0.0 - Static type checking
- `pytest` ^7.0.0 - Testing framework
- `pre-commit` ^3.0.0 - Code quality hooks
- `sphinx` ^5.0.0 - Documentation generation
- `black` ^22.0.0 - Code formatting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **McCann et al.** for creating the [Knitout specification](https://textiles-lab.github.io/knitout/knitout.html) that serves as our compilation target.
- **Northeastern University ACT Lab** for supporting this research and development.
- **The knitting community** for inspiration and feedback on language design.
- This work has been supported by the following NSF Grants:
  - 2341880: HCC:SMALL:Tools for Programming and Designing Interactive Machine-Knitted Smart Textiles.
  - 2327137: Collaborative Research: HCC: Small: End-User Guided Search and Optimization for Accessible Product Customization and Design.

## 📚 Related Projects

### Northeastern ACT Lab Knitting Ecosystem
- [knit-graphs](https://pypi.org/project/knit-graphs/) - Knitting graph data structures and analysis
- [virtual-knitting-machine](https://pypi.org/project/virtual-knitting-machine/) - Virtual machine simulation
- [knitout-interpreter](https://pypi.org/project/knitout-interpreter/) - Knitout processing and execution
- [koda-knitout](https://pypi.org/project/koda-knitout/) - Optimization framework for knitout

### CMU Textiles Lab
- [knitout](https://github.com/textiles-lab/knitout) - Original knitout specification and tools
- [knitout-frontend-js](https://github.com/textiles-lab/knitout-frontend-js) - JavaScript knitout frontend

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/knit-script/
- **Documentation**: https://mhofmann-khoury.github.io/knit_script/
- **Source Code**: https://github.com/mhofmann-Khoury/knit_script
- **Issue Tracker**: https://github.com/mhofmann-Khoury/knit_script/issues


**Made with ❤️ and 🧶 by the Northeastern University ACT Lab**
