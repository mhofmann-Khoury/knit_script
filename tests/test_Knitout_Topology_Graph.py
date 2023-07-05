from unittest import TestCase

from knit_script.knitout_interpreter.Knitout_Interpreter import Knitout_Interpreter
from knit_script.knitout_interpreter.Knitout_Topology_Graph import Knitout_Topology_Graph


class TestKnitout_Topology_Graph(TestCase):
    def test_visualize_yarn_graph(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                ;!knitout-2
                inhook 1
                releasehook 1
                tuck + f1 1
                tuck + f3 1
                tuck - f4 1
                tuck - f2 1
                knit + f1 1
                knit + f2 1
                knit + f3 1
                knit + f4 1
                knit - f4 1
                knit - f3 1
                knit - f2 1
                knit - f1 1
                split + f1 b1 1
                split + f2 b2 1
                split + f3 b3 1
                split + f4 b4 1
                outhook 1
                """
        knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        topo_graph = Knitout_Topology_Graph(context, 2)
        topo_graph.visualize()

    def test_inhook_placement(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                        ;!knitout-2
                        inhook 1
                        releasehook 1
                        inhook 2
                        releasehook 2
                        tuck + f1 1
                        tuck + f2 1
                        tuck + f3 1
                        tuck + f4 1
                        knit - f1 2
                        knit - f2 2
                        knit - f3 2
                        knit - f4 2
                        knit + f4 1
                        knit + f3 1
                        knit + f2 1
                        knit + f1 1
                        knit - f4 2
                        knit - f3 2
                        knit - f2 2
                        knit - f1 2
                        knit + f1 1
                        knit + f2 1
                        knit + f3 1
                        knit + f4 1
                        knit - f1 2
                        knit - f2 2
                        knit - f3 2
                        knit - f4 2
                        outhook 1 2
                        """
        knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        topo_graph = Knitout_Topology_Graph(context, 3)
        sorted_instructions = topo_graph.topo_sort()
        print(sorted_instructions)
        topo_graph.visualize()

    def test_xfer_releasehook(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                        ;!knitout-2
                        inhook 1
                        releasehook 1
                        tuck + f1 1
                        tuck + f2 1
                        tuck + f3 1
                        tuck + f4 1
                        xfer f1 b1
                        xfer f2 b2
                        xfer f3 b3
                        xfer f4 b4
                        knit - b4 1
                        knit - b3 1
                        knit - b2 1
                        knit - b1 1
                        outhook 1
                        """
        knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        topo_graph = Knitout_Topology_Graph(context, 3)
        sorted_instructions = topo_graph.topo_sort()
        print(sorted_instructions)
        topo_graph.visualize()

    def test_topo_sort_carrier(self):
        interpreter = Knitout_Interpreter(False, False)
        pattern = r"""
                ;!knitout-2
                inhook 1
                releasehook 1
                tuck + f1 1
                tuck + f3 1
                tuck - f4 1
                tuck - f2 1
                knit + f1 1
                knit + f2 1
                knit + f3 1
                knit + f4 1
                knit - f4 1
                knit - f3 1
                knit - f2 1
                knit - f1 1
                knit + f1 1
                knit + f2 1
                knit + f3 1
                knit + f4 1
                ;split + f1 b1 1
                ;split + f2 b2 1
                ;split + f3 b3 1
                ;split + f4 b4 1
                outhook 1
                """
        knitout_instructions = interpreter.interpret_knitout(pattern, False, True)
        context = interpreter.context
        topo_graph = Knitout_Topology_Graph(context, 5)
        sorted_instructions = topo_graph.topo_sort()
        print(sorted_instructions)
