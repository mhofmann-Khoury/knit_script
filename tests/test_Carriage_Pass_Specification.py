from unittest import TestCase


class TestCarriage_Pass_Specification(TestCase):
    def test_multi_miss_carriage_pass(self):
        pass
        # Todo add this test in next time knitout-interpreter is updated to ^0.0.19
        # program = r"""
        # Carrier = c1;
        # in Leftward direction:{
        #     tuck Front_Needles[0:4];
        # }
        # releasehook;
        # in Rightward direction:{
        #     miss Front_Loops;
        # }"""
        # interpret_test_ks(program, print_k_lines=False)
