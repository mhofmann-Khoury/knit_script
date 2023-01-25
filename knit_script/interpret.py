"""Console function for processing knit_script"""
import getopt
import sys
from typing import Optional

from knit_script.knit_graphs.Knit_Graph import Knit_Graph
from knit_script.knit_script_interpreter.Knit_Script_Interpreter import Knit_Script_Interpreter
from knit_script.knit_script_interpreter.compile_knitout import knitout_to_dat


def knit_script_to_knitout(pattern: str, out_file_name: str, pattern_is_filename: bool = True) -> Knit_Graph:
    """
    Processes a knit script pattern into knitout and a dat file for shima seiki machines and returns the resulting knit graph from the operations
    :param: pattern: the knit script pattern or a file containing it
    :param: out_file_name: the output location for knitout and dat files
    :param: pattern_is_filename: if true, pattern is a filename
    :return: the KnitGraph constructed during parsing on virtual machine
    """
    interpreter = Knit_Script_Interpreter()
    _, knit_graph = interpreter.write_knitout(pattern, out_file_name, pattern_is_filename)
    return knit_graph


def knit_script_to_knitout_to_dat(pattern: str, knitout_name: str, dat_name: Optional[str] = None, pattern_is_filename: bool = False) -> Knit_Graph:
    """
    Processes a knit script pattern into knitout and a dat file for shima seiki machines and returns the resulting knit graph from the operations
    :param: pattern: the knit script pattern or a file containing it
    :param: knitout_name: the output location for knitout
    :param: dat_name: output location for dat file. If none, dat file will share name with knitout
    :param: pattern_is_filename: if true, pattern is a filename
    :return: the KnitGraph constructed during parsing on virtual machine
    """
    interpreter = Knit_Script_Interpreter()
    _, knit_graph = interpreter.write_knitout(pattern, knitout_name, pattern_is_filename)
    success = knitout_to_dat(knitout_name, dat_name)
    assert success, f"Dat file could not be produced from {knitout_name}"
    return knit_graph


def main():
    """
        Run the interpreter to generate knitout and optionally a dat file.
        First argument is the input pattern. Either a string or a filename
        -k and --knitout specify the knitout file name. Defaults to same name as pattern
        -d and --dat specify the dat file name. Defaults to none and no DAT file is produced
        --string specifies if the pattern is a string. Defaults to false
    """
    argv = sys.argv[1:]
    pattern_str = False
    knitout = None
    dat = None
    try:
        opts, args = getopt.getopt(argv, "k:d:",
                                   ["knitout =", "dat =", "string"])
        assert len(args) == 1, f"Expected knit script pattern but got {args}"
        pattern = args[0]
        for opt, arg in opts:
            if opt in ['-k', '--knitout']:
                knitout = arg
            elif opt in ['-d', '--dat']:
                dat = arg
            elif opt == "--string":
                pattern_str = True
        if knitout is None:
            assert not pattern_str, "Cannot make knitout file without a output name or a knit script file"
            knitout = pattern[0:pattern.index('.')] + '.k'
        if dat is not None:
            knit_graph = knit_script_to_knitout_to_dat(pattern, knitout, dat, pattern_is_filename=not pattern_str)
            print(f"Generated Knitout to {knitout} and DAT to {dat}")
        else:
            knit_graph = knit_script_to_knitout(pattern, knitout, pattern_is_filename=not pattern_str)
            print(f"Generated Knitout to {knitout}")

    except getopt.GetoptError as e:
        print(e)


if __name__ == "__main__":
    main()
