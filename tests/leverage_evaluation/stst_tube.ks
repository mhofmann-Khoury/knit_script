import cast_ons;
with Gauge as 2, Carrier as c1, width as 20, height as 20:{
    with Sheet as s0:{
        cast_ons.alt_tuck_cast_on(width, is_front=True);
    }
    with Sheet as s1:{
        cast_ons.alt_tuck_cast_on(width, is_front=False);
    }
    for r in range(0, height):{
        with Sheet as s0:{
            in reverse direction:{  knit Loops; }
        }
        with Sheet as s1:{
            in reverse direction:{  knit Loops; }
        }
    }
}