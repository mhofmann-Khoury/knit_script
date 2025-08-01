from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks


class Test_Branch_Statements(TestCase):
    def test_if(self):
        program = r"""
            p = "dog";
            if True:{
                print "In If";
                p = "cat";
            }
            assert p == "cat";
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_elif(self):
        program = r"""
            p = "dog";
            if False:{
                assert False, "Shouldn't reach this statement";
            } elif True:{
                print "In else if";
                p = "cat";
            }
            assert p == "cat";
        """
        interpret_test_ks(program, print_k_lines=False)

    def test_else(self):
        program = r"""
            p = "dog";
            if False:{
                assert False, "Shouldn't reach this statement";
            } elif False:{ assert False, "shouldn't reach this statement";}
            else:{
                print "In else";
                p = "cat";
            }
            assert p == "cat";
        """
        interpret_test_ks(program, print_k_lines=False)
