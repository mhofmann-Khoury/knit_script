Quick Start
===========

Get up and running with KnitScript in just a few minutes! This guide will walk you through creating your first knitting pattern.

🎯 Your First Pattern
---------------------

Let's create a simple stockinette pattern to get familiar with KnitScript syntax.

Basic Stockinette
~~~~~~~~~~~~~~~~~

Create a file called ``stockinette.ks``:

.. code-block:: knitscript

   // Simple stockinette scarf pattern
   width = 10;

   with Carrier as c1:{
     in Leftward direction:{
       tuck Front_Needles[0:width:2];
     }
     in reverse direction:{
       tuck Front_Needles[1:width:2];
     }
     for _ in range(10):{
       in reverse direction:{
         knit Loops;
       }
     }
   }
   cut c1;

Now convert it to knitout:

.. code-block:: python

   from knit_script import knit_script_to_knitout

   # Convert pattern to knitout
   knit_graph, machine = knit_script_to_knitout(
       pattern="stockinette.ks",
       out_file_name="stockinette.k"
   )

   print(f"✅ Generated the stockinette pattern")

🧶 Understanding the Pattern
----------------------------

Let's break down what each part does:

Variable Declaration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   width = 10;

This creates a variable ``width`` that we can use throughout our pattern.

Carrier Management
~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   with Carrier as c1:{
       // pattern code here
   }

The ``with Carrier as c1`` block:
* Sets carrier 1 as the active working carrier
* Automatically handles inhook operations when needed
* Scopes the carrier setting to this block

Directional Operations
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   in Leftward direction:{
       tuck Front_Needles[0:width:2];
   }

The ``in direction`` block:
* Sets the carriage pass direction
* Groups multiple operations into a single carriage pass
* Organizes operations to be sorted by the given direction

Needle Selection
~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   Front_Needles[0:width:2]  // Even Needles 0 through 9 on front bed
   Loops                   // All needles currently holding loops

KnitScript provides convenient ways to select needles:
- ``Front_Needles`` / ``Back_Needles``: All needles on a bed
- ``Loops`` / ``Front_Loops`` / ``Back_Loops``: Needles with stitches
- Array slicing: ``[start:end:step]`` like Python

🔄 Adding Complexity
--------------------

Parameterized Patterns
~~~~~~~~~~~~~~~~~~~~~~

Make your pattern configurable by accepting parameters from Python:

.. code-block:: python

   # Python code
   knit_graph, machine = knit_script_to_knitout(
       pattern="stockinette.ks",
       out_file_name="custom_stockinette.k",
       width=20,      # Inject width parameter
       height=50      # Inject height parameter
   )

.. code-block:: knitscript

   // stockinette.ks - now uses injected parameters
   // width and height are available from Python

   with Carrier as c1:{
     in Leftward direction:{
       tuck Front_Needles[0:width:2];
     }
     in reverse direction:{
       tuck Front_Needles[1:width: 2];
     }
     for _ in range(height):{  // Use injected height
       in reverse direction:{
         knit Loops;
       }
     }
   }
   cut c1;

Adding Functions
~~~~~~~~~~~~~~~~

Create reusable components with functions:

.. code-block:: knitscript

   // Function for alternating tuck cast-on
   def alt_tuck_cast_on(width = 10):{
       in Leftward direction:{
         tuck Front_Needles[0:width:2];  // Even needles
       }
       in reverse direction:{
         tuck Front_Needles[1:width:2];  // Odd needles
       }
   }

   // Use the function
   with Carrier as c1:{
     alt_tuck_cast_on(20);  // Cast on 20 stitches

     // Main knitting
     for row in range(50):{
       in reverse direction:{
         knit Loops;
       }
     }
   }
   cut c1;

🎨 Multi-Sheet Knitting
-----------------------

For more complex patterns, try multi-sheet knitting:

.. code-block:: knitscript

   // Two-layer tube pattern
   width = 20;

   with Carrier as c1, Gauge as 2:{
     // Front of tube (Sheet 0)
     with Sheet as s0:{
       in Leftward direction:{
         tuck Front_Needles[0:width:2];
         tuck Back_Needles[1:width:2];
       }
     }

     // Back of tube (Sheet 1)
     with Sheet as s1:{
       in reverse direction:{
         tuck Front_Needles[0:width:2];
         tuck Back_Needles[1:width:2];
       }
     }

     // Knit both layers
     for _ in range(30):{
       with Sheet as s0:{
         in reverse direction:{ knit Loops; }
       }
       with Sheet as s1:{
         in reverse direction:{ knit Loops; }
       }
     }
   }
   cut c1;

🔧 Development Workflow
-----------------------

1. **Install KnitScript**:

   .. code-block:: bash

      pip install knit-script

2. **Create your first pattern**:

   Create ``my_pattern.ks`` with your KnitScript code.

3. **Test and iterate**:

   .. code-block:: python

      from knit_script import knit_script_to_knitout

      # Test your pattern
      try:
          knit_graph, machine = knit_script_to_knitout(
              pattern="my_pattern.ks",
              out_file_name="output.k"
          )
          print("✅ Pattern compiled successfully!")
      except Exception as e:
          print(f"❌ Error: {e}")

🎯 Next Steps
-------------

Now that you have KnitScript installed:

1. **Learn the syntax**: Read the :doc:`language_reference` for full documentation

Need Help?
----------

- 📖 **Documentation**: Complete language reference in :doc:`language_reference`
