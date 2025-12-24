from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class TestAssertion(TestCase):
    def test_failed_assertion(self):
        try:
            program = r"""assert 1==2, "failure"; """
            interpret_test_ks(program, print_k_lines=False)
        except AssertionError as e:
            assert hasattr(e, "ks_error_str")
            assert getattr(e, "ks_error_str") == "failure"
        try:
            program = r"""assert 1==2; """
            interpret_test_ks(program, print_k_lines=False)
        except AssertionError as e:
            assert hasattr(e, "ks_error_str")
            assert getattr(e, "ks_error_str") == "<1==2> is False"
