from unittest import TestCase

from Swatch_Knitter import *
from knit_script.knit_graphs.knit_graph_viz import visualize_sheet


class Test_Swatch_Knitter(TestCase):
    def test_knit_jersey(self):
        knit_graph = jersey_knit(10, 10)
        out_graph = knit_swatch(knit_graph, "jersey")
        visualize_sheet(out_graph)

    def test_knit_seed(self):
        knit_graph = seed_stitch(10, 10)
        out_graph = knit_swatch(knit_graph, "seed")
        visualize_sheet(out_graph)

    def test_knit_rib(self):
        knit_graph = kp_rib()
        out_graph = knit_swatch(knit_graph, "rib")
        visualize_sheet(out_graph)

    def test_knit_lace(self):
        knit_graph = lace()
        out_graph = knit_swatch(knit_graph, "lace")
        visualize_sheet(out_graph)

    def test_knit_cable(self):
        knit_graph = cable()
        out_graph = knit_swatch(knit_graph, "cable")
        visualize_sheet(out_graph)
