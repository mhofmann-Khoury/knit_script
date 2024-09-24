from knit_script.interpret_knit_script import knit_script_to_knitout_to_dat

knit_script_to_knitout_to_dat("inlay_test.ks", "inlay_test.k", "inlay_test.dat", pattern_is_filename=True,
                              width=40,
                              height=40,
                              base_yarn=5, inlay_yarn=3)
