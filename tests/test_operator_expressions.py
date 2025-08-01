from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class TestOperator_Expression(TestCase):
    def test_negation(self):
        program = r"""assert not False;"""
        interpret_test_ks(program, print_k_lines=False)
        program = r"""assert not True == False;"""
        interpret_test_ks(program, print_k_lines=False)
        program = "assert not (2==1);"
        interpret_test_ks(program, print_k_lines=False)

    def test_add(self):
        program = r"""assert 2+1==3;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_subtrack(self):
        program = r"""assert 2-1==1;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_divide(self):
        program = r"""assert 4/2==2;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_mod(self):
        program = r"""assert 4%2==0;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_mul(self):
        program = r"""assert 2*3==6;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_exp(self):
        program = r"""assert 2^3==8;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_less_than(self):
        program = r"""assert 4<5;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_greater_than(self):
        program = r"""assert 6>2;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_less_than_equal(self):
        program = r"""assert 4<=4;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_greater_than_equal(self):
        program = r"""assert 4>=4;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_equal(self):
        program = r"""assert "cat" == "cat";"""
        interpret_test_ks(program, print_k_lines=False)

    def test_not_equal(self):
        program = r"""assert "dog" != "cat";"""
        interpret_test_ks(program, print_k_lines=False)

    def test_is(self):
        program = r"""assert 1 is 1;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_is_not(self):
        program = r"""assert 6 is not 2;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_in(self):
        program = r"""assert 1 in [0, 1, 2];"""
        interpret_test_ks(program, print_k_lines=False)

    def test_not_in(self):
        program = r"""assert 6 not in [0, 1, 2];"""
        interpret_test_ks(program, print_k_lines=False)

    def test_or(self):
        program = r"""assert False or True;"""
        interpret_test_ks(program, print_k_lines=False)

    def test_and(self):
        program = r"""assert 1==1 and True;"""
        interpret_test_ks(program, print_k_lines=False)
