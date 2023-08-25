from unittest import TestCase

from knit_script.knitout_compilers.compile_knitout import knitout_to_dat


class Test(TestCase):
    def test_knitout_to_dat(self):
        knitout_to_dat("test.k", "test.dat")
