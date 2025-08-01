"""Tests associated with the parsing of the language. Does not interpret the code"""
import random
from unittest import TestCase

from virtual_knitting_machine.Knitting_Machine_Specification import Knitting_Machine_Type

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.expressions.needle_set_expression import Needle_Sets
from knit_script.knit_script_interpreter.Machine_Specification import Xfer_Direction, Machine_Bed_Position
from knit_script.knit_script_interpreter.statements.Statement import Expression_Statement


class Test_KnitScript_Parser(TestCase):
    interpreter = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def _parse_program(self, program: str):
        print(f"Testing:\n{program}")
        statements = self.interpreter.parse(program)
        for statement in statements:
            if isinstance(statement, Expression_Statement):
                print(f"Expression Statement <{statement}> of value {statement.expression} of type {statement.expression.__class__.__name__}")
            else:
                print(f"<{statement}> of type {statement.__class__.__name__}")
        return statements

    def test_numbers(self):
        for _ in range(0, 10):
            float_value = random.uniform(-100.0, 100.0)
            self._parse_program(f"{float_value};")
            self._parse_program(f"{int(float_value)};")

    def test_bools(self):
        self._parse_program("True;")
        self._parse_program("False;")

    def test_none(self):
        self._parse_program("None;")

    def test_strings(self):
        self._parse_program(""" "string"; """)
        self._parse_program(""" "string with (;)";""")
        self._parse_program(""" "string with number 1242343.23232"; """)
        self._parse_program(""" "string with symbols - -- _ + * ^ $ % # ! '' " ;""")

    def test_lhs_rhs_expression(self):
        self._parse_program("len(string) == 14;")
        self._parse_program("value != bool;")
        self._parse_program(" value + value;")
        self._parse_program(" value - value;")
        self._parse_program(" value * value;")
        self._parse_program(" value / value;")
        self._parse_program(" value ^ value;")
        self._parse_program(" value % value;")

    def test_list_expression(self):
        self._parse_program("[1,2,3];")
        self._parse_program("""[1,2,True, "string"];""")

    def test_nested_expression(self):
        self._parse_program("len(len(list_value));")

    def test_standard_values(self):
        for pos in Xfer_Direction:
            self._parse_program(f"{pos.value};")
        for mt in Knitting_Machine_Type:
            self._parse_program(f"{mt.value};")
        for ns in Needle_Sets:
            self._parse_program(f"{ns.value};")
        for pos in Machine_Bed_Position:
            self._parse_program(f"{pos.value};")

    def test_rack_statement(self):
        self._parse_program("Rack = 2;")
        self._parse_program("Rack = -2.1;")
        self._parse_program("Rack = old_rack;")

    def test_carrier(self):
        self._parse_program("Carrier = 2;")
        self._parse_program("Carrier = -2;")
        self._parse_program("Carrier = c1;")
        self._parse_program("Carrier = [1,3];")
        self._parse_program("Carrier = [c4, c2];")

    def test_xfer(self):
        self._parse_program("xfer n across;")
        self._parse_program("xfer [n] across;")
        self._parse_program("xfer n 1 to Left;")
        self._parse_program("xfer [n] 1 to Right;")
        self._parse_program("xfer [n] 1 to Leftward;")
        self._parse_program("xfer n 1 to Rightward;")
        self._parse_program("xfer n across to Front bed;")
        self._parse_program("xfer n across to Back bed;")
        self._parse_program("xfer [n] 1 to Left to Back bed;")
        self._parse_program("xfer [n] 2 to Leftward;")
        self._parse_program("xfer [f1,f2, f3] across to Front bed sliders;")
        self._parse_program("xfer Back_Loops[1::2] across to Back bed sliders;")

    def test_iter(self):
        self._parse_program("[n for n,q in Front_Needles if n==f2];")
        self._parse_program("{k:v for n,v in Front_Needles if n==f2};")
        self._parse_program("vals = [n.opposite() for n in other_vals];")

    def test_assert(self):
        self._parse_program("""assert True, "test true";""")
        self._parse_program("""assert True;""")
        self._parse_program("""assert False, "test false";""")
        self._parse_program("""assert False;""")
        self._parse_program("""assert a==False;""")

    def test_print(self):
        program = r"""
        print "test";
        print 1.0;
        print a;
                """
        self._parse_program(program)

    def test_try(self):
        self._parse_program("""try: {assert True;} catch: {a="False";}""")
        self._parse_program("""try: {assert False;} catch: {a="False";}""")
        self._parse_program("""try: {assert False;} catch KeyError as e: {a="False";}""")
        program = r"""
        try: {print c;}
        catch Exception as e: { print "no c yet :)";}"""
        self._parse_program(program)

    def test_if(self):
        program = r"""
                if index <2 : {assert True;}
                if True: {assert True;}
                else: {print True;}
                if True: {assert True;}
                elif True: {print True;}
                else: {print False;}
                """
        self._parse_program(program)
        program = """
        if reverse == Leftward:{
            print "leftward pass";
        } else:{
            print "rightward pass";
        }
        """
        self._parse_program(program)

    def test_method_call(self):
        self._parse_program("opposite();")
        self._parse_program("n.x();")
        self._parse_program("b.a(f[1],v.f[1]);")
        self._parse_program("b.a(cat=f[1], dog=2);")
        self._parse_program("b.a(f[1],v.f[1], cat=f[1], dog =2);")

    def test_iteration_blocks(self):
        program = r""" while cat > dog: {print True;} """
        self._parse_program(program)
        program = r""" for e in cat: {assert False;}  """
        self._parse_program(program)

    def test_in_direction_statements(self):
        program = r"""
                        in dir direction:{ knit f1;}
                        in current direction:{ knit f1;}
                        in Leftward direction:{
                            tuck b3, bs4, fs16;
                        }
                        in <-- direction:{
                            tuck b3, bs4, fs16;
                        }
                        in reverse direction:{
                            tuck b3, bs4, fs16;
                        }"""
        self._parse_program(program)

    def test_function_declaration(self):
        program = r"""
                      def func(a, b=True):{
                        assert True;
                        return True;
                      }
                      value = func(1, b=1);"""
        self._parse_program(program)

    def test_slices_and_indexing(self):
        self._parse_program("indexable[i];")
        self._parse_program("sliceable[s:e];")
        self._parse_program("sliceable[s:e:sp];")
        self._parse_program("sliceable[:e];")
        self._parse_program("sliceable[:e:sp];")
        self._parse_program("sliceable[s::sp];")
        # TODO: Fix slicing to include open ended slicing
        # self._parse_program("sliceable[s:];")

    def test_import(self):
        program = r"""
            import knit_script.knitting_machine.machine_components.needles as needles;
            cat = needles.Needle(True, 1);
        """
        self._parse_program(program)

    def test_accessor(self):
        self._parse_program("cat.dog;")
        self._parse_program("cat.dog.bird;")
        self._parse_program("cat.dog.bird();")
        self._parse_program("cat.dog.bird[1];")

    def test_order_of_operations(self):
        self._parse_program(f" (p - p)^e * m / d + a - s;")
        statements = self._parse_program(" (2 - 1)^0 * 1 / 1 + 1 - 1;")
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert 1 == self.interpreter.knit_script_evaluate_expression(statement.expression)
        statements = self._parse_program("2 < 0;")
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.interpreter.knit_script_evaluate_expression(statement.expression)
        statements = self._parse_program("2 <= 0;")
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.interpreter.knit_script_evaluate_expression(statement.expression)
        statements = self._parse_program("2 > 0;")
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.interpreter.knit_script_evaluate_expression(statement.expression)
        statements = self._parse_program("2 >= 0;")
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.interpreter.knit_script_evaluate_expression(statement.expression)
        statements = self._parse_program("2 == 0;")
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.interpreter.knit_script_evaluate_expression(statement.expression)
        statements = self._parse_program("2 != 0;")
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.interpreter.knit_script_evaluate_expression(statement.expression)
        self._parse_program("not 2 < 0;")

    def test_with(self):
        # warning note: seems to be a parsing issue. The statement runs fine
        program = "with Rack as 2, Carrier as a: {assert False;}"
        self._parse_program(program)

    def test_needle_accessor(self):
        program = r"""
            machine.f2;
            s0.b2;
            s1:g2.bs10;
        """
        self._parse_program(program)

    def test_sheet_accessor(self):
        self._parse_program("s1.f1;")
        self._parse_program("machine.f0;")

    def test_global(self):
        self._parse_program("global cat=dog;")

    def test_layers(self):
        self._parse_program("push f1 to layer 2;")
        self._parse_program("push f1 to Front;")
        self._parse_program("push f1 2 backward;")
        self._parse_program("swap f1 with layer 1;")
        self._parse_program("swap f1 with sheet 3;")
