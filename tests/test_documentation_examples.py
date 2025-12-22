import warnings
from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks
from virtual_knitting_machine.knitting_machine_warnings.Needle_Warnings import Knit_on_Empty_Needle_Warning
from virtual_knitting_machine.knitting_machine_warnings.Yarn_Carrier_System_Warning import Yarn_Carrier_Warning


class Test_Documentation_Examples(TestCase):

    def test_lr_comments(self):
        program = r"""
        // This is a single-line comment
        width = 20;  // End-of-line comment
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_var_assignment(self):
        program = r"""
        // Basic types
           width = 20;              // Integer
           gauge_size = 14.5;       // Float
           yarn_color = "blue";     // String
           is_finished = True;      // Boolean

           // Collections
           needle_list = [1, 2, 3, 4];           // List
           pattern_dict = {"a": 1, "b": 2};      // Dictionary
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_fstrings(self):
        program = r"""
        name = "scarf";
       width = 20;
       print f"Knitting {name} with {width} stitches";

       // Multi-expression formatting
       message = f"Pattern: {name}, Width: {width}, Total: {width * 2}";
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_comprehensions(self):
        program = r"""
        every_other_loop = [l for l in Loops[::2]];
        dictionary_of_loops = {fl:Back_Needles[fl.position] for fl in Front_Loops};
        list_with_condition = [bl for bl in Back_Loops if bl.position % 2 == 0];
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_local_variables(self):
        program = r"""
        def knit_rectangle(width, height):{
           row_count = 0;  // Local variable
           for row in range(height):{
               in reverse direction:{ knit Loops; }
               row_count = row_count + 1;
           }
           return row_count;
        }
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_machine_state_variables(self):
        program = r"""
        Gauge = 2;         // Number of sheets to work with
       Sheet = 0;         // Active sheet (0 to Gauge-1)
       Carrier = c1;      // Active carrier
       Racking = 0.0;     // Bed alignment. Negative values are leftward. Positive values are rightward.
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_control_flow(self):
        program = r"""
        width = 5;
        if width > 20:{
           print "Wide pattern";
       }
       elif width > 10:{
           print "Medium pattern";
       }
       else:{
           print "Narrow pattern";
       }
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_for_loops(self):
        program = r"""
        // Range-based iteration
        Carrier = c1;
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
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_while_loops(self):
        program = r"""
        Carrier = c1;
        height = 10;
        row = 0;
           while row < height:{
               in reverse direction:{ knit Loops; }
               row = row + 1;
           }
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_function(self):
        program = r"""
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
       Carrier = c1;
       // Call with positional arguments
       cable_cross(8);

       // Call with keyword arguments
       cable_cross(width=6, cable_dir="left");

       // Mixed arguments
       cable_cross(8, cable_dir="left");
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_return_values(self):
        program = r"""
        def calculate_remainder(total_width, pattern_width):{
           remainder = total_width % pattern_width;
           return remainder;
       }

       // Use return values
       extra = calculate_remainder(40, 6);
       print f"Pattern has {extra} extra stitches";
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_basic_stitching(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=Knit_on_Empty_Needle_Warning)  # Ignore all warnings within this block
            program = r"""
            // Knit all loops in Rightward direction
            Carrier = c1;
           in Rightward direction:{ knit Loops; }

           // Knit and Tuck specific needles
           in Leftward direction:{
               knit Front_Needles[0:10];
               tuck Back_Needles[5:15];
           }
           releasehook;
            """
            interpret_test_ks(program)

    def test_lr_transfer_ops(self):
        program = r"""
        // Direct across-bed transfers
       xfer Loops across;

       // Direct across-bed to a specified bed.
       xfer Front_Loops across to Back bed;

       // Offset transfers
       xfer Front_Needles[0:10] 2 to Right to Back bed;
       xfer Back_Needles[10:20] 1 to Left to Front bed;

       // Transfer to sliders
       xfer Front_Loops across sliders;
       """
        interpret_test_ks(program)

    def test_lr_drops(self):
        program = r"""
        // Drop specific needles
       drop Front_Needles[0:5];

       // Drop all loops on a bed
       drop Back_Loops;
        """
        interpret_test_ks(program)

    def test_lr_array_slicing(self):
        program = r"""
        print Front_Needles[0:10];     // Needles 0-9
        print Front_Needles[5:];       // Needle 5 to end
        print Front_Needles[:15];      // Start to needle 14
        print Front_Needles[::2];      // Every other needle
        print Front_Needles[1:20:3];   // Every 3rd needle from 1 to 19
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_exceptions(self):
        program = r"""
        try:{
           assert False;
       }
       catch Exception as e:{
           print f"Assertion failed: {e}";
       }
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_assertions(self):
        program = r"""
        // Validate assumptions
       assert len(Front_Loops) == 0, "Currently holds no loops";
       assert Carrier is None, "No active working carrier set";
       print Gauge;
       assert (Gauge >= 2) and (Gauge <= 9), "Invalid gauge setting";
        """
        try:
            interpret_test_ks(program, print_k_lines=False)
        except AssertionError as _e:
            pass

    def test_lr_withs(self):
        program = r"""
        // Temporarily change machine settings
        with Racking as 1.0, Carrier as 1:{
           xfer Front_Loops across to back bed;
           in reverse direction:{ knit Loops; }
        }
        // Racking and Sheet automatically restored
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_arithmetic(self):
        program = r"""
        a = 5 + 3;      // Addition: 8
           b = 10 - 4;     // Subtraction: 6
           c = 6 * 7;      // Multiplication: 42
           d = 15 / 3;     // Division: 5.0
           e = 17 % 5;     // Modulo: 2
           f = 2 ^ 3;      // Exponentiation: 8
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_lists(self):
        program = r"""
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
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_dicts(self):
        program = r"""
        // Dictionary creation
       config = {"width": 20, "height": 30};

       // Dictionary access
       w = config["width"];
       config["new_key"] = "value";

       // Dictionary comprehension
       squares = {x: x^2 for x in range(5)};
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_lr_common_funcs(self):
        program = r"""
        // Output and debugging
       print("Hello, Python!"); // Will print to Python console only
       width = 10;
       print f"Width: {width}"; // Will print to python console and into the knitout code.

       // Type checking from Python Standard Library
       type(width);
       len(Needles);

       // Math functions (from Python)
       abs(-5);        // Absolute value: 5
       min(1, 2, 3);   // Minimum: 1
       max(1, 2, 3);   // Maximum: 3
       range(10);      // Range object: 0-9
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_mo_knit(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=Knit_on_Empty_Needle_Warning)  # Ignore all warnings within this block
            program = r"""
            Carrier = c1;
            // Knit all loops on Front bed
           in Rightward direction:{ knit Front_Loops; }

           // Knit specific needles
           in Leftward direction:{ knit Front_Needles[0:10]; }

           // Knit all loops regardless of bed
           in reverse direction:{ knit Loops; }
           releasehook;
            """
            interpret_test_ks(program)

    def test_mo_tuck(self):
        program = r"""
        Carrier = c1;
        width = 5;
        // Alternating tuck cast-on
       in Leftward direction:{
           tuck Front_Needles[0:width:2];  // Even needles
       }
       in Rightward direction:{
           tuck Front_Needles[1:width:2];  // Odd needles
       }
       releasehook;
        """
        interpret_test_ks(program)

    def test_mo_miss(self):
        program = r"""
        // Miss needles to position carrier
        Carrier = c1;
       in Rightward direction:{
           miss Front_Needles[5:15];
       }
       releasehook;
        """
        interpret_test_ks(program)

    def test_mo_xfer(self):
        program = r"""
        // Transfer all front loops to Back bed
       xfer Front_Loops across to Back bed;

       // Transfer specific needles
       xfer Front_Needles[0:10] across to Back bed;

       // Transfer to Front bed
       xfer Back_Loops across to Front bed;

       // Transfer all loops only to Back bed. Back bed loops stay in place
       xfer Loops across to Back bed;

       // Transfer 2 needles to the Right
       xfer Front_Needles[0:8] 2 to Right to Back bed;

       // Transfer 1 needle to the Left
       xfer Back_Needles[10:20] 1 to Left to Front bed;

       // Variable offset
       offset = 3;
       xfer Front_Loops offset to Right to Back bed;

       // Transfer to sliders
       xfer Front_Needles[1:5] across sliders;

       // Transfer loops moved to sliders back to Front bed.
       xfer Last_Pass.values() across to Front bed;
        """
        interpret_test_ks(program)

    def test_mo_splits(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
           split Front_Needles[5:10];  // Splits loops and creates new ones on the opposite position
       }
       releasehook;
        """
        interpret_test_ks(program)

    def test_mo_drops(self):
        program = r"""
        // Drop specific needles
       drop Front_Needles[0:5];

       // Drop all loops on a bed
       drop Front_Loops;
       drop Back_Loops;

       // Drop everything
       drop Loops;
        """
        interpret_test_ks(program)

    def test_mo_carrier_ops(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=Yarn_Carrier_Warning)  # Ignore all warnings within this block
            program = r"""
            // Single carrier
            Carrier = c1;

           // Multiple carriers for platting
           Carrier = [c1, c2];

           // Using with statement for scoped carrier work
           with Carrier as c2:{
               in Leftward direction:{ tuck Front_Needles[0:10]; }
           }
           releasehook;

           // Cut carriers (outhook)
           cut c1;              // Cut specific carrier
           cut [c1, c2];        // Cut multiple carriers
           cut Carrier;         // Cut current working carrier

           // Release yarn hook
           releasehook;         // Release current hooked carrier. If no yarn is hooked, this is a safe no-op.
            """
            interpret_test_ks(program)

    def test_mo_directions(self):
        program = r"""
        Carrier = c1;
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
            in var_dir direction: {knit Back_Loops;}
        }
        """
        interpret_test_ks(program)

    def test_mo_all_needle(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=Knit_on_Empty_Needle_Warning)  # Ignore all warnings within this block
            program = r"""
            Carrier = c1;
            // Operations that might need all-needle racking
            in Leftward direction:{
               knit Front_Needles[10];
               knit Back_Needles[10];  // Same position - needs all-needle
            }
            """
            interpret_test_ks(program)

    def test_mo_gauge(self):
        program = r"""
        // Set number of sheets
       Gauge = 2;    // 2 sheets (a.k.a., half-gauge)

       // Sheet selection
       Sheet = 0;    // First sheet knit on even needle slots
       Sheet = 1;    // Second sheet knit on odd needle slots
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_mo_tube_gauged(self):
        program = r"""
        Carrier = c1;
        width = 6;
        height = 4;
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
        """
        interpret_test_ks(program)

    def test_mo_layers(self):
        program = r"""
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
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_mo_pause(self):
        program = r"""
        // Pause for manual intervention
       pause;

       // Pause with context
       print "Please check tension";
       pause;
       print "Continuing pattern...";
        """
        interpret_test_ks(program)
