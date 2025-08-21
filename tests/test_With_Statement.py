from unittest import TestCase

from knitout_interpreter.knitout_operations.Rack_Instruction import Rack_Instruction
from resources.interpret_test_ks import count_lines, interpret_test_ks
from resources.load_test_resources import load_test_resource


class TestWith_Statement(TestCase):
    def test_withs(self):
        program = load_test_resource("with_tests.ks")
        klines, _, __ = interpret_test_ks(program, pattern_is_filename=True, print_k_lines=True)
        rack_count = count_lines(klines, include_types={Rack_Instruction})
        assert rack_count == 2, f"Expected 3 racks but got {rack_count}"
