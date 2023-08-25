from knitout import Writer
def opposite_needle(needle: tuple[str, int]) -> tuple[str, int]:
    if needle[0] == 'f':
        return 'b', needle[1]
    else:
        return 'f', needle[1]
writer = Writer('1 2 3 4 5 6 7 8 9 10')
c = '1'
size = 20
s0 = [('f', i) for i in range(0, (size*2)-1, 2)]
s1 = [('b', i) for i in range(1, size*2, 2)]
s0_rib = [n if i % 2 == 0 else opposite_needle(n) for i, n in enumerate(s0)]
s0_returns = [(opposite_needle(n), n) for n in s0_rib if n[0] == 'b']
s0_layer = [(n, opposite_needle(n)) for n in s0_rib if n[0] == 'b']
s1_rib = [n if i % 2 == 0 else opposite_needle(n) for i, n in enumerate(s1)]
s1_returns = [(opposite_needle(n), n) for n in s1_rib if n[0] == 'f']
s1_layer = [(n, opposite_needle(n)) for n in s1_rib if n[0] == 'f']
writer.inhook(c)
for n in s0[-1::-2]:
    writer.tuck('-', n, c)
writer.releasehook(c)
for n in s0[::2]:
    writer.tuck('+', n, c)
for n1, n2 in reversed(s0_returns):
    writer.xfer(n1[0], n1[1], n2[0], n2[1])
for n1, n2 in s0_layer:
    writer.xfer(n1[0], n1[1], n2[0], n2[1])
for n in s1[-1::-2]:
    writer.tuck('-', n, c)
for n in s1[::2]:
    writer.tuck('+', n, c)
for n1, n2 in reversed(s1_returns):
    writer.xfer(n1[0], n1[1], n2[0], n2[1])
reverse = '-'
for r in range(0, size * 2):
    if reverse == '-':
        for n1, n2 in s1_layer:
            writer.xfer(n1[0], n1[1], n2[0], n2[1])
        for n1, n2 in s0_returns:
            writer.xfer(n1[0], n1[1], n2[0], n2[1])
        for n in reversed(s0_rib):
            writer.knit(reverse, n, c)
        reverse = '+'
    else:
        for n1, n2 in s0_layer:
            writer.xfer(n1[0], n1[1], n2[0], n2[1])
        for n1, n2 in s1_returns:
            writer.xfer(n1[0], n1[1], n2[0], n2[1])
        for n in s1_rib:
            writer.knit(reverse, n, c)
        reverse = '-'
writer.outhook(c)

# End Line Counting
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat

name = "fe_rib_tube"
writer.write(f'{name}.k')
knitout_to_dat(f"{name}.k", f"{name}.dat")
