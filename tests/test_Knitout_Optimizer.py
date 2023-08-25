from unittest import TestCase

from knit_script.interpret import knit_script_to_knitout
from knit_script.knitout_interpreter.Knitout_Interpreter import Knitout_Interpreter
from knit_script.knitout_interpreter.Knitout_Optimizer import Knitout_Optimizer


class TestKnitout_Optimizer(TestCase):
    def test_visualize_needle(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                        ;!knitout-2
                        inhook 1
                        releasehook 1
                        tuck - f2 1
                        tuck - f1 1
                        knit + f1 1
                        knit + f2 1
                        knit - f2 1
                        knit - f1 1
                        outhook 1
                        """
        knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        topo_graph = Knitout_Optimizer(context, 1)
        topo_graph.visualize()

    def test_optimize(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                    ;!knitout-2
                    inhook 1
                    releasehook 1
                    tuck - f2 1
                    tuck - f1 1
                    knit + f1 1
                    knit + f2 1
                    knit - f2 1
                    knit - f1 1
                    outhook 1
                    """
        knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        topo_graph = Knitout_Optimizer(context, 1)
        optimized_knitout = topo_graph.optimize()
        print(optimized_knitout)

    def test_optimize_rib(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                    ;!knitout-2
                    inhook 1
                    releasehook 1
                    tuck - f4 1
                    tuck - f3 1
                    tuck - f2 1
                    tuck - f1 1
                    knit + f1 1
                    knit + f2 1
                    knit + f3 1
                    knit + f4 1
                    xfer f3 b3
                    xfer f1 b1
                    knit - f4 1
                    knit - b3 1
                    knit - f2 1
                    knit - b1 1
                    outhook 1
                    """
        knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        optimizer = Knitout_Optimizer(context, 3)
        optimizer.visualize()
        optimized_knitout = optimizer.optimize()
        print(optimized_knitout)

    def test_rib_from_ks(self):
        knit_script_to_knitout('rib.ks', 'rib.k')
