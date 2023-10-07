import cast_ons;
with Gauge as 2, Carrier as c1, width as 60, height as 60:{
    with Sheet as s0:{ cast_ons.alt_tuck_cast_on(width, is_front=True); }
    with Sheet as s1:{ cast_ons.alt_tuck_cast_on(width, is_front=True); }
    with Sheet as s0:{ push Loops[: int(width / 2)] to back; }
    for r in range(0, height):{
        with Carrier as c2, Sheet as s1:{
            in reverse direction:{  knit Loops; }
        }
        with Carrier as c1, Sheet as s0:{
            in current direction:{ knit Loops; }
        }
    }
}