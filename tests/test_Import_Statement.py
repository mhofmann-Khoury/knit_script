from unittest import TestCase

from knitout_interpreter.knitout_operations.needle_instructions import Tuck_Instruction
from resources.interpret_test_ks import count_lines, interpret_test_ks, interpret_test_ks_with_return
from resources.load_test_resources import load_test_resource


class Test_Imports(TestCase):
    def test_import_python(self):
        program = r"""
        import random;
        return random.random();
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, float))

    def test_import_ks_in_std_library(self):
        program = r"""
        import cast_ons;
        Carrier = c1;
        cast_ons.alt_tuck_cast_on(5, knit_lines =1, tuck_lines=1);
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Tuck_Instruction}) == 5

    def test_import_python_in_std_library(self):
        program = r"""
        import needles;
        return needles.direction_sorted_needles([f1,f3,f2], direction=Leftward);
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(3, len(return_value))
        self.assertEqual(3, return_value[0].position)
        self.assertEqual(2, return_value[1].position)
        self.assertEqual(1, return_value[2].position)

    def test_import_local_ks_module(self):
        program = load_test_resource("imports_ks.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False)
