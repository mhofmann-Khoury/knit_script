import warnings
from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks

from knit_script.knit_script_warnings.Knit_Script_Warning import Shadow_Variable_Warning


class TestKnit_Script_Warning(TestCase):

    def test_shadow_variable_warning(self):
        with warnings.catch_warnings(record=True) as caught:
            program = r""" x = 1;
            y = 2;
            def func(x, y="cat"):{
            return x;
            }
            func(2);"""
            interpret_test_ks(program, print_k_lines=False)
            self.assertEqual(len(caught), 2)
            self.assertIs(caught[0].category, Shadow_Variable_Warning)
            self.assertIs(caught[1].category, Shadow_Variable_Warning)
