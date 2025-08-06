from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class Test_KnitScript_Parser(TestCase):
    def test_before_space_after_no_space(self):
        program = r""" print f"before string {2+2} after string {2+3}."; """
        interpret_test_ks(program, print_k_lines=False)

    def test_before_no_space_after_space(self):
        program = r""" print f" before string:{2+2} after string {2+3} ."; """
        interpret_test_ks(program, print_k_lines=False)

    def test_mult_space_after(self):
        program = r""" print f" before string {2+2}     after string {2+3}  ."; """
        interpret_test_ks(program, print_k_lines=False)

    def test_tabs(self):
        program = r""" print f" before string:\t{2+2}\t after string\t{2+3}\t."; """
        interpret_test_ks(program, print_k_lines=False)

    def test_carriage_returns(self):
        program = r""" print f" before string:\n{2+2}\n after string\n{2+3}\n."; """
        interpret_test_ks(program, print_k_lines=False)
