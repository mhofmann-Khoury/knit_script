"""A file used to quickly make sure the installation of knitout is working as expected"""
from knit_script.interpret import knit_script_to_knitout, knit_script_to_knitout_to_dat
from knit_script.knit_graphs.knit_graph_viz import visualize_sheet


def _print_knitout(filename: str):
    with open(filename, mode='r') as knitout_file:
        print_str = ""
        for line in knitout_file.readlines():
            print_str += line
        print(print_str)


def installation_test(output_dat: bool = False):
    """
        Runs three quick checks on the installation of Knit Script
    """
    program = r"""
    import cast_ons;
    import stockinette;

    with Carrier as 1, width as 4, height as 4:{
        cast_ons.alt_tuck_cast_on(width);
        stockinette.stst(height);                
    }
            """
    with open("program.ks", mode='w') as file:
        file.write(program)
    knit_graph, _machine_state = knit_script_to_knitout(program, "installation.k", pattern_is_filename=False)
    _print_knitout("installation.k")
    visualize_sheet(knit_graph, "program_knit_graph.png")
    _knit_graph, _machine_state = knit_script_to_knitout("installation_test.ks", "program_from_file.k", pattern_is_filename=True)
    _print_knitout("program_from_file.k")
    if output_dat:
        _knit_graph, _machine_state = knit_script_to_knitout_to_dat("program.ks", "program_for_dat.k", "program.dat", pattern_is_filename=True)


if __name__ == "__main__":
    installation_test()
