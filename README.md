# knit_script
Knit Script is a domain-specific programming language for writing v-bed knitting machine instructions. The language is loosely based on conventions from Python 3 but includes support for controlling a knitting machine. The code is interpreted into knitout which can then be processed into instructions for different types of knitting machines.

# Set Up
## Install Development Version (from local source code)
```
$ git clone https://github.com/mhofmann-Khoury/knit_script.git
$ pip install -e .   
```
This will clone the [repository](https://github.com/mhofmann-Khoury/knit_script) to your machine and then install the system for active development to your python interpreter associated with pip. This will give you access to knit_script from anywhere on your machine as other standard python libraries.

[//]: # (Distribution is updated with the following commands from within the repo directory:)

[//]: # (```)

[//]: # (python setup.py sdist)

[//]: # (python -m build)

[//]: # (twine upload dist/*)

[//]: # (```)

## Install Stable Version from [PyPI](https://pypi.org/project/knit-script/)

```
$ pip install knit-script
```

[//]: # (## Add Your Own DAT Compiler)

[//]: # (The Knitout to DAT compiler we use for controlling Shima Seiki machines is copyrighted and not provided with this distribution. You can install your own copy of the DAT compiler under the `dat_compiler` folder in your installation. Name the javascript entry point `knitout-to-dat.js` and have the main method accept two arguments for the knitout file name and the output dat file name. )

## Kniterate Compiler:
We have not tested these samples on a kniterate machine, however, the knitout to [kniterate compiler](https://github.com/textiles-lab/knitout-backend-kniterate/) is available and should work with our standardized knitout files. 

## Testing your installation

You can check that your installation using the installation_test.ks and installation_test.py files in the `installation_test` package.
Running the installation_test.py file should produce the following files:
1. `installation_test_from_string.k`
2. `installation_test_from_file.k`
3. `installation_test_to_dat.k`
4. `installation_test.dat`

You can work through this example using the `installation_test.ipynb` jupyter notebook.
Similarly, you can convert installation_test.ks into the same files using the entry points from your local terminal 

### Using knit_script from command line (Unix)
```
$knit-script -k <name for knitout to generate> -d <name for dat file to generate, optional> <name of knit_script file>
```
For example, convert installation_test.ks as follows:
```
$ knit-script -k stst_10.k -d stst_10.dat installation_test.ks
```

The resulting dat file should look like:

![A 10x10 square of stockinette in a dat format](/expected_installation_test_output.PNG)
### Using knit_script from command line (windows)
Index into the knit_script directory to access knit_script.bat or add knit_script.bat to your system PATH
```
$knit_script.bat -k <name for knitout to generate> -d <name for dat file to generate, optional> <name of knit_script file>
```
For example, convert installation_test.ks as follows:
```
$ knit_script.bat -k stst_10.k -d stst_10.dat installation_test.ks
```

## Using knit_script Interpreter from Python
To just generate a knitout file from knit_script, use the following

```python
from knit_script.interpret import knit_script_to_knitout

knit_graph, machine_state = knit_script_to_knitout('<pattern file>', '<knitout file name>')
```

To also generate a data file use:

```python
from knit_script.interpret import knit_script_to_knitout_to_dat

knit_graph, machine_state = knit_script_to_knitout_to_dat('<pattern file>', '<knitout file name>', '<dat file name>')
```

For more information, check out the jupyter notebook in the `installation_test` package.

Additional examples of accessing the interpreter can be seen in the `test` package.

# Knit Script DSL
Knit script is a scripting language designed to offer the computing convenience of standard languages (e.g., Python 3) with quality of life features specific to V-Bed Machine knitting.
The language is built on a virtual machine model of a v-bed knitting machine similar to those assumed by knitout.
Unlike knitout, knit script offers variables, control structures, functions, access to imported python libraries and much more.
Knit Script interprets down to knitout operations that have been validated and should run without an error on your machine. 

## Carriage Passes

The core knitting control structure of KnitScript is the control pass structure. A carriage pass is a set of consecutive needle operations (e.g., knit, tuck, miss, split, drop, xfer) that happen in one pass of the machine carriage. The direction that the carriage passes over the needles will determine the order that these operations occur. A carriage pass moving from left (needle 0) to right (max needle) (e.g., Rightward, Increasing, +, -->) will execute the operations on needles 0 to the max needle. A reverse carriage pass (e.g., Leftward, Decreasing, -, <--) will execute in the opposite order. Carriage passes are the unit of time we use to measure knitting programs and, as such, efficient use of carriage passes is essential to writing good knitting instructions. Knit script lets you disambiguate which needles you want to do an operation on from the direction you want to move in the carriage pass control structures. 

V-bed knitting allows for two types of carriage passes: those that involve yarn carriers and those that don't. Let's first look at those that require a yarn carrier. 

The direction that a yarn moves must be specified by the programmer. Dragging a yarn from the left to the right will produce different knitted structures than pulling it from left to right. Most of the time we want to drag the yarn in the opposite direction that we last knit it in. 

### Directed Carriage Passes
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
Note that this will knit one carriage pass with needles in the following order: `f0 b1 f2 b3...f8 b9`. This is because KnitScript ignores the order that needles are provided to an operation and instead sorts them into the order that they will be knit in the carriage pass direction (e.g., `Leftward` and increasing). If we change the direction of this pass to be `Rightward` it will knit in the following order `b9 f8 b7 f6...b1 f0`. This means that you don't have to keep track of the order needles are knit in. This is especially useful when rapidly switching between knitting directions.

You can mix operations that involve a yarn carrier into one carriage pass. Let's say you want to knit every even needle on the front and tuck the odd needles:

```KnitScript
in Rightward direction:{
    knit Front_Needles[0:10:2];
    tuck Front_Needles[1:10:2];
}
```

As a general rule, you want to reverse the direction between carriage passes that involve a yarn carrier.
Otherwise, the yarn will be dragged across the whole piece creating long floats.
However, because knit script lets you write carriage passes in functions and jump around your code base, you may not know where the carriage was last left.
No fear, we have keywords for that.
You can knit in the `current` or `reverse` direction.
The `current` direction will repeat the last carriage pass direction run in with a yarn carrier.
Will apply it in the reverse direction.
So to knit our front needles back and forth, over 10 rows we can write:

```KnitScript
for r in range(0, 10):{
    in reverse direction:{
        knit Front_Needles[0:10];
    }
}
```

The needles you pass to an operation can be any iterable of needles. If you provide integers they will be cast to front needles (e.g., `knit range(0,3)` -> `f0 f1 f2`). The needle list can come from a variable, or as we have been showing from the following global sets of needles: `Front_Needles`, `Back_Needles`, `Needles`. The `Needles` keyword will sort the loops for all-needle knitting that may not be possible on all machines. 

But what if you don't want to keep track of which needles are currently holding loops, the ones you want to knit on? We have keyword for that! `Loops` will give you the set of all needles that currently hold a loop. `Front_Loops` and `Back_Loops` will give you the set of all front/back needles that hold loops.

### Un-Directed Carriage Passes
Xfer and drop operations don't involve a yarn, and as a result, the direction of the carriage pass will not affect your knitted object.
Knitting machines tend to always do drops in a Rightward pass.
Xfers seem to happen in whatever direction they feel like, depending on how your machine is configured.
Because of this, you will do these operations in a different control structure with optional parameters for the racking and target bed.

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
Transfer all loops in a set of needles to the front bed. If a needle in the set is already on the front, it won't transfer (its already on the front bed).
```KnitScript
xfer needles across to Front bed;
```

Transfer all front loops to the left by 2 needles.
```KnitScript
xfer Front_Loops 2 to Left;
```

A key feature of xfer and drop passes is that the direction the carriage passes will not affect the values of `current` or `reverse` for directed carriage passes.
So we can do xfers without losing track of back and forth knitting operations.
Let's say we want to alternate knitting rows on the front and back (garter stitch for hand-knitting). 

```KnitScript
for r in range(0, height):{
    in reverse direction:{
        knit Loops;
    }
    xfer Loops across;
}
```

Reverse switches back and forth between Leftward and Rightward with each pass even though we have the transfer pass. This might introduce some necessary no-operation carriage passes, knit script handles those for you. 

## Carriers and Yarn Management
Of course, you can't knit with air, and our examples so far say nothing about the yarn being knit with.

Knitting machines control the yarn by pulling yarn-carriers across the needle bed in sync with the carriage pass.
Each carrier has one yarn and multiple carriers can be used at the same time.
In order to use a carrier, it must be active or `inhooked` on the machine.
In knitout, this is managed manually with the `inhook` and `in` commands.
When a yarn is no longer needed, and likely getting in your way, you deactivate carriers with `outhook` and `out` commands. 

### The Yarn-Inserting-Hook

The main challenge of using carriers is managing the yarn-inserting-hook. When a yarn is first brought onto the machine, it is loose and will slip out of the carrier. To prevent this, a yarn-inserting-hook grabs the tail of yarn and holds it in place while the yarn is knit. This hook hovers above needles on the bed and will block those needles from being used. The yarn-inserting-hook will be positioned just before the first needle that knits with the carrier. When you no longer need the hook to hold the yarn-tail because the yarn has knit enough loops you call `releasehook` in knitout. Choosing when to release the hook in knitout is a tension between multiple trade-offs. First, the longer you hold it, the longer you cannot use the needles below and after that hook. Second, as long as it is holding one yarn, you can't bring in a new yarn. Third, if you release it too early, the loops knit with that yarn are likely to come loose. One of the benefits of knitout is that you don't have to factor these considerations into your knitting program. Knit script does it for you.

### Declaring Active Carriers in Knit Script

Knit Script has a global variable named `Carrier`. Setting the value of `Carrier` to a yarn carrier will declare that all subsequent directed passes will use that carrier. The interpreter will also add an `inhook` operation when a new carrier is declared and a `in` operation if the carrier is already active. All of our prior examples were using `Carrier` by default. Run on their own, they will error because `Carrier` is not declared and no carriers will be activated in the knitout.

You can declare carrier the same way you declare any other variable. A simple variable declaration will work and will insert any needed `inhook` and `in` operations into your knitout before you use the carrier in a directed pass. 

```KnitScript
Carrier = 1; // carrier will be set to first carrier on machine. Integer 1 casts to c1
Carrier = c2; // positive integers prefixed with c declare a carrier
Carrier = [c1, 2]; // lists of carriers are used for platted knitting with multiple carriers at once.
// The order of carriers will be the order of yarns in the plate. Carriers and integers can be mixed
Carrier += 1; // integer operations on carriers will act like integers
```

Knit Script is designed to treat carriers like output streams in other languages. If you bring a carrier in, it must eventually go out, and when switching between different scopes you don't want to lose track of what carriers have already been activated. Like managing file-streams in Python, we recommend that you use with-statements to control which carrier is active. 

Consider the basic example where we want to knit stockinette with Carrier 1. Inside the with statement, the carrier will be c1 unless otherwise set. Outside the with statement, no carrier is available. 

```KnitScript
import cast_ons;
width = 20;
height = 10;

def knit_stripe():{
    for r in range(0, height):{
        in reverse direction: { // Looks for carrier from outer scope. 
            knit Loops;
        }
    }
}

with Carrier as c1:{
    // All operations in this with statement will use carrier 1 unless another carrier is declared
    cast_ons.alt_tuck_cast_on(width); // function call from standard knit script library
    knit_stripe();
}
// Any knitting operations out here will cause an error since no carrier is active.
```

But what if you want to use a different carrier inside some sub-scope, like a function call? Declaring the carrier value either with a variable declaration or a with statement will only set that value for the current scope. So when you leave that scope, the carrier will default back to the outer scopes value.

Let's say you want to knit some stripes of stockinette with a different carrier, but otherwise knit with c1:
```knit_script
import cast_ons;
width = 20;
height = 10;

def knit_stripe():{
    for r in range(0, height):{
        in reverse direction: { // Looks for carrier from outer scope. 
            knit Loops;
        }
    }
}

def knit_colored_stripe(new_carrier):{
    with Carrier as new_carrier:{
        knit_stripe();
    }
}

with Carrier as c1:{
    cast_ons.alt_tuck_cast_on(width);
    knit_stripe(); // uses c1
    knit_colored_stripe(c2); // will use c2
    knit_stripe(); // starts using c1 again
}
```

### Cutting Yarns
In knitout, yarns are cut with an outhook operation that hooks the yarn on the yarn-inserting-hook, cuts it, then returns the tail of the yarn left on the carrier to the grippers. To use that carrier again, it will need to be inhooked again. Since cutting a yarn is destructive, you must explicitly cut the yarns.

In knit script you cut a yarn with a cut statement which is the keyword `cut` followed by one or more carriers or a list of carriers. For example:
```knit_script
cut 1; // cuts carrier 1
cut Carrier; // cuts the active carrier
cut c1, c2, c3; // cuts each of the listed carriers
cut [1, c2, 3], Carrier; // cuts carriers in the list and active carriers
```

Note that all the carriers in use at the end of a knitting program must be cut so that the object can be released from the machine. By default, knit_script will add outhook statements to the knitout for every yarn carrier that is still active at the very end of the program. 

## Gauge and Sheets
So for, we have given examples of using knit script to knit swatches of fabric. It is possible to make use of the two needle beds to create multiple sheets of fabric at once or create objects out of layers of fabric. For example, we can knit a tube of fabric by reversing on the back bed using the following code:

```knit_script
with Carrier as c1, width as 10:{
    cast_ons.alt_tuck_cast_on(width, is_front=True);
	cast_ons.alt_tuck_cast_on(width, is_front=False);

	for r in range(0, height):{
		in reverse direction:{
			knit Front_Loops;
		}
		in reverse direction:{
			knit Back_Loops;
		}
	}
}
```

Note that this tube will knit stockinette on the front bed loop and reverse stockinette on the back bed loops. The final tube will have knits facing outwards and purls facing outwards. But what if we want to make a tube of knit-purl ribbing. The purls in the texture will take up space on the back bed. Instead, we will need to knit at half-gauge, knitting the front of the tube on even needles and the back of the tube on odd needles. This results in the cumbersome code below:

```knit_script
with width as 12, height as 10, Carrier as 1:{

    // Collect needles for the front and back of the tube split up by stitch type. Knits on front needles, purl on back needles
    knit_front_tube = [n for n in Front_Needles[0:width:4]];
    purl_front_tube_back_needles = [n for n in Back_Needles[2:width:4]];
    purl_front_tube_front_needles = [n.opposite() for n in purl_front_tube_back_needles];//[n for n in Front_Needles[2:width:4]];

    knit_back_tube_front_needles = [n for n in Front_Needles[1:width:4]];
    knit_back_tube_back_needles = [n.opposite() for n in knit_back_tube_front_needles];
    purl_back_tube = [n for n in Back_Needles[3:width:4]];

    // cast on each side of the tube. Standard cast ons are not designed for half gauge so we have to do it manually
    in Leftward direction:{
        tuck purl_front_tube_front_needles;
    }
    in reverse direction:{
        tuck knit_front_tube;
    }
    in reverse direction:{
        tuck knit_back_tube_back_needles;
    }
    in reverse direction:{
        tuck purl_back_tube;
    }


    for r in range(0, height):{
        xfer purl_front_tube_front_needles across to back bed; // send front of tube cast ons to be back bed to be purled
        // knit front of the tube
        in reverse direction:{
            knit knit_front_tube;
            knit purl_front_tube_back_needles; // Note: knits and purls will merge to alternate based on bed order
        }
        xfer purl_front_tube_back_needles across to front bed; // move front tube purls out of way of back of tube knitting
        xfer knit_back_tube_back_needles across to front bed; // return knits back bed to their position on front bed needles
        // knit back of tube
        in reverse direction:{
            knit knit_back_tube_front_needles;
            knit purl_back_tube;
        }
        xfer knit_back_tube_front_needles across to back bed; // move back of tube knits out of way of front of tube knitting
    }
}
```

Working in half-gauge requires us to manually keep track of a variety of details that knit script is designed to avoid. Because of this, knit script has support for gauging build directly into the language. 

We introduce two concepts into the language: Gauge and Sheets. 

Gauge is a spacing schema for the needles, allowing us to skip over needles.
For instance, to knit at half-gauge we set the `Gauge` to 2.
This will cause us to skip every other needle.
To knit at a third gauge we set `Gauge` to 3, and so on.
Note that you do not generally want to work at large gauges (i.e., > 4) because this creates unseemly long floats.
Knit Script won't stop you though, so try it out on your machine.
Gauge defaults to 1 (full gauge) so that we knit on every needle.

So if we set the Gauge to 2 we will only b knitting on the even needles. Consider this simple KnitScript, which knits the first four front needles at half-gauge:

```knit_script
with Gauge as 2, Carrier as 1:{
    in Rightward direction:{
        knit Front_Loops[0:4];
    }
}
```
This will produce the following knitout:
```knitout
knit + f0 1;
knit + f2 1;
knit + f4 1;
knit + f6 1;
```

Sheets allow us to knit on different groups of gauged needles. By default, we knit on sheet 0, the set of needles starting at 0 on the right side. But if we want to knit on other sections, we can set the working `Sheet` to any integer modifier. For example, we could knit the first four odd front needles using this code:

```knit_script
with Gauge as 2, Sheet as 1, Carrier as 1:{
    in Rightward direction:{
        knit Front_Loops[0:4];
    }
}
```
This will produce the following knitout:
```knitout
knit + f1 1;
knit + f3 1;
knit + f5 1;
knit + f7 1;
```

You can switch between different sheets by changing the `Sheet` variable. This will throw an error if the sheet you are using is not in the current `Gauge`. For example, we cannot knit on sheet 1 if we only have 1 Gauge (full gauge). 

Changing sheets will have hidden effects. To prevent sheets from crossing over each other, we need the other sheets to be on the outside of the course being worked. Recall that the ribbed tube has xfer lines to move the back knits and front purls out of the way and then back into place. Changing between sheets in knit script will keep track of this for you. When working on a sheet you can always assume that the sheet is where you left it and that all other sheets are out of the way. 

With Gauge and Sheets our ribbed tube is much simpler to program. We will knit the front of our tube on sheet 0 and the back of our tube on sheet 1 as follows:
```knit_script
import cast_ons;

with Gauge as 2, Carrier as 1, width as 12, height as 20:{
	// cast on front and back of the tube
	for s in range(0, Gauge):{
		with Sheet as s:{
			cast_ons.alt_tuck_cast_on(width);
		}
	}
	for s in range(0, Gauge):{
		with Sheet as s:{
		    xfer Loops[1::2] across; // xfer every other loop to opposite bed for knit purl pattern
		}
	}
	for r in range(0, height):{
		for s in range(0, Gauge):{
			with Sheet as s:{
				in reverse direction:{
					knit Loops; // only the loops on the active sheet and keeps track of knit-purl pattern
				}
			}
		}
	}
}
```

### Machine vs Sheet Needles
KnitScript uses the same notation as knitout to specify a needle (e.g., `f1`, `b2`). In this gauging schema using those values will assume you are indexing into the sheet, not the whole machine bed. So at `Gauge = 2`, when `Sheet == 0` `f1` will actually produce the needle `f2` on the machine bed. Set `Sheet==1` and `f1` will produce `f3` on the machine bed. But what if you want to access a needle on a different Sheet or you actually mean a specific needle on the machine bed?

You can access a needle from a specific sheet by accessing them with dot notation. Similar to needles, sheets can be specified as `s#` (e.g., `s2` is the sheet at index 2). So, regardless of the value of `Sheet`, we can access the front needle at index 1 of sheet 2 by writing `s2.f1`.

You can access a needle on the machine bed, regardless of the sheet and gauging schema with the keyword `machine`. So to get the real `f1` we write `machine.f1`. Side note: the keyword `machine` access the machine state of the interpreter directly, so if you can take full control of that state as though you are writing python code. 

If you want to know the sheet of a given needle, you can also get this from `machine` as follows: `machine.sheet_of(n)`

### Layering Sheets
In the prior example, there is an implicit layering of sheets used to form a tube.
The first (front) layer of the tube is knit on sheet 0 and the second (back)
layer of the tube is knit on sheet 1. But what if we don't want to keep this layering consistent across the whole set of needles on a sheet?
For example, we could split our tube into two pieces with the first sheet in front of half the needles and in the back for the second half of needles. 

You can explicitly set the layer of a given needle using `push` statements, the last knit script control structure we will go over.

By default, each needle will be on the same layer as the sheet it is on. For example, at `Gauge=2` the needles on sheet 0 (even needles) will be on layer 0 (the front layer) and the needles on sheet 1 (odd needles) will be on layer 1 (the back layer). 

With a push statement, we can change the layering for specific needles. For example, we can set a list of needles `first_needles` to be on the front layer (0) and the `second_needles' to be on the back layer (1) with the following statements:

```knit_script
push first_needles to layer 0;
push second_needles to layer 1;
```

We can also push needles to layers forward and backwards from their current position:
```knit_script
push first_needles 1 forward;
push second_needles 1 backward;
```

Finally, we can push a layer all the way to the `front` or `back` of the pattern:
```knits_script
push first_needles to front;
push second_needles to back;
```

Note that when we set a needle layer, we affect the needles at the same position in all other sheets.
So for example, if we have 2 sheets (i.e., `Gauge=2`) and we set the layer of f1 in sheet 0 to be 1 then we will also be setting the layer of f1 in sheet 1 to be 1. Two needles at equivalent positions in different sheets cannot have the same layer position because this will create xfer conflicts.
Knit Script handles this for you.
In practice, the difference between the current layer of your needle and the layer you are setting it to will be applied to all other needles in the same position in each sheet.
Note that because all the sheets will cycle layers by the same amount it usually doesn't matter what the value of `Sheet` is when you are using push statements though you may want
to set it specifically if you are 

Let's consider the following example where we are making our stockinette tube but switching the order of the layers halfway across the tube.
This will make two connect tubes, the first with stockinette facing out and the second with reverse stockinette facing out:

```knit_script
import cast_ons;
with Gauge as 2, Carrier as 1, width as 10, height as 20:{
    // cycle layers for first half of working needles
    push Front_Needles[0:width/2] to back;
    // cast on front and back of the tube
	for s in range(0, Gauge):{
		with Sheet as s:{
			cast_ons.alt_tuck_cast_on(width, is_front=s%2==0);
		}
	}
	for r in range(0, height):{
	    for s in range(0, Gauge):{
	        with Sheet as s:{
	            in reverse direction:{
	                knit Loops;
	            }
	        }
	    }
	}
}
```

You may not always want to cycle layer positions with a push. Your other option is to swap layer values between two needles at the same position in a sheet or with a specific layer. 

Let's say that you have 3 sheets (0, 1, 2) and 3 needles at the same position on those sheets: needle a on sheet 0, needle b on sheet 1, needle c on sheet 2. Their starting layers are the same as the sheet order (e.g., a on sheet 0 at layer 0). We can swap the layers of a and b in two ways:
```knit_script
swap a with sheet 1; // note that b is on sheet 1
swap a with layer 1; // note that b is set to layer 1
```

If you want to know what the layer of a specific needle is you can access that from the `machine` similar to checking the sheets of needles: `machine.layer_of(n)`.

## Machine Headers
By default, knit script assumes you are converting to knitout to control a Shima Seiki SWG091N2 knitting machine that is 250 needles wide with 10 carriers.
It will position your knitout instructions in the center of the bed and start.
However,
you can change all of these features for your whole program
by starting your knit script program with a header in the same format as [knitout headers](https://textiles-lab.github.io/knitout/knitout.html).

## Set Machine Type:
We currently support either Shima Seiki Whole garment machines or a Kniterate
```knit_script
;;Machine: <machine type being used>; // Options: SWG091N2 or Kniterate
```

## Knitting Position
Set where to place the operations on the needle bed; Left, Center, Right, and Keep are standard values.

```knit_script
;;Position: <position>; //Defaults to Center
```

## Needle Bed Width:
Shima Seiki machines may have different needle bed widths. You can set this as:

```knit_script
;;Width: <Needle Count>; // Defaults to 250 but is machine dependent
```

## Set Maximum Racking
Knit script will throw an error if your knitting operations force a racking beyond the maximum allowed. By default, we allow racking operations of |4.25| or less. You can change this value:

```knit_script
;;Rack: <maximum rack value>;
```


## Carrier Count
You can change the number of carriers on the machine. Note that this is likely dependent on the machine you are using, and you do not need to set this manually.

```knit_script
;;Carriers: <Carrier Count>;
```

## Set Inserting Hook Size
You can set the expected size of the yarn-inserting hook (i.e., how many needles it blocks).
This should be dependent on the machine, and you likely do not need to set this.
Setting this value to zero will tell the interpreter that there is not yarn-inserting-hook and that other ways of inserting yarns must be used.

```knit_script
;;Hook: <hook size>;
```


# Packages

## knit_graphs
The knit_graphs package holds the components of a Knit_Graph representation of a knitted structure. Knit Graphs are collections of loops connected on yarns and pulled through each other to form a node-link graph structure. Networkx graphs are used to represent yarns and knit graphs. This provides a variety of common graph algorithms for manipulating and searching in a knit graph. For more details on Loop-based knit graphs reference [KnitPick](https://dl.acm.org/doi/abs/10.1145/3332165.3347886)

## knitting_machine
The knitting_machine package holds components of the machine state for a v-bed knitting machine. Knitout operations can be performed on this virtual machine set which will either produce a knit graph representing the knitted object or result in machine knitting errors. For more details on the basic representations of a knitting machine reference [a compiler for Machine Knitting](https://dl.acm.org/doi/10.1145/2897824.2925940). For more details on knitout operations, reference the [knitout specification](https://textiles-lab.github.io/knitout/knitout.html).

## interpreter
The knit script interpreter which manages parsing and interpreting knit_script patterns. Parsing is managed through the [Parglare parsing toolkit](http://www.igordejanovic.net/parglare/0.16.0/).

## tests
Test classes for evaluating the interpreter and parsing knit_script samples. Calibration samples are used for calibrating allowable gauge on a machine. Paper samples demonstrate different basic techniques of sheet knitting. 
