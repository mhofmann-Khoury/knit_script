from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks, count_lines
from resources.load_test_resources import load_test_resource


class Test_Basic_Examples(TestCase):

    def test_stst(self):
        program = load_test_resource("stst.ks")
        klines, _, __ = interpret_test_ks(program, pattern_is_filename=True, print_k_lines=True,
                                          c=1, pattern_width=10, pattern_height=10)
