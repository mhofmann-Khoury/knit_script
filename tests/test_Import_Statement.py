from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks, count_lines
from knitout_interpreter.knitout_operations.needle_instructions import Tuck_Instruction

from resources.load_test_resources import load_test_resource


class Test_Imports(TestCase):
    def test_import_python(self):
        program = r"""
        import random;
        print random.random();
        """
        interpret_test_ks(program, print_k_lines=False)

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
        print needles.direction_sorted_needles([f1,f3,f2], direction=Leftward);
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_import_local_ks_module(self):
        program = load_test_resource("imports_ks.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False)
