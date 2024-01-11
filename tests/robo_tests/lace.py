from knit_script.interpret import knit_script_to_knitout_to_dat

knit_script_to_knitout_to_dat("lace.ks", "lace.k", "lace.dat",
                              pattern_is_filename=True, base_carrier=7, robo_carrier=5,
                              reps=10,
                              robo_height=30)
