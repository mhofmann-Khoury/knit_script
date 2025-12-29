from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks

from knit_script.knit_script_exceptions.Knit_Script_Exception import Incompatible_In_Carriage_Pass_Exception


class TestKnit_Script_Exception(TestCase):

    def test_shadow_variable_warning(self):
        try:
            program = r"""
            Carrier = 1;
            in Leftward direction:{
                knit f1;
                miss f2;
            }
            """
            interpret_test_ks(program, print_k_lines=False)
            self.fail("Should have raised an exception")
        except Incompatible_In_Carriage_Pass_Exception as e:
            pass
