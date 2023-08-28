"""Tests for catching knit script errors"""
from unittest import TestCase

from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.Knit_Errors.parse_errors import Knit_Script_Parse_Error
from knit_script.Knit_Errors import Duplicate_Carrier_Error, Non_Existent_Carrier_Error


class Test_Errors(TestCase):
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

    def test_dup_carrier(self):
        program = r"""
            with Carrier as [c1, c2, c1]:{
                in reverse direction:{
                    knit Loops;
                }
            }
        """
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
            assert False, "Should show duplicate error"
        except Duplicate_Carrier_Error as e:
            print(e)
        program = r"""
                    with Carrier as [c1, 1]:{
                        in reverse direction:{
                            knit Loops;
                        }
                    }
                """
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
            assert False, "Should show duplicate error"
        except Duplicate_Carrier_Error as e:
            print(e)

    def test_bad_carrier(self):
        program = r"""
                    with Carrier as c0:{
                        in reverse direction:{
                            knit Loops;
                        }
                    }
                """
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
            assert False, "Should show duplicate error"
        except Non_Existent_Carrier_Error as e:
            print(e)
        program = r"""
                            with Carrier as c12:{
                                in reverse direction:{
                                    knit Loops;
                                }
                            }
                        """
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
            assert False, "Should show duplicate error"
        except Non_Existent_Carrier_Error as e:
            print(e)
        program = r"""
                            with Carrier as -1:{
                                in reverse direction:{
                                    knit Loops;
                                }
                            }
                        """
        try:
            self.parser.write_knitout(program, f"error_test.k", pattern_is_file=False)
            assert False, "Should show duplicate error"
        except Non_Existent_Carrier_Error as e:
            print(e)
