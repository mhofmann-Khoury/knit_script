from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class TestAttribute_Accessor_Expression(TestCase):
    def test_access_needle_property(self):
        interpret_test_ks("assert Front_Needles[0].position == 0;", print_k_lines=False)

    def test_machine_access(self):
        pattern = r"""
        Carrier = c1;
        in Leftward direction:{
            tuck Front_Needles[0:10];
        }
        releasehook;
        print machine.carrier_system.active_carriers;
        """
        interpret_test_ks(pattern, print_k_lines=False)
