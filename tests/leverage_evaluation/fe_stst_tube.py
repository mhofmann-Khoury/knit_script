from knitout import Writer
writer = Writer('1 2 3 4 5 6 7 8 9 10')
c = '1'
size = 20
s0 = [('f', i) for i in range(0, (size * 2) - 1, 2)]
s1 = [('b', i) for i in range(1, size * 2, 2)]
writer.inhook(c)
for n in s0[-1::-2]:
    writer.tuck('-', n, c)
writer.releasehook(c)
for n in s0[::2]:
    writer.tuck('+', n, c)
for n in s1[-1::-2]:
    writer.tuck('-', n, c)
for n in s1[::2]:
    writer.tuck('+', n, c)
reverse = '-'
for r in range(0, size * 2):
    if reverse == '-':
        for n in reversed(s0):
            writer.knit(reverse, n, c)
        reverse = '+'
    else:
        for n in s1:
            writer.knit(reverse, n, c)
        reverse = '-'
writer.outhook(c)

# End Line Counting
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat
name = "fe_stst_tube"
writer.write(f'{name}.k')
knitout_to_dat(f"{name}.k", f"{name}.dat")
