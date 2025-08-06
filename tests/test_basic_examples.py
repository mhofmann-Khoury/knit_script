from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks
from resources.load_test_resources import load_test_resource


class Test_Basic_Examples(TestCase):

    def test_stst(self):
        program = load_test_resource("stst.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=True, c=1, pattern_width=4, pattern_height=4)

    def test_all_needles(self):
        program = load_test_resource("all_needle.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=True, c=1, pattern_width=4, pattern_height=4)

    def test_all_needles_racked(self):
        program = load_test_resource("all_needle_racked.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=True, c=1, pattern_width=4, pattern_height=2)
