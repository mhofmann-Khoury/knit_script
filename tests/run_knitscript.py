from knit_script.interpret import knit_script_to_knitout

# name = "tree"
# knit_script_to_knitout_to_dat(f"{name}.ks", f"{name}.k", f"{name}.dat", pattern_is_filename=True)

# name = "bag"
# knit_script_to_knitout_to_dat(f"{name}.ks", f"{name}.k", f"{name}.dat", pattern_is_filename=True)

# name = "knitjs"
# knit_script_to_knitout_to_dat(f"{name}.ks", f"{name}.k", f"{name}.dat", pattern_is_filename=True)

name = "test"
knit_script_to_knitout(f"{name}.ks", f"{name}_x.k")
# knit_script_to_knitout_to_dat(f"{name}.ks", f"{name}_x.k", f"{name}_x.dat", pattern_is_filename=True)

# success = knitout_to_dat(f"{name}.k", f"{name}.dat")
# assert success, f"Dat file could not be produced from {name}.k"