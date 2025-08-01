from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class Test_Loops(TestCase):
    def test_while(self):
        program = r"""
        i=0;
        while i < 10:{
            assert i < 10;
            i= i+1;
        }
        """
        interpret_test_ks(program, print_k_lines=False)
