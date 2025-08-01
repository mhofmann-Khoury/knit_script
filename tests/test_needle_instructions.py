from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks, count_lines
from knitout_interpreter.knitout_operations.needle_instructions import *


class Test_Needle_Instructions(TestCase):
    def test_tucks(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[0:5];
        }
        releasehook;
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Tuck_Instruction}) == 5

    def test_knit(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            knit Front_Needles[0:5];
        }
        releasehook;
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Knit_Instruction}) == 5

    def test_split(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            split Front_Needles[0:5];
        }
        releasehook;
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Split_Instruction}) == 5

    def test_miss(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            knit Front_Needles[0:5];
        }
        releasehook;
        in reverse direction:{
            miss Front_Needles[5];
        }
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Miss_Instruction}) == 1

    def test_xfer(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            knit Front_Needles[0:5];
        }
        releasehook;
        xfer Loops across to Back bed;
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Xfer_Instruction}) == 5

    def test_drop(self):
        program = r"""
        drop Front_Needles[0:5];
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Drop_Instruction}) == 5
