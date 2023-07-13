from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter


class Test(TestCase):
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_rack_statement(self):
        program = r"""racking f1 to b3;"""
        knitout, knit_graph = self.parser.write_knitout(program, f"rack_test.k", pattern_is_file=False)

    def test_as_rack(self):
        program = r"""
            with Carrier as 1, Rack as 2:{
                Rack = 1;
                in reverse direction: {
                    knit f1;
                }
            }
        """
        knitout, knit_graph = self.parser.write_knitout(program, f"rack_test.k", pattern_is_file=False)