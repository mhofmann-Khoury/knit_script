from knit_script.interpret import knit_script_to_knitout_to_dat

name = "tree"
knit_script_to_knitout_to_dat(f"{name}.ks", f"{name}.k", f"{name}.dat", pattern_is_filename=True)

