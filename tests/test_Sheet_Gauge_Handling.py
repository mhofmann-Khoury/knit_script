from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class Test_Sheet_Gauge_Handling(TestCase):
    def test_knit_sheets_at_half_gauge(self):
        program = r"""
        Carrier = c1;
        Gauge = 2;
        Sheet = s0;
        in Leftward direction:{
            tuck Front_Needles[0:5];
        }
        releasehook;
        assert len([n for n in Last_Pass if n.position%2==0]) == len(Last_Pass);
        assert len(Front_Loops) == len(Last_Pass);
        Sheet = s1;
        assert len(Front_Loops) == 0;
        in Rightward direction:{
            knit Back_Needles[0:5];
        }
        assert len([n for n in Last_Pass if n.position%2==1]) == len(Last_Pass);
        assert len(Back_Loops) == len(Last_Pass);
        Sheet = s0;
        assert len(Back_Loops) == 0;
        Gauge = 1;
        assert len(Front_Loops) == len(Back_Loops) and len(Front_Loops) == 5;
        print Loops;
        """
        interpret_test_ks(program)

    def test_push_layers(self):
        program = r"""
        Carrier = c1;
        Gauge = 2;
        Sheet = s0;
        in Leftward direction:{
            tuck Back_Needles[0:10];
        }
        releasehook;
        Sheet = s1;
        in Rightward direction:{
            tuck Front_Needles[0:10];
        }
        Sheet = s0;
        push Loops[0:5] to Back;
        in Leftward direction:{
            knit Loops;
        }
        """
        interpret_test_ks(program)

    def test_swap_layers(self):
        program = r"""
        Carrier = c1;
        Gauge = 2;
        Sheet = s0;
        in Leftward direction:{
            tuck Back_Needles[0:10];
        }
        releasehook;
        Sheet = s1;
        in Rightward direction:{
            tuck Front_Needles[0:10];
        }
        Sheet = s0;
        swap Loops[0:5] with sheet s1;
        in Leftward direction:{
            knit Loops;
        }
        """
        interpret_test_ks(program)
