import cast_ons;
w = 20;
h = 20;
with Carrier as c1:{
    cast_ons.alt_tuck_cast_on(w);
    xfer Loops[1::2] across;
    for r in range(0, h):{
        in reverse direction:{
            knit Loops;
        }
    }
}