from knitout import Writer
writer = Writer('1 2 3 4 5 6 7 8 9 10')
carrier = '1'
width = 40
height = 10
writer.inhook(carrier)
for i in range(width - 1, 0, -2):
    writer.tuck('-', ('f', i), carrier)
writer.releasehook(carrier)
for i in range(0, width, 2):
    writer.tuck('+', ('f', i), carrier)
reverse = '-'
for r in range(0, height):
    if reverse == '-':
        for i in range(width - 1, -1, -1):
            writer.knit(reverse, ('f', i), carrier)
        reverse = '+'
    else:
        for i in range(0, width):
            writer.knit(reverse, ('f', i), carrier)
        reverse = '-'
writer.outhook(carrier)
# End Line Counting
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat

name = "fe_mod_stst"
writer.write(f'{name}.k')
knitout_to_dat(f"{name}.k", f"{name}.dat")
