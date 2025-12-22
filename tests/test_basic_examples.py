from unittest import TestCase

from resources.interpret_test_ks import interpret_test_ks
from resources.load_test_resources import load_test_resource


class Test_Basic_Examples(TestCase):

    def test_stst(self):
        program = load_test_resource("stst.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=4, pattern_height=4)

    def test_all_needles(self):
        program = load_test_resource("all_needle.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=4, pattern_height=4)

    def test_all_needles_racked(self):
        program = load_test_resource("all_needle_racked.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=4, pattern_height=2)

    def test_cable(self):
        program = load_test_resource("cable.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_gauged_sheets(self):
        program = load_test_resource("gauged_sheets.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_half_gauge(self):
        program = load_test_resource("half_gauge.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_intarsia_float_blocks(self):
        program = load_test_resource("intarsia_float_block.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, border=4, block_width=4, block_height=4, white=1, black=2)

    def test_jacquard_stripes(self):
        program = load_test_resource("jacquard_stripes.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, pattern_width=6, pattern_height=4, white=1, black=2)

    def test_lace(self):
        program = load_test_resource("lace.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_pauses(self):
        program = load_test_resource("pauses.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_plating(self):
        program = load_test_resource("plating.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, stripe_size=2, stripes=3, pattern_height=4, white=1, black=2)

    def test_rib(self):
        program = load_test_resource("rib.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_seed(self):
        program = load_test_resource("seed.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_shift(self):
        program = load_test_resource("shift.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4, shift=2)

    def test_short_rows(self):
        program = load_test_resource("short_rows.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4, base=2, shorts=1)

    def test_splits(self):
        program = load_test_resource("splits.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_tubes(self):
        program = load_test_resource("tube.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_tuck_2_lines(self):
        program = load_test_resource("tuck_2_lines.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_tuck_line(self):
        program = load_test_resource("tuck_line.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_weird_moves(self):
        program = load_test_resource("weird_carriage_moves.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)

    def test_xfer_rackings(self):
        program = load_test_resource("xfer_rackings.ks")
        interpret_test_ks(program, pattern_is_filename=True, print_k_lines=False, c=1, pattern_width=6, pattern_height=4)
