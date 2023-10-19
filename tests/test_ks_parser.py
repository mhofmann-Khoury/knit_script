"""Tests associated with the parsing of the language. Does not interpret the code"""
from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.expressions.needle_set_expression import Needle_Sets
from knit_script.knitting_machine.machine_specification.Machine_Type import Machine_Type
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID
from knit_script.knit_script_interpreter.statements.Statement import Expression_Statement
from knit_script.knitting_machine.machine_components.machine_position import Machine_Bed_Position, Machine_Position


class Test_KnitScript_Parser(TestCase):
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_rack_statement(self):
        program = r"""Rack = 2;"""
        statements = self.parser.parse(program)
        print(statements)

    def test_parser(self):
        program = r"""
def alt_tuck_needle_set(co_needles, co_dir=Leftward):{
    if co_dir == Leftward:{
        in co_dir direction:{
            tuck co_needles[1::2];
        }
        in reverse direction:{
            tuck co_needles[0::2];
        }
    } else:{
        in co_dir direction:{
            tuck co_needles[0::2];
        }
        in reverse direction:{
            tuck co_needles[1::2];
        }
    }
}
        """
        statements = self.parser.parse(program)
        print(statements)

    def test_values(self):
        program = "1.2;"
        statements = self.parser.parse(program)
        print(statements)
        program = "12;"
        statements = self.parser.parse(program)
        print(statements)
        program = "-45;"
        statements = self.parser.parse(program)
        print(statements)
        program = "-9.87;"
        statements = self.parser.parse(program)
        print(statements)
        program = "True;"
        statements = self.parser.parse(program)
        print(statements)
        program = "False;"
        statements = self.parser.parse(program)
        print(statements)
        program = "None;"
        statements = self.parser.parse(program)
        print(statements)
        program = """ "string test with some 1.034908 _ -- ; '' " ; """
        statements = self.parser.parse(program)
        print(statements)
        program = """ len("len(str) == 14") ; """
        statements = self.parser.parse(program)
        print(statements)
        program = """[True, "string", 1.0];"""
        statements = self.parser.parse(program)
        print(statements)
        program = f"{Machine_Bed_Position.Back.name};"
        statements = self.parser.parse(program)
        print(statements)
        program = f"{Machine_Position.Center.name};"
        statements = self.parser.parse(program)
        print(statements)
        program = f"{Machine_Position.Left.name};"
        statements = self.parser.parse(program)
        print(statements)
        program = f"{Machine_Type.SWG091N2.name};"
        statements = self.parser.parse(program)
        print(statements)
        program = f"{Header_ID.Width.name};"
        statements = self.parser.parse(program)
        print(statements)
        program = f"{Needle_Sets.Loops.name};"
        statements = self.parser.parse(program)
        print(statements)

    def test_carrier(self):
        program = r'''Carrier = 1;'''
        statements = self.parser.parse(program)
        print(statements)
        program = r'''Carrier = c1;'''
        statements = self.parser.parse(program)
        print(statements)
        program = r'''Carrier = [1, 2];'''
        statements = self.parser.parse(program)
        print(statements)
        program = r'''Carrier = [c2, c1];'''
        statements = self.parser.parse(program)
        print(statements)

    def test_order_of_operations(self):
        program = f" (p - p)^e * m / d + a - s;"
        statements = self.parser.parse(program)
        print(statements)
        program = f" (2 - 1)^0 * 1 / 1 + 1 - 1;"
        statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert 1 == self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 < 0;"
        statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 <= 0;"
        statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 > 0;"
        statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 >= 0;"
        statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 == 0;"
        statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 != 0;"
        statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.parser.knit_script_evaluate_expression(statement.expression)
        program = "not 2 < 0;"
        statements = self.parser.parse(program)
        print(statements)

    def test_xfer(self):
        program = "xfer n across to Front bed sliders;"
        statements = self.parser.parse(program)
        print(statements)
        program = "xfer n, n2 2 to Left to Back bed;"
        statements = self.parser.parse(program)
        print(statements)
        program = "xfer [f1, f2, b3] 4 to Right;"
        statements = self.parser.parse(program)
        print(statements)
        program = "xfer [f1, f2, b3] 4 to Rightward;"
        statements = self.parser.parse(program)
        print(statements)

        program = "xfer Back_Loops[1::2]  1 to left to front bed;"
        statements = self.parser.parse(program)
        print(statements)

    def test_iter(self):
        program = "[n for n,q in Front_Needles if n==f2];"
        statements = self.parser.parse(program)
        print(statements)

        program = "{k:v for n,v in Front_Needles if n==f2};"
        statements = self.parser.parse(program)
        print(statements)

        program = "vals = [n.opposite() for n in other_vals];"
        statements = self.parser.parse(program)
        print(statements)

    def test_assert(self):
        program = """assert True, "test true";"""
        statements = self.parser.parse(program)
        print(statements)
        program = """assert True;"""
        statements = self.parser.parse(program)
        print(statements)
        program = """assert False, "test false";"""
        statements = self.parser.parse(program)
        print(statements)
        program = """assert False;"""
        statements = self.parser.parse(program)
        print(statements)
        program = """assert a==False;"""
        statements = self.parser.parse(program)
        print(statements)

    def test_print(self):
        program = r"""
        print "test";
        print 1.0;
        print a;
                """
        results = self.parser.parse(program)
        print(results)

    def test_try(self):
        program = """try: {assert True;} catch: {a="False";}"""
        results = self.parser.parse(program)
        print(results)
        program = """try: {assert False;} catch: {a="False";}"""
        results = self.parser.parse(program)
        print(results)
        program = """try: {assert False;} catch KeyError as e: {a="False";}"""
        results = self.parser.parse(program)
        print(results)

        program = r"""
        try: {print c;}
        catch Exception as e: { print "no c yet :)";}"""
        results = self.parser.parse(program)
        print(results)

    def test_if(self):
        program = r"""
                if index <2 : {assert True;}
                if True: {assert True;}
                else: {print True;}
                if True: {assert True;}
                elif True: {print True;}
                else: {print False;}
                """
        results = self.parser.parse(program)
        print(results)

    def test_method_call(self):
        program = "opposite();"
        results = self.parser.parse(program)
        print(results)
        program = "n.x();"
        results = self.parser.parse(program)
        print(results)
        program = "b.a(f[1],v.f[1]);"
        results = self.parser.parse(program)
        print(results)
        program = "b.a(cat=f[1], dog=2);"
        results = self.parser.parse(program)
        print(results)
        program = "b.a(f[1],v.f[1], cat=f[1], dog =2);"
        results = self.parser.parse(program)
        print(results)

    def test_while(self):
        program = r"""
                while cat > dog: {print True;}
                """
        results = self.parser.parse(program)
        print(results)

    def test_foreach(self):
        program = r"""
                        for e in cat: {assert False;}
                        """
        results = self.parser.parse(program)
        print(results)

    def test_with(self):
        # warning note: seems to be a parsing issue. The statement runs fine
        program = "with Rack as 2, Carrier as a: {assert False;}"
        results = self.parser.parse(program)
        print(results)

    def test_in(self):
        program = r"""
                        in dir direction:{ knit f1;}
                        in Current direction:{ knit f1;}
                        in Leftward direction:{
                            tuck b3, bs4, fs16;
                        }
                        in <-- direction:{
                            tuck b3, bs4, fs16;
                        }
                        in reverse direction:{
                            tuck b3, bs4, fs16;
                        }"""
        results = self.parser.parse(program)
        print(results)

    def test_needle_accessor(self):
        program = r"""
            machine.f2;
            s0.b2;
            s1:g2.bs10;
        """
        results = self.parser.parse(program)
        print(results)

    def test_func(self):
        program = r"""
                      def func(a, b=True):{
                        assert True;
                        return True;
                      }
                      value = func(1, b=1);"""
        results = self.parser.parse(program)
        print(results)

    def test_slices(self):
        program = "slice[0];"
        results = self.parser.parse(program)
        print(results)
        # program = "slice[0:];"
        # results = self.parser.parse(program)
        # print(results)
        program = "slice[0:1];"
        results = self.parser.parse(program)
        print(results)
        program = "slice[0:1:-1];"
        results = self.parser.parse(program)
        print(results)
        program = "slice[10::-1];"
        results = self.parser.parse(program)
        print(results)
        program = "slice[:-1];"
        results = self.parser.parse(program)
        print(results)
        program = "slice[:-1:-2];"
        results = self.parser.parse(program)
        print(results)
        program = "slice[::-2];"
        results = self.parser.parse(program)
        print(results)

    def test_needle_list(self):
        program = r"""
            in reverse direction:{
                tuck n[0:w:2];
            }
        """
        results = self.parser.parse(program)
        print(results)

    def test_import(self):
        program = r"""
            import knit_script.knitting_machine.machine_components.needles as needles;
            cat = needles.Needle(True, 1);
        """
        results = self.parser.parse(program)
        print(results)

    def test_accessor(self):
        program = "cat.dog;"
        results = self.parser.parse(program)
        print(results)
        program = "cat.dog.bird;"
        results = self.parser.parse(program)
        print(results)
        program = "cat.dog.bird();"
        results = self.parser.parse(program)
        print(results)
        program = "cat.dog.bird[1];"
        results = self.parser.parse(program)
        print(results)

    def test_sheet_accessor(self):
        program = "s1.f1;"
        results = self.parser.parse(program)
        print(results)
        program = "machine.f0;"
        results = self.parser.parse(program)
        print(results)

    def test_global(self):
        program = "global cat=dog;"
        results = self.parser.parse(program)
        print(results)

    def test_layers(self):
        program = "push f1 to layer 2;"
        results = self.parser.parse(program)
        print(results)
        program = "push f1 to Front;"
        results = self.parser.parse(program)
        print(results)
        program = "push f1 2 backward;"
        results = self.parser.parse(program)
        print(results)
        program = "swap f1 with layer 1;"
        results = self.parser.parse(program)
        print(results)
        program = "swap f1 with sheet 3;"
        results = self.parser.parse(program)
        print(results)

    def test_if_else(self):
        program = """
        if reverse == Leftward:{
            print "leftward pass";
        } else:{
            print "rightward pass";
        }
        """
        results = self.parser.parse(program)
        print(results)


