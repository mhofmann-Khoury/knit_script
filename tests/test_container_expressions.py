from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class Test_Containers(TestCase):
    def test_needle_list(self):
        program = r"""print [f1,f2,f3];"""
        interpret_test_ks(program)

    def test_mixed_list(self):
        program = r"""print [f1,"f2",3, c1];"""
        interpret_test_ks(program)

    def test_simple_list_comp(self):
        program = r"""
        l = [i for i in range(10)];
        print l;
        assert len(l) == 10;
        """
        interpret_test_ks(program)

    def test_conditioned_list_comp(self):
        program = r"""
        l =[i for i in range(10) if i%2==0];
        print l;
        assert len(l) == 5;
        """
        interpret_test_ks(program)

    def test_multiple_vars_comp(self):
        program = r"""

        l =[[i,j] for i,j in zip(range(10), range(1,11)) if i%2==0];
        print l;
        assert len(l) == 5;
        """
        interpret_test_ks(program)

    def test_needle_dict(self):
        program = r"""print {f1:1,f2:2,f3:3};"""
        interpret_test_ks(program)

    def test_mixed_dict(self):
        program = r"""print {"f1":1,"cat":2,f3:c3};"""
        interpret_test_ks(program)

    def test_simple_dict_comp(self):
        program = r"""
        l = {i:True for i in range(10)};
        print l;
        assert len(l) == 10;
        """
        interpret_test_ks(program)

    def test_conditioned_dict_comp(self):
        program = r"""
        l ={i: i%2==1 for i in range(10) if i%2==0};
        print l;
        assert len(l) == 5;
        for k, v in l.items():{
            assert not v;
        }
        """
        interpret_test_ks(program)

    def test_multiple_vars_dict_comp(self):
        program = r"""
        l ={i:j for i,j in zip(range(10), range(1,11)) if i%2==0};
        print l;
        assert len(l) == 5;
        """
        interpret_test_ks(program)
