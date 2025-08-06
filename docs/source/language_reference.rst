Language Reference
==================

Complete syntax reference for the KnitScript programming language.

📝 Basic Syntax
---------------

Comments
~~~~~~~~

KnitScript uses double-slash comments like Java or JavaScript:

.. code-block:: knitscript

   // This is a single-line comment
   width = 20;  // End-of-line comment

Variable Assignment
~~~~~~~~~~~~~~~~~~~

Variables are dynamically typed following Python conventions:

.. code-block:: knitscript

   // Basic types
   width = 20;              // Integer
   gauge_size = 14.5;       // Float
   yarn_color = "blue";     // String
   is_finished = True;      // Boolean

   // Collections
   needle_list = [1, 2, 3, 4];           // List
   pattern_dict = {"a": 1, "b": 2};      // Dictionary

String Formatting
~~~~~~~~~~~~~~~~~

KnitScript supports Python-style f-string formatting:

.. code-block:: knitscript

   name = "scarf";
   width = 20;
   print f"Knitting {name} with {width} stitches";

   // Multi-expression formatting
   message = f"Pattern: {name}, Width: {width}, Total: {width * 2}";

List and Dictionary Comprehension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can construct lists and dictionaries using python style comprehensions:

.. code-block:: knitscript

    every_other_loop = [l for l in Loops[::2]];
    dictionary_of_loops = {fl:Back_Needles[fl.position] for fl in Front_Loops};
	list_with_condition = [bl for bl in Back_Loops if bl.position % 2 == 0];

🔧 Variables and Scoping
------------------------

Local Variables
~~~~~~~~~~~~~~~

Variables declared in functions are local to that scope:

.. code-block:: knitscript

   def knit_rectangle(width, height):{
       row_count = 0;  // Local variable
       for row in range(height):{
           in reverse direction:{ knit Loops; }
           row_count += row_count + 1;
       }
       return row_count;
   }

Machine State Variables
~~~~~~~~~~~~~~~~~~~~~~~

Special variables control machine configuration:

.. code-block:: knitscript

   Gauge = 2;         // Number of sheets to work with
   Sheet = 0;         // Active sheet (0 to Gauge-1)
   Carrier = c1;      // Active carrier
   Racking = 0.0;     // Bed alignment. Negative values are leftward. Positive values are rightward.

🎛️ Control Flow
---------------

Conditionals
~~~~~~~~~~~~

Standard if-else statements:

.. code-block:: knitscript

   if width > 20:{
       print "Wide pattern";
   }
   elif width > 10:{
       print "Medium pattern";
   }
   else:{
       print "Narrow pattern";
   }

Loops
~~~~~

**For loops** with ranges:

.. code-block:: knitscript

   // Range-based iteration
   for row in range(10):{
       in reverse direction:{ knit Loops; }
   }

   // Collection iteration
   for needle in Front_Needles[0:10]:{
       print needle;
   }

   // Multiple variables (unpacking)
   coordinates = [[0, 5], [1, 6], [2, 7]];
   for x, y in coordinates:{
       print f"Position: {x}, {y}";
   }

**While loops**:

.. code-block:: knitscript

   row = 0;
   while row < height:{
       in reverse direction:{ knit Loops; }
       row = row+1;
   }

🔨 Functions
------------

Function Definition
~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Function with parameters and defaults
   def cable_cross(width = 4, cable_dir = "right"):{
       if dir == "cable_dir":{
           xfer Front_Needles[0:width/2] 2 to Right to back bed;
       }
       else:{
           xfer Front_Needles[width/2:width] 2 to Left to back bed;
       }

       in reverse direction:{ knit Loops; }

       xfer Back_Loops across to front bed;
       return width;
   }

Function Calls
~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Call with positional arguments
   cable_cross(8);

   // Call with keyword arguments
   cable_cross(width=6, cable_dir="left");

   // Mixed arguments
   cable_cross(8, cable_dir="left");

Return Values
~~~~~~~~~~~~~

.. code-block:: knitscript

   def calculate_remainder(total_width, pattern_width):{
       remainder = total_width % pattern_width;
       return remainder;
   }

   // Use return values
   extra = calculate_remainder(40, 6);
   print f"Pattern has {extra} extra stitches";

🧶 Machine Operations
---------------------

Basic Stitching
~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Knit all loops in Rightward direction
   in Rightward direction:{ knit Loops; }

   // Knit and Tuck specific needles
   in Leftward direction:{
       knit Front_Needles[0:10];
       tuck Back_Needles[5:15];
   }


Transfer Operations
~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Direct across-bed transfers
   xfer Loops across;

   // Direct across-bed to a specified bed.
   xfer Front_Loops across to Back bed;

   // Offset transfers
   xfer Front_Needles[0:10] 2 to Right to Back bed;
   xfer Back_Needles[10:20] 1 to Left to Front bed;

   // Transfer to sliders
   xfer Front_Loops across sliders;

Drop Operations
~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Drop specific needles
   drop Front_Needles[0:5];

   // Drop all loops on a bed
   drop Back_Loops;

🎯 Needle Selection
-------------------

Built-in Needle Sets
~~~~~~~~~~~~~~~~~~~~

KnitScript provides convenient needle set variables:

.. code-block:: knitscript

   Front_Needles      // All front bed needles
   Back_Needles       // All back bed needles
   Front_Sliders      // All front slider needles
   Back_Sliders       // All back slider needles

   Loops              // All needles with loops (set starts with front bed loops, then back bed loops
   Front_Loops        // Front needles with loops
   Back_Loops         // Back needles with loops

   Slider_Loops       // All loops on slider beds (front then back)
   Front_Slider_Loops // All loops on front slider bed
   Back_Slider_Loops  // All loops on back slider bed

   Needles            // All needles (front then back)
   Sliders            // All slider needles (front then back)

   Last_Pass          // The needles involved in the last carriage pass in the order of operation. Xfer passes produce a dictionary of start-needles to target needles

Array Slicing
~~~~~~~~~~~~~

Use Python-style slicing to select needle ranges:

.. code-block:: knitscript

   Front_Needles[0:10]     // Needles 0-9
   Front_Needles[5:]       // Needle 5 to end
   Front_Needles[:15]      // Start to needle 14
   Front_Needles[::2]      // Every other needle
   Front_Needles[1:20:3]   // Every 3rd needle from 1 to 19

🔄 Advanced Control Flow
------------------------

Exception Handling
~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   try:{
       assert False;
   }
   catch Exception as e:{
       print f"Assertion failed: {e}";
   }

Assertions
~~~~~~~~~~

.. code-block:: knitscript

   // Validate assumptions
   assert len(Front_Loops) == 0, "Currently holds no loops";
   assert Carrier is None, "No active working carrier set";
   assert (Gauge >= 1) and (Gauge <= 9), "Invalid gauge setting";

With Statements
~~~~~~~~~~~~~~~

Temporarily change variables:

.. code-block:: knitscript

   // Temporarily change machine settings
   with Racking as 1.0, Carrier as 1:{
       xfer Front_Loops across to back bed;
       in reverse direction:{ knit Loops; }
   }
   // Racking and Sheet automatically restored

📚 Operators
------------

Arithmetic Operators
~~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   a = 5 + 3;      // Addition: 8
   b = 10 - 4;     // Subtraction: 6
   c = 6 * 7;      // Multiplication: 42
   d = 15 / 3;     // Division: 5.0
   e = 17 % 5;     // Modulo: 2
   f = 2 ^ 3;      // Exponentiation: 8

Comparison Operators
~~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   a == b    // Equal
   a != b    // Not equal
   a < b     // Less than
   a <= b    // Less than or equal
   a > b     // Greater than
   a >= b    // Greater than or equal
   a is b    // Identity comparison
   a in b    // Membership test

Logical Operators
~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   True and False   // Logical AND: False
   True or False    // Logical OR: True
   not True         // Logical NOT: False

🎨 Data Structures
------------------

Lists
~~~~~

.. code-block:: knitscript

   // List creation
   needles = [f1, f2, f3];
   numbers = [1, 2, 3, 4, 5];
   mixed = [1, "hello", True];

   // List operations
   needles.append(f4);
   length = len(Needles);
   first = Needles[0];

   // List comprehensions
   even_nums = [x for x in range(10) if x % 2 == 0];

Dictionaries
~~~~~~~~~~~~

.. code-block:: knitscript

   // Dictionary creation
   config = {"width": 20, "height": 30};

   // Dictionary access
   w = config["width"];
   config["new_key"] = "value";

   // Dictionary comprehension
   squares = {x: x^2 for x in range(5)};

🔍 Built-in Functions
---------------------

Common Functions
~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Output and debugging
   print("Hello, Python!"); // Will print to Python console only
   print f"Width: {width}"; // Will print to python console and into the knitout code.

   // Type checking from Python Standard Library
   type(width);
   len(Needles);

   // Math functions (from Python)
   abs(-5);        // Absolute value: 5
   min(1, 2, 3);   // Minimum: 1
   max(1, 2, 3);   // Maximum: 3
   range(10);      // Range object: 0-9

📖 Syntax Summary
-----------------

.. list-table:: KnitScript Syntax Quick Reference
   :widths: 30 70
   :header-rows: 1

   * - Construct
     - Syntax
   * - Variable
     - ``variable_name = value;``
   * - Function
     - ``def name(params):{ body }``
   * - If statement
     - ``if condition:{ block } else:{ block }``
   * - For loop
     - ``for var in iterable:{ block }``
   * - While loop
     - ``while condition:{ block }``
   * - Try-catch
     - ``try:{ block } catch Type as var:{ block }``
   * - With statement
     - ``with Variable as value:{ block }``
   * - Carriage pass
     - ``in direction:{ operations; }``
   * - Transfer
     - ``xfer needles distance direction to bed;``
   * - Drop
     - ``drop needles;``

Next: Explore :doc:`machine_operations` for detailed machine control syntax.
