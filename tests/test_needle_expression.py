from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class TestNeedle_Expression(TestCase):
    def test_fronts(self):
        for i in range(10):
            program = f"assert f{i}.position == {i} and f{i}.is_front and not f{i}.is_slider;"
            interpret_test_ks(program, print_k_lines=False)

    def test_backs(self):
        for i in range(10):
            program = f"assert b{i}.position == {i} and not b{i}.is_front and not b{i}.is_slider;"
            interpret_test_ks(program, print_k_lines=False)

    def test_fronts_sliders(self):
        for i in range(10):
            program = f"assert fs{i}.position == {i} and fs{i}.is_front and fs{i}.is_slider;"
            interpret_test_ks(program, print_k_lines=False)

    def test_backs_sliders(self):
        for i in range(10):
            program = f"assert bs{i}.position == {i} and not bs{i}.is_front and bs{i}.is_slider;"
            interpret_test_ks(program, print_k_lines=False)
