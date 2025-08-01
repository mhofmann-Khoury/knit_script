from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class Test_Racked_Xfers(TestCase):
    def test_across(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[0:5];
        }
        releasehook;
        xfer Loops across;
        assert len(Back_Loops) == 5;
        xfer Loops across;
        assert len(Front_Loops) == 5;
        """
        interpret_test_ks(program)

    def test_across_to_bed(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[0:5];
        }
        releasehook;
        xfer Loops across to Front bed;
        assert len(Back_Loops) == 0;
        xfer Loops across to Back bed;
        assert len(Back_Loops) == 5;
        xfer Loops across to Back bed;
        assert len(Front_Loops) == 0;
        xfer Loops across to Front bed;
        assert len(Front_Loops) == 5;
        """
        interpret_test_ks(program)

    def test_left_rack(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[1:5];
        }
        releasehook;
        xfer Loops 1 to Left;
        assert len(Back_Loops) == 4;
        assert Back_Loops[0].position == 0;
        """
        interpret_test_ks(program)

    def test_right_rack(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[0:5];
        }
        releasehook;
        xfer Loops 1 to Right;
        assert len(Back_Loops) == 5;
        assert Back_Loops[0].position == 1;
        """
        interpret_test_ks(program)

    def test_mix_bed_and_rack(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[0:5];
        }
        releasehook;
        xfer Loops[0::2] 1 to Right to Back bed;
        assert len(Back_Loops) == 3;
        assert Back_Loops[0].position == 1;
        xfer Back_Loops 1 to Left to Front bed;
        assert len(Front_Loops) == 5;
        """
        interpret_test_ks(program)
