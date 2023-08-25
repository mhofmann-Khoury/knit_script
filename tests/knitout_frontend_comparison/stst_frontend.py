from knit_script.interpret import knit_script_to_knitout
from knit_script.knitout_interpreter.Knitout_Interpreter import Knitout_Interpreter
from knitout import Writer

name = "stst"
knit_script_to_knitout(f"{name}.ks", f"{name}.k", pattern_is_filename=True)

w = 20
h = 20
wr = Writer('1 2 3 4 5 6 7 8 9 10')
c = '1'
wr.inhook(c)
for i in range(w - 1, 0, -2):
    wr.tuck('-', ('f', i), c)
wr.releasehook(c)
for i in range(0, w, 2):
    wr.tuck('+', ('f', i), c)
for j in range(0, h):
    if j % 2 == 0:
        for i in range(w, 0, -1):
            wr.knit('-', ('f', i - 1), c)
    else:
        for i in range(0, w):
            wr.knit('+', ('f', i), c)

wr.outhook(c)

wr.write('stst_py.k')

interpreter = Knitout_Interpreter(False, False)
interpreter.write_trimmed_knitout('stst_py.k', 'stst_py.k')
interpreter.write_trimmed_knitout('stst.k', 'stst.k')
