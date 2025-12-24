from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class TestCarrier_Expression(TestCase):
    def test_get_all_carrier_ids(self):
        for cid in range(1, 10):
            pattern = f"""assert c{cid}.carrier_id == {cid};"""
            interpret_test_ks(pattern, print_k_lines=False)

    def test_carrier_position(self):
        pattern = r"""
            Carrier = c1;
            in Leftward direction:{
                tuck Front_Needles[10: 20];
            }
            releasehook;
            assert machine.carrier_system[Carrier].position == 10;
            """
        interpret_test_ks(pattern, print_k_lines=False)

    def test_assign_carrier_by_number(self):
        pattern = r"""
                Carrier = 1;
                in Leftward direction:{
                    tuck Front_Needles[10: 20];
                }
                releasehook;
                assert Carrier[0] == 1;
                """
        interpret_test_ks(pattern, print_k_lines=False)
