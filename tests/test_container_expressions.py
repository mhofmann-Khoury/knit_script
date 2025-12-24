from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks, interpret_test_ks_with_return
from virtual_knitting_machine.machine_components.needles.Needle import Needle
from virtual_knitting_machine.machine_components.yarn_management.Yarn_Carrier import Yarn_Carrier


class Test_Containers(TestCase):
    def test_needle_list(self):
        program = r"""return [f1,f2,f3];"""
        _ko, _machine, _graph, return_val = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_val, list))
        for i, n in enumerate(return_val):
            self.assertTrue(isinstance(n, Needle))
            self.assertEqual(n.position, i + 1)
            self.assertTrue(n.is_front)

    def test_mixed_list(self):
        program = r"""return [f1,"f2",3, c1];"""
        _ko, _machine, _graph, return_val = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_val, list))
        self.assertTrue(isinstance(return_val[0], Needle))
        self.assertTrue(isinstance(return_val[1], str))
        self.assertTrue(isinstance(return_val[2], int))
        self.assertTrue(isinstance(return_val[3], Yarn_Carrier))

    def test_simple_list_comp(self):
        program = r"""
        l = [i for i in range(10)];
        assert len(l) == 10;
        return l;
        """
        _ko, _machine, _graph, return_val = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_val, list))
        for i, i_l in enumerate(return_val):
            self.assertEqual(i, i_l)

    def test_conditioned_list_comp(self):
        program = r"""
        l =[i for i in range(10) if i%2==0];
        assert len(l) == 5;
        return l;
        """
        _ko, _machine, _graph, return_val = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_val, list))
        for i, i_l in zip(return_val, [i_p for i_p in range(5) if i_p % 2 == 0]):
            self.assertEqual(i, i_l)

    def test_multiple_vars_comp(self):
        program = r"""

        l =[[i,j] for i,j in zip(range(10), range(1,11)) if i%2==0];
        assert len(l) == 5;
        return l;
        """
        _ko, _machine, _graph, return_val = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_val, list))
        py_l = [[i, j] for i, j in zip(range(10), range(1, 11)) if i % 2 == 0]
        for i, i_l in zip(return_val, py_l):
            self.assertEqual(i, i_l)

    def test_needle_dict(self):
        program = r"""return {f1:1,f2:2,f3:3};"""
        _ko, _machine, _graph, return_val = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_val, dict))
        for k, v in return_val.items():
            self.assertTrue(isinstance(k, Needle))
            self.assertEqual(k.position, v)

    def test_mixed_dict(self):
        program = r"""return {"f1":1,"cat":2,f3:c3};"""
        _ko, _machine, _graph, return_val = interpret_test_ks_with_return(program, print_k_lines=False)
        self.assertTrue(isinstance(return_val, dict))
        self.assertEqual(return_val["f1"], 1)
        self.assertTrue(return_val["cat"], 2)
        self.assertIn(Needle(True, 3), return_val)

    def test_conditioned_dict_comp(self):
        program = r"""
        l ={i: i%2==1 for i in range(10) if i%2==0};
        assert len(l) == 5;
        for k, v in l.items():{
            assert not v;
        }
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_multiple_vars_dict_comp(self):
        program = r"""
        l ={i:j for i,j in zip(range(10), range(1,11)) if i%2==0};
        assert len(l) == 5;
        """
        interpret_test_ks(program, print_k_lines=False)
