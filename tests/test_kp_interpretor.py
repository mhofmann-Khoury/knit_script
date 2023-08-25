"""Tests associated with the parsing of the language. Does not interpret the code"""
from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.expressions.needle_set_expression import Needle_Sets
from knit_script.knitting_machine.machine_specification.Machine_Type import Machine_Type
from knit_script.knitting_machine.machine_specification.Header_ID import Header_ID
from knit_script.knit_script_interpreter.statements.Statement import Expression_Statement
from knit_script.knitting_machine.machine_components.machine_position import Machine_Bed_Position, Machine_Position


class TestKnit_Pass_Interpreter(TestCase):
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

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
        header, statements = self.parser.parse(program)
        print(statements)

    def test_values(self):
        program = "1.2;"
        header, statements = self.parser.parse(program)
        print(statements)
        program = "12;"
        header, statements = self.parser.parse(program)
        print(statements)
        program = "-45;"
        header, statements = self.parser.parse(program)
        print(statements)
        program = "-9.87;"
        header, statements = self.parser.parse(program)
        print(statements)
        program = "True;"
        header, statements = self.parser.parse(program)
        print(statements)
        program = "False;"
        header, statements = self.parser.parse(program)
        print(statements)
        program = "None;"
        header, statements = self.parser.parse(program)
        print(statements)
        program = """ "string test with some 1.034908 _ -- ; '' " ; """
        header, statements = self.parser.parse(program)
        print(statements)
        program = """ len("len(str) == 14") ; """
        header, statements = self.parser.parse(program)
        print(statements)
        program = """[True, "string", 1.0];"""
        header, statements = self.parser.parse(program)
        print(statements)
        program = f"{Machine_Bed_Position.Back.name};"
        header, statements = self.parser.parse(program)
        print(statements)
        program = f"{Machine_Position.Center.name};"
        header, statements = self.parser.parse(program)
        print(statements)
        program = f"{Machine_Position.Left.name};"
        header, statements = self.parser.parse(program)
        print(statements)
        program = f"{Machine_Type.SWG091N2.name};"
        header, statements = self.parser.parse(program)
        print(statements)
        program = f"{Header_ID.Width.name};"
        header, statements = self.parser.parse(program)
        print(statements)
        program = f"{Needle_Sets.Loops.name};"
        header, statements = self.parser.parse(program)
        print(statements)

    def test_carrier(self):
        program = r'''Carrier = 1;'''
        header, statements = self.parser.parse(program)
        print(statements)
        program = r'''Carrier = c1;'''
        header, statements = self.parser.parse(program)
        print(statements)
        program = r'''Carrier = [1, 2];'''
        header, statements = self.parser.parse(program)
        print(statements)
        program = r'''Carrier = [c2, c1];'''
        header, statements = self.parser.parse(program)
        print(statements)

    def test_order_of_operations(self):
        program = f" (p - p)^e * m / d + a - s;"
        header, statements = self.parser.parse(program)
        print(statements)
        program = f" (2 - 1)^0 * 1 / 1 + 1 - 1;"
        header, statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert 1 == self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 < 0;"
        header, statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 <= 0;"
        header, statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 > 0;"
        header, statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 >= 0;"
        header, statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 == 0;"
        header, statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert not self.parser.knit_script_evaluate_expression(statement.expression)
        program = "2 != 0;"
        header, statements = self.parser.parse(program)
        print(statements)
        statement = statements[0]
        assert isinstance(statement, Expression_Statement)
        assert self.parser.knit_script_evaluate_expression(statement.expression)
        program = "not 2 < 0;"
        header, statements = self.parser.parse(program)
        print(statements)

    def test_xfer(self):
        # program = "xfer n across to Front bed sliders;"
        # header, statements = self.parser.parse(program)
        # print(statements)
        # program = "xfer n, n2 2 to Left to Back bed;"
        # header, statements = self.parser.parse(program)
        # print(statements)
        # program = "xfer [f1, f2, b3] 4 to Right;"
        # header, statements = self.parser.parse(program)
        # print(statements)
        # program = "xfer [f1, f2, b3] 4 to Rightward;"
        # header, statements = self.parser.parse(program)
        # print(statements)

        program = "xfer Back_Loops[1::2]  1 to left to front bed;"
        header, statements = self.parser.parse(program)
        print(statements)

    def test_iter(self):
        program = "[n for every other n,q in Front_Needles if n==f2];"
        header, statements = self.parser.parse(program)
        print(statements)

        program = "{k:v for every 10 n,v in Front_Needles if n==f2};"
        header, statements = self.parser.parse(program)
        print(statements)

        program = "vals = [n.opposite() for n in other_vals];"
        header, statements = self.parser.parse(program)
        print(statements)

    def test_assert(self):
        program = """assert True, "test true";"""
        header, statements = self.parser.parse(program)
        print(statements)
        program = """assert True;"""
        header, statements = self.parser.parse(program)
        print(statements)
        program = """assert False, "test false";"""
        header, statements = self.parser.parse(program)
        print(statements)
        program = """assert False;"""
        header, statements = self.parser.parse(program)
        print(statements)
        program = """assert a==False;"""
        header, statements = self.parser.parse(program)
        print(statements)

    def test_print(self):
        program = r"""
        print "test";
        print 1.0;
        print a;
                """
        _, results = self.parser.parse(program)
        print(results)

    def test_try(self):
        program = """try: {assert True;} catch: {a="False";}"""
        _, results = self.parser.parse(program)
        print(results)
        program = """try: {assert False;} catch: {a="False";}"""
        _, results = self.parser.parse(program)
        print(results)
        program = """try: {assert False;} catch KeyError as e: {a="False";}"""
        _, results = self.parser.parse(program)
        print(results)

        program = r"""
        try: {print c;}
        catch Exception as e: { print "no c yet :)";}"""
        _, results = self.parser.parse(program)
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
        _, results = self.parser.parse(program)
        print(results)

    def test_method_call(self):
        program = "opposite();"
        _, results = self.parser.parse(program)
        print(results)
        program = "n.x();"
        _, results = self.parser.parse(program)
        print(results)
        program = "b.a(f[1],v.f[1]);"
        _, results = self.parser.parse(program)
        print(results)
        program = "b.a(cat=f[1], dog=2);"
        _, results = self.parser.parse(program)
        print(results)
        program = "b.a(f[1],v.f[1], cat=f[1], dog =2);"
        _, results = self.parser.parse(program)
        print(results)

    def test_while(self):
        program = r"""
                while cat > dog: {print True;}
                """
        _, results = self.parser.parse(program)
        print(results)

    def test_foreach(self):
        program = r"""
                        for e in cat: {assert False;}
                        """
        _, results = self.parser.parse(program)
        print(results)

    def test_with(self):
        # warning note: seems to be a parsing issue. The statement runs fine
        program = "with Racking as 2, Carrier as a: {assert False;}"
        _, results = self.parser.parse(program)
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
        _, results = self.parser.parse(program)
        print(results)

    def test_needle_accessor(self):
        program = r"""
            machine.f2;
            s0.b2;
            s1:g2.bs10;
        """
        _, results = self.parser.parse(program)
        print(results)

    def test_func(self):
        program = r"""
                      def func(a, b=True):{
                        assert True;
                        return True;
                      }
                      value = func(1, b=1);"""
        _, results = self.parser.parse(program)
        print(results)

    def test_slices(self):
        program = "slice[0];"
        _, results = self.parser.parse(program)
        print(results)
        program = "slice[0:];"
        _, results = self.parser.parse(program)
        print(results)
        program = "slice[0:1];"
        _, results = self.parser.parse(program)
        print(results)
        program = "slice[0:1:-1];"
        _, results = self.parser.parse(program)
        print(results)
        program = "slice[10::-1];"
        _, results = self.parser.parse(program)
        print(results)
        program = "slice[:-1];"
        _, results = self.parser.parse(program)
        print(results)
        program = "slice[:-1:-2];"
        _, results = self.parser.parse(program)
        print(results)
        program = "slice[::-2];"
        _, results = self.parser.parse(program)
        print(results)

    def test_needle_list(self):
        program = r"""
            in reverse direction:{
                tuck n[0:w:2];
            }
        """
        _, results = self.parser.parse(program)
        print(results)

    def test_import(self):
        program = r"""
            import knit_script.knitting_machine.machine_components.needles as needles;
            cat = needles.Needle(True, 1);
        """
        _, results = self.parser.parse(program)
        print(results)

    def test_accessor(self):
        program = "cat.dog;"
        _, results = self.parser.parse(program)
        print(results)
        program = "cat.dog.bird;"
        _, results = self.parser.parse(program)
        print(results)
        program = "cat.dog.bird();"
        _, results = self.parser.parse(program)
        print(results)
        program = "cat.dog.bird[1];"
        _, results = self.parser.parse(program)
        print(results)

    def test_sheet_accessor(self):
        program = "s1.f1;"
        _, results = self.parser.parse(program)
        print(results)
        program = "machine.f0;"
        _, results = self.parser.parse(program)
        print(results)

    def test_global(self):
        program = "global cat=dog;"
        _, results = self.parser.parse(program)
        print(results)

    def test_layers(self):
        program = "push f1 to layer 2;"
        _, results = self.parser.parse(program)
        print(results)
        program = "push f1 to Front;"
        _, results = self.parser.parse(program)
        print(results)
        program = "push f1 2 backward;"
        _, results = self.parser.parse(program)
        print(results)
        program = "swap f1 with layer 1;"
        _, results = self.parser.parse(program)
        print(results)
        program = "swap f1 with sheet 3;"
        _, results = self.parser.parse(program)
        print(results)

    def test_if_else(self):
        program = """
        if reverse == Leftward:{
            print "leftward pass";
        } else:{
            print "rightward pass";
        }
        """
        _, results = self.parser.parse(program)
        print(results)
