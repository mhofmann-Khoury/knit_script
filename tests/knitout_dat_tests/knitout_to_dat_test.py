from knit_script.knitout_compilers.compile_knitout import knitout_to_dat

knitout_name = "in_test.k"
dat_name = "test.dat"
success = knitout_to_dat(knitout_name, dat_name)
assert success, f"Dat file could not be produced from {knitout_name}"
