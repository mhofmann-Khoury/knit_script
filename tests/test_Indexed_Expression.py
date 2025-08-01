import random
from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class Test_Slicing_and_Indexing(TestCase):
    def test_index(self):
        for _ in range(10):
            pos = random.randint(0, 400)
            program = f"assert Front_Needles[{pos}].position == {pos};"
            interpret_test_ks(program)

    def test_full_def_slice(self):
        program = r"""
        needles = Front_Needles[1:6:2];
        print needles;
        assert len(needles) == 3;
        """
        interpret_test_ks(program)

    def test_no_spacing(self):
        program = r"""
        needles = Front_Needles[1:6];
        print needles;
        assert len(needles) == 5;
        """
        interpret_test_ks(program)

    def test_no_start_no_space(self):
        program = r"""
        needles = Front_Needles[:6];
        print needles;
        assert len(needles) == 6;
        """
        interpret_test_ks(program)

    def test_no_end_no_space(self):
        program = r"""
        needles = Front_Needles[0:6];
        needles = needles[1:];
        print needles;
        assert len(needles) == 5;
        """
        interpret_test_ks(program)

    def test_no_start_spacer(self):
        program = r"""
        needles = Front_Needles[:6:2];
        print needles;
        assert len(needles) == 3;
        """
        interpret_test_ks(program)

    def test_no_end_spacer(self):
        program = r"""
        needles = Front_Needles[0:6];
        needles = needles[1::2];
        print needles;
        assert len(needles) == 3;
        """
        interpret_test_ks(program)

    def test_negative_start(self):
        program = r"""
        needles = Front_Needles[0:6];
        needles = needles[-2:];
        print needles;
        assert len(needles) == 2;
        """
        interpret_test_ks(program)

    def test_negative_end(self):
        program = r"""
        needles = Front_Needles[0:6];
        needles = needles[:-2];
        print needles;
        assert len(needles) == 4;
        """
        interpret_test_ks(program)

    def test_negative_space(self):
        program = r"""
        needles = Front_Needles[6:0:-1];
        print needles;
        assert len(needles) == 6;
        """
        interpret_test_ks(program)
