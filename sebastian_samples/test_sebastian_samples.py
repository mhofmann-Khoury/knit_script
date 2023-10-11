from unittest import TestCase

from knit_script.interpret import knit_script_to_knitout_to_dat


class Test_Sebastian_Samples(TestCase):

    @staticmethod
    def _run_sample(name: str):
        knit_script_to_knitout_to_dat(f"{name}.ks", f"{name}.k", f"{name}.dat", pattern_is_filename=True)

    def test_tube(self):
        self._run_sample("tube")

    def test_rib(self):
        self._run_sample("test_ribbing")

    def test_seed(self):
        self._run_sample("test_seed")

    def test_trinity(self):
        self._run_sample("test_trinity")
        assert False, "May have some duplicate transfers"

    def test_icord(self):
        self._run_sample("icord")

    def test_spiral(self):
        self._run_sample("3D_spiral")
