from unittest import TestCase

from knit_script.knitting_machine.machine_components.yarn_management.Carrier_Set import Carrier_Set


class TestCarrier_Set(TestCase):
    def test_carrier_dat_id(self):
        cs = Carrier_Set([1, 2, 3])
        dat_id = cs.carrier_DAT_ID()
        assert dat_id == 123, f"Expected 123 but got {dat_id}"
        cs = Carrier_Set([1, 3, 2])
        dat_id = cs.carrier_DAT_ID()
        assert dat_id == 132, f"Expected 132 but got {dat_id}"
