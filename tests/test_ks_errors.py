"""Tests for catching knit script errors"""

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.knit_script_errors.parse_errors import Knit_Script_Parse_Error


class Test_Errors:
    parser = Knit_Script_Interpreter(debug_grammar=False, debug_parser=False, debug_parser_layout=False)

    def test_eol_errors(self):
        program = r"""
                    cat=dog
                """
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
        except Knit_Script_Parse_Error as e:
            print(e)

    def test_colon_errors(self):
        program = """if True {block;}"""
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
        except Knit_Script_Parse_Error as e:
            print(e)
        program = """try: {block;}
                        catch E as e {block;}"""
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
        except Knit_Script_Parse_Error as e:
            print(e)

    def test_missing_paren(self):
        program = """range(0,2;"""
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
        except Knit_Script_Parse_Error as e:
            print(e)
        program = """range 0,2);"""
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
        except Knit_Script_Parse_Error as e:
            print(e)