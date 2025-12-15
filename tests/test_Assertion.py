from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks

from knit_script.knit_script_exceptions.ks_exceptions import Knit_Script_Assertion_Exception


class TestAssertion(TestCase):
    def test_failed_assertion(self):
        try:
            program = r"""assert 1==2, "failure"; """
            interpret_test_ks(program, print_k_lines=False)
        except Knit_Script_Assertion_Exception as e:
            print(str(e))
            pass
