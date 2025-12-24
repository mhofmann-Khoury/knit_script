from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks_with_return


class Test_KnitScript_Parser(TestCase):
    def test_before_space_after_no_space(self):
        program = r""" return f"before string {2+2} after string {2+3}."; """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertEqual(return_value, f"before string {2+2} after string {2+3}.")

    def test_before_no_space_after_space(self):
        program = r""" return f" before string:{2+2} after string {2+3} ."; """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertEqual(return_value, f" before string:{2+2} after string {2+3} .")

    def test_mult_space_after(self):
        program = r""" return f" before string {2+2}     after string {2+3}  ."; """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertEqual(return_value, f" before string {2+2}     after string {2+3}  .")

    def test_tabs(self):
        program = r""" return f" before string:\t{2+2}\t after string\t{2+3}\t."; """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertEqual(return_value, f" before string:\t{2+2}\t after string\t{2+3}\t.")

    def test_carriage_returns(self):
        program = r""" return f" before string:\n{2+2}\n after string\n{2+3}\n."; """
        _, __, ___, return_value = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertEqual(return_value, f" before string:\n{2+2}\n after string\n{2+3}\n.")
