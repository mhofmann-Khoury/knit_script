from knitout import Writer
writer = Writer('1 2 3 4 5 6 7 8 9 10')
c = '1'
width = 20
height = 20
writer.inhook(c)
for i in range(width - 1, 0, -2):
    writer.tuck('-', ('f', i), c)
writer.releasehook(c)
for i in range(0, width, 2):
    writer.tuck('+', ('f', i), c)
for i in range(width-1, 0, -2):
    writer.xfer('f', i, 'b', i)
reverse = '-'
for r in range(0, height):
    if reverse == '-':
        for i in range(width - 1, -1, -1):
            if i % 2 == 0:
                writer.knit(reverse, ('f', i), c)
            else:
                writer.knit(reverse, ('b', i), c)
        reverse = '+'
    else:
        for i in range(0, width):
            if i % 2 == 0:
                writer.knit(reverse, ('f', i), c)
            else:
                writer.knit(reverse, ('b', i), c)
        reverse = '-'
writer.outhook(c)

# End Line Counting
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat
name = "fe_rib"
writer.write(f'{name}.k')
knitout_to_dat(f"{name}.k", f"{name}.dat")
