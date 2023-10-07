import cast_ons;
with Gauge as 2, Carrier as c5, width as 40, height as 60:{
    with Sheet as s0:{
        cast_ons.alt_tuck_cast_on(width, is_front=True);
        xfer Loops[1::2] across;
    }
    with Sheet as s1:{
        cast_ons.alt_tuck_cast_on(width, is_front=False);
        xfer Loops[1::2] across;
    }
    for r in range(0, height):{
        with Sheet as s0:{
            in reverse direction:{ knit Loops; }
        }
        with Sheet as s1:{
            in reverse direction:{  knit Loops; }
        }
    }
}