from unittest import TestCase

from knitout_interpreter.knitout_operations.needle_instructions import Knit_Instruction
from resources.interpret_test_ks import count_lines, interpret_test_ks


class TestNeedle_Set_Expression(TestCase):
    def test_front_needles(self):
        program = r"""assert len(Front_Needles) == 540;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_back_needles(self):
        program = r"""assert len(Back_Needles) == 540;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_all_needles(self):
        program = r"""assert len(Needles) == 540*2;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_front_sliders(self):
        program = r"""assert len(Front_Sliders) == 540;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_back_sliders(self):
        program = r"""assert len(Back_Sliders) == 540;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_all_sliders(self):
        program = r"""assert len(Sliders) == 540*2;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_Front_Loops(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[:4];
        }
        releasehook;
        assert len(Front_Loops) == 4;
        in Rightward direction:{
            knit Front_Loops;
        }
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Knit_Instruction}) == 4

    def test_Back_Slider_Loops(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[:4];
        }
        releasehook;
        assert len(Front_Loops) == 4;
        xfer Front_Loops across sliders;
        print Back_Slider_Loops;
        """
        interpret_test_ks(program, execute_knitout=False)

    def test_Back_Loops(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Back_Needles[:4];
        }
        releasehook;
        assert len(Back_Loops) == 4;
        in Rightward direction:{
            knit Back_Loops;
        }
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Knit_Instruction}) == 4

    def test_Front_Slider_Loops(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Back_Needles[:4];
        }
        releasehook;
        assert len(Back_Loops) == 4;
        xfer Back_Loops across sliders;
        print Front_Slider_Loops;
        """
        interpret_test_ks(program, execute_knitout=False)

    def test_Loops(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Back_Needles[:4];
            tuck Front_Needles[:4];
        }
        releasehook;
        assert len(Loops) == 8;
        in Rightward direction:{
            knit Loops;
        }
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Knit_Instruction}) == 8

    def test_Slider_Loops(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Back_Needles[:4:2];
            tuck Front_Needles[1:4:2];
        }
        releasehook;
        assert len(Loops) == 4;
        xfer Loops across sliders;
        assert len(Slider_Loops) == 4;
        """
        interpret_test_ks(program, execute_knitout=False)

    def test_directed_last_pass(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[:4];
        }
        releasehook;
        assert len(Last_Pass) == 4;
        assert isinstance(Last_Pass, list);
        in Rightward direction:{
            knit Last_Pass;
        }
        """
        klines, _, __ = interpret_test_ks(program)
        assert count_lines(klines, include_types={Knit_Instruction}) == 4

    def test_xfer_last_pass(self):
        program = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[:4];
        }
        releasehook;
        assert len(Last_Pass) == 4;
        assert isinstance(Last_Pass, list);
        xfer Loops across;
        assert len(Last_Pass) == 4;
        assert isinstance(Last_Pass, dict);
        xfer Last_Pass.values() across;
        assert len(Front_Loops) == 4;
        """
        interpret_test_ks(program)
