from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.Knit_Script_Parser import Knit_Script_Parser


def _print_parse(parser, pattern, is_file: bool = False):
    x, y = parser.parse(pattern, pattern_is_file=is_file)
    print(x)
    print(y)


class Test_Actions(TestCase):
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
        interpreter._interpret_knit_script(pattern, pattern_is_file=False)

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
        interpreter._interpret_knit_script(pattern, pattern_is_file=False)

