import random
from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks, interpret_test_ks_with_return


class Test_Slicing_and_Indexing(TestCase):
    def test_index(self):
        for _ in range(10):
            pos = random.randint(0, 400)
            program = f"assert Front_Needles[{pos}].position == {pos};"
            interpret_test_ks(program, print_k_lines=False)

    def test_full_def_slice(self):
        program = r"""
        needles = Front_Needles[1:6:2];
        assert len(needles) == 3;
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 3)
        self.assertEqual(1, return_value[0].position)
        self.assertEqual(3, return_value[1].position)
        self.assertEqual(5, return_value[2].position)

    def test_no_spacing(self):
        program = r"""
        needles = Front_Needles[1:6];
        assert len(needles) == 5;
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 5)
        for i, needle in enumerate(return_value):
            self.assertEqual(i + 1, needle.position)

    def test_no_start_no_space(self):
        program = r"""
        needles = Front_Needles[:6];
        assert len(needles) == 6;
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 6)
        for i, needle in enumerate(return_value):
            self.assertEqual(i, needle.position)

    def test_no_end_no_space(self):
        program = r"""
        needles = Front_Needles[0:6];
        needles = needles[1:];
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 5)
        for i, needle in enumerate(return_value):
            self.assertEqual(i + 1, needle.position)

    def test_no_start_spacer(self):
        program = r"""
        needles = Front_Needles[:6:2];
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 3)
        self.assertEqual(0, return_value[0].position)
        self.assertEqual(2, return_value[1].position)
        self.assertEqual(4, return_value[2].position)

    def test_no_end_spacer(self):
        program = r"""
        needles = Front_Needles[0:6];
        needles = needles[1::2];
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 3)
        self.assertEqual(1, return_value[0].position)
        self.assertEqual(3, return_value[1].position)
        self.assertEqual(5, return_value[2].position)

    def test_negative_start(self):
        program = r"""
        needles = Front_Needles[0:6];
        needles = needles[-2:];
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 2)
        self.assertEqual(4, return_value[0].position)
        self.assertEqual(5, return_value[1].position)

    def test_negative_end(self):
        program = r"""
        needles = Front_Needles[0:6];
        needles = needles[:-2];
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 4)
        for i, needle in enumerate(return_value):
            self.assertEqual(i, needle.position)

    def test_negative_space(self):
        program = r"""
        needles = Front_Needles[6:0:-1];
        return needles;
        """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_value, list))
        self.assertEqual(len(return_value), 6)
        for i, needle in enumerate(return_value):
            self.assertEqual(6 - i, needle.position)
