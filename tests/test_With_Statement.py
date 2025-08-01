from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks
from resources.load_test_resources import load_test_resource


class TestWith_Statement(TestCase):
    def test_withs(self):
        program = load_test_resource("with_tests.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False)
