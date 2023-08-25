from knitout import Writer
def opposite_needle(needle: tuple[str, int]):
    if needle[0] == 'f':
        return 'b', needle[1]
    else:
        return 'f', needle[1]
writer = Writer('1 2 3 4 5 6 7 8 9 10')
c1 = '1'
c2 = '2'
size = 20
s0 = [('f', i) for i in range(0, (size * 2) - 1, 2)]
s1 = [('f', i) for i in range(1, size * 2, 2)]
s0_back_stripe = [n for n in s0[:int(size / 2)]]
s1_front_stripe = [n for n in s1[:int(size / 2)]]
s1_back_stripe = [n for n in s1[int(size / 2):]]
writer.inhook(c1)
writer.inhook(c2)
for n in s0[-1::-2]:
    writer.tuck('-', n, c1)
writer.releasehook(c1)
for n in s0[::2]:
    writer.tuck('+', n, c1)
for n in s1[-1::-2]:
    writer.tuck('-', n, c1)
for n in s1[::2]:
    writer.tuck('+', n, c1)
for n in s1:
    op_n = opposite_needle(n)
    writer.xfer(n[0], n[1], op_n[0], op_n[1])
for n in s1_front_stripe:
    op_n = opposite_needle(n)
    writer.xfer(op_n[0], op_n[1], n[0], n[1])
reverse = '-'
for r in range(0, size):
    if size/2 == r:
        s0_front_stripe = [n for n in s0[:int(size / 2)]]
        s0_back_stripe = [n for n in s0[int(size / 2):]]
        for n in s1_front_stripe:
            op_n = opposite_needle(n)
            writer.xfer(n[0], n[1], op_n[0], op_n[1])
        s1_front_stripe = [n for n in s1[int(size / 2):]]
        for n in s1_front_stripe:
            op_n = opposite_needle(n)
            writer.xfer(op_n[0], op_n[1], n[0], n[1])
        s1_back_stripe = [n for n in s1[:int(size / 2)]]
    if reverse == '-':
        for n in s0_back_stripe:  # peel s0 back stripe to back
            op_n = opposite_needle(n)
            writer.xfer(n[0], n[1], op_n[0], op_n[1])
        for n in s1_back_stripe:  # put s1 back stripe on front for knitting
            op_n = opposite_needle(n)
            writer.xfer(op_n[0], op_n[1], n[0], n[1])
        for n in reversed(s1):
            writer.knit(reverse, n, c2)
        if r == 0:
            writer.releasehook(c2)
        for n in s1_back_stripe:  # peel s1 back stripe to back
            op_n = opposite_needle(n)
            writer.xfer(n[0], n[1], op_n[0], op_n[1])
        for n in s0_back_stripe:  # put s1 back stripe on front for knitting
            op_n = opposite_needle(n)
            writer.xfer(op_n[0], op_n[1], n[0], n[1])
        for n in reversed(s0):
            writer.knit(reverse, n, c1)
        reverse = '+'
    else:
        for n in s0_back_stripe:  # peel s0 back stripe to back
            op_n = opposite_needle(n)
            writer.xfer(n[0], n[1], op_n[0], op_n[1])
        for n in s1_back_stripe:  # put s1 back stripe on front for knitting
            op_n = opposite_needle(n)
            writer.xfer(op_n[0], op_n[1], n[0], n[1])
        for n in s1:
            writer.knit(reverse, n, c2)
        for n in s1_back_stripe:  # peel s1 back stripe to back
            op_n = opposite_needle(n)
            writer.xfer(n[0], n[1], op_n[0], op_n[1])
        for n in s0_back_stripe:  # put s1 back stripe on front for knitting
            op_n = opposite_needle(n)
            writer.xfer(op_n[0], op_n[1], n[0], n[1])
        for n in s0:
            writer.knit(reverse, n, c1)
        reverse = '-'
writer.outhook(c1)
writer.outhook(c2)

# End Line Counting
from knit_script.knitout_compilers.compile_knitout import knitout_to_dat
name = "fe_squares"
writer.write(f'{name}.k')
knitout_to_dat(f"{name}.k", f"{name}.dat")
