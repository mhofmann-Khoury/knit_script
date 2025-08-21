Machine Operations
==================

Detailed guide to machine control operations in KnitScript.

🧶 Basic Stitching Operations
-----------------------------

Knitting
~~~~~~~~

The ``knit`` operation creates new loops and stitches them through old ones on the specified needle:

.. code-block:: knitscript

   // Knit all loops on Front bed
   in Rightward direction:{ knit Front_Loops; }

   // Knit specific needles
   in Leftward direction:{ knit Front_Needles[0:10]; }

   // Knit all loops regardless of bed
   in reverse direction:{ knit Loops; }

Tucking
~~~~~~~

The ``tuck`` operation creates new loops while keeping old ones on the specified needle:

.. code-block:: knitscript

   // Alternating tuck cast-on
   in Leftward direction:{
	   tuck Front_Needles[0:width:2];  // Even needles
   }
   in Rightward direction:{
	   tuck Front_Needles[1:width:2];  // Odd needles
   }

Missing
~~~~~~~

The ``miss`` operation moves carriers to a specified needle without forming loops:

.. code-block:: knitscript

   // Miss needles to position carrier
   in Rightward direction:{
	   miss Front_Needles[5:15];
   }

🔄 Transfer Operations
----------------------

Across-Bed Transfers
~~~~~~~~~~~~~~~~~~~~

Transfer loops directly between front and back beds:

.. code-block:: knitscript

   // Transfer all front loops to Back bed
   xfer Front_Loops across to Back bed;

   // Transfer specific needles
   xfer Front_Needles[0:10] across to Back bed;

   // Transfer to Front bed
   xfer Back_Loops across to Front bed;

   // Transfer all loops only to Back bed. Back bed loops stay in place
   xfer Loops across to Back bed;

Offset Transfers
~~~~~~~~~~~~~~~~

Transfer with horizontal offset (Racking localized to xfers):

.. code-block:: knitscript

   // Transfer 2 needles to the Right
   xfer Front_Needles[0:8] 2 to Right to Back bed;

   // Transfer 1 needle to the Left
   xfer Back_Needles[10:20] 1 to Left to Front bed;

   // Variable offset
   offset = 3;
   xfer Front_Loops offset to Right to Back bed;

Slider Transfers
~~~~~~~~~~~~~~~~

Transfer to slider needles for temporary holding:

.. code-block:: knitscript

   // Transfer to sliders
   xfer Front_Needles[0:5] across to sliders;

   // Transfer loops moved to sliders back to Front bed.
   xfer Last_Pass.values() across to Front bed;

Split Operations
~~~~~~~~~~~~~~~~

The ``split`` operation creates loops on one needle while moving existing loops to another:

.. code-block:: knitscript

   in Rightward direction:{
	   split Front_Needles[5:10];  // Splits loops and creates new ones on the opposite position
   }

🗑️ Drop Operations
------------------

Basic Dropping
~~~~~~~~~~~~~~

Remove loops from needles:

.. code-block:: knitscript

   // Drop specific needles
   drop Front_Needles[0:5];

   // Drop all loops on a bed
   drop Front_Loops;
   drop Back_Loops;

   // Drop everything
   drop Loops;

🎨 Carrier Management
---------------------

Setting Active Carrier
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Single carrier
   Carrier = c1;

   // Multiple carriers for platting
   Carrier = [c1, c2];

   // Using with statement for scoped carrier work
   with Carrier as c2:{
	   in reverse direction:{ knit Loops; }
   }

Carrier Operations
~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Cut carriers (outhook)
   cut c1;              // Cut specific carrier
   cut [c1, c2];        // Cut multiple carriers
   cut Carrier;         // Cut current working carrier

   // Release yarn hook
   releasehook;         // Release current hooked carrier. If no yarn is hooked, this is a safe no-op.

🎯 Direction Control
--------------------

Direction Keywords
~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Explicit directions
   in Rightward direction:{ knit Loops; }
   in Leftward direction:{ knit Loops; }

   // Contextual directions
   in reverse direction:{ knit Loops; }    // Opposite of last directed carriage pass (ignores xfer passes)
   in current direction:{ knit Loops; }    // Same as last directed carriage pass (ignores xfer passes)

	//Preserve a direction in a variable
	var_dir = current;
	with Carrier as c1:{
		in Leftward direction: {knit Front_Loops;}
	}
	with Carrier as c2:{
		in var_dir: {knit Back_Loops;}
	}

📐 Racking and Positioning
--------------------------

Racking Control
~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Set racking position
   Racking = 0.0;    // Aligned beds. This is the default racking
   Racking = 1.0;    // Front bed 1 needle Right
   Racking = -2.0;   // Front bed 2 needles Left

All-Needle Operations
~~~~~~~~~~~~~~~~~~~~~

If operations require all-needle racking, KnitScript will automatically adjust the racking for that carriage pass.

.. code-block:: knitscript

   // Operations that might need all-needle racking
   in Rightward direction:{
	   knit Front_Needles[10];
	   knit Back_Needles[10];  // Same position - needs all-needle
   }

📊 Multi-Sheet Operations
-------------------------
Use Gauge and sheets to independently knit structures with multiple layers.

Common example is knitting a tube in half-gauge to use knit-purl patterns such as ribbing.

Seetting the gauge will determine the number of working sheets.
Each sheet will work on needle slots with spacing defined by the gauge.

Gauge Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Set number of sheets
   Gauge = 2;    // 2 sheets (a.k.a., half-gauge)

   // Sheet selection
   Sheet = 0;    // First sheet knit on even needle slots
   Sheet = 1;    // Second sheet knit on odd needle slots

Sheet-Scoped Operations
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // comment fixes with warning in pycharm?
		with Gauge as 2:{
		   // Work on sheet 0
		   with Sheet as s0:{
			   in Leftward direction:{
				tuck Front_Needles[0:width:2]; // note that front_needles is localized to the working sheet
				tuck Back_Needles[1:width:2]; // note that back_needles is localized to the working sheet
			   }
		   }

		   // Work on sheet 1
		   with Sheet as s1:{
			   in reverse direction:{
				tuck Front_Needles[0:width:2]; // note that front_needles is localized to the working sheet
				tuck Back_Needles[1:width:2]; // note that back_needles is localized to the working sheet
			   }
		   }

		   // Knit both sheets alternately to form a tube
		   for row in range(height):{
			   with Sheet as s0:{
				   in reverse direction:{ knit Loops; }
			   }
			   with Sheet as s1:{
				   in reverse direction:{ knit Loops; }
			   }
		   }
	   }

Layer Management
~~~~~~~~~~~~~~~~

Control the layering order of sheets:

.. code-block:: knitscript

	Gauge = 2;
	Sheet = 0;
	// Push needles to different layers
   push Front_Needles[0:10] to Front;    // Bring to first 10 needle slots of this sheet to the front of the sheet layers.
   push Front_Needles[10:20] to Back;    // Send the next 10 needle slots of this sheet to the back of the sheet layers.

   Gauge = 3;
   Sheet = 0;
   // Push by distance
   push Front_Needles[5:15] 1 Backward;  // Move 1 layers backward (to be in the center at these layers
   Sheet = 2;
   push Back_Needles[0:5] 2 Forward;   // Move 2 layers forward to be in front of all other sheets.

   // Swap layer positions
   swap Front_Needles[0:5] with layer 2; // Set to be 2nd layer over these needle slots.
   swap Front_Needles[10:15] with sheet s1; // Set to trade the layer of sheet 1 at these slots.

🛠️ Machine Control
------------------

Pause Operations
~~~~~~~~~~~~~~~~

.. code-block:: knitscript

   // Pause for manual intervention
   pause;

   // Pause with context
   print "Please check tension";
   pause;
   print "Continuing pattern...";


📋 Operation Reference
----------------------

.. list-table:: KnitScript Machine Operations
   :widths: 20 30 50
   :header-rows: 1

   * - Operation
     - Syntax
     - Description
   * - Knit
     - ``knit needles``
     - Form new loops, consume old ones
   * - Tuck
     - ``tuck needles``
     - Form new loops, keep old ones
   * - Miss
     - ``miss needles``
     - Move carrier without forming loops
   * - Split
     - ``split needles``
     - Create loop and move existing loops
   * - Transfer
     - ``xfer needles [offset] to bed``
     - Move loops between needles
   * - Drop
     - ``drop needles``
     - Remove loops from needles
   * - Cut
     - ``cut carriers``
     - Permanently remove carriers
   * - Remove
     - ``remove carriers``
     - Temporarily remove carriers
   * - Release
     - ``releasehook``
     - Release yarn inserting hook
   * - Pause
     - ``pause``
     - Stop machine execution
