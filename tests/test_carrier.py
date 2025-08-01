from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class TestCarrier_Expression(TestCase):
    def test_print_all_carriers(self):
        pattern = r"""
        for c in machine.carrier_system.carriers:{
            print c;
        }
        """
        interpret_test_ks(pattern)
        for cid in range(1, 10):
            pattern = f"""print c{cid};"""
            interpret_test_ks(pattern)
