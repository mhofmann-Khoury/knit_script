import cast_ons;
width = 20;
height = 1;
with Carrier as c1:{
	cast_ons.alt_tuck_cast_on(width);
	xfer Loops[1::2] across;
	for r in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
	}
	xfer Back_Loops across to front bed;
	for _ in range(0, 10):{
		in reverse direction:{
			knit Loops;
		}
	}
}