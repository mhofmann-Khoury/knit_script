from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.Knit_Script_Parser import Knit_Script_Parser
from knit_script.knitout_interpreter.knitout_structures.Knitout_Line import Knitout_Line


def _print_parse(parser, pattern, is_file: bool = False):
    statements = parser.parse(pattern, pattern_is_file=is_file)
    print(statements)


def _print_knitout(knitout: list[Knitout_Line]):
    for l in knitout:
        print(str(l))


class Test_KS_Interpreter(TestCase):
    def test_indexed_value(self):
        parser = Knit_Script_Parser(debug_grammar=False, debug_parser=False)
        interpreter = Knit_Script_Interpreter()
        pattern = r"""
                l = [1, 2, 3, 4];
                print l[0];
                print l[0:2];
                print l[0::2];
                print l[0:-1:2];
                l[0] = "cat";
                print l;
                l[1] = l[0];
                print l;
                d = {"cat": 1, "dog":2};
                print d["cat"];
                d["bird"] = 3;
                print d;
                """
        _print_parse(parser, pattern)
        knitout = interpreter._interpret_knit_script(pattern, pattern_is_file=False)

    def test_not_expression(self):
        parser = Knit_Script_Parser(debug_grammar=False, debug_parser=False)
        interpreter = Knit_Script_Interpreter()
        pattern = r"""
                cat = "cat";
                dog = "dog";
                print cat is dog;
                print cat is not dog;
                print 1 not in [2,3,4];
                """
        _print_parse(parser, pattern)
        knitout = interpreter._interpret_knit_script(pattern, pattern_is_file=False)

    def test_rack_change(self):
        parser = Knit_Script_Parser(debug_grammar=False, debug_parser=False)
        interpreter = Knit_Script_Interpreter()
        pattern = r"""Rack = 2;
                        """
        _print_parse(parser, pattern)
        knitout = interpreter._interpret_knit_script(pattern, pattern_is_file=False)
        _print_knitout(knitout)
