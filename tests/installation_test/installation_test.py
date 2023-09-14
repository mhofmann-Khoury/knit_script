"""A file used to quickly make sure the installation of knitout is working as expected"""
from knit_script.interpret import knit_script_to_knitout, knit_script_to_knitout_to_dat


def installation_test():
    """
        Runs three quick checks on the installation of Knit Script
    """
    program = r"""
            import cast_ons;
            import stockinette;
            
            with Carrier as 1, width as 10, height as 10:{
                cast_ons.alt_tuck_cast_on(width);
                stockinette.stst(height);                
            }
        """
    print("Running Test Program from String")
    knit_script_to_knitout(program, "installation_test_from_string.k", pattern_is_filename=False)
    print("Running Test Program from File")
    knit_script_to_knitout("installation_test.ks", "installation_test_from_file.k", pattern_is_filename=True)
    print("Your Installation is successfully Interpreting KnitScript")
    print("Running Test Program from File to DAT File")
    knit_script_to_knitout_to_dat("installation_test.ks", "installation_test_to_dat.k", "installation_test.dat", pattern_is_filename=True)
    print("Your installation is successfully Interpreting KnitScript and generating DAT files")


if __name__ == "__main__":
    installation_test()
