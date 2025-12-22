from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class TestCarriage_Pass_Specification(TestCase):
    def test_multi_miss_carriage_pass(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[0:4];
        }
        releasehook;
        in Rightward direction:{
            miss Front_Loops;
        }"""
        interpret_test_ks(program, print_k_lines=False)
