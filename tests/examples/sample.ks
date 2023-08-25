import cast_ons;
size = 10;
with Carrier as c1:{
	co_needles = Front_Needles[0:size:2];
	co_needles.extend(Back_Needles[1:size:2]);
	cast_ons.alt_tuck_needle_set(co_needles);
	in reverse direction:{
		knit Loops;
	}
	for r in range(1, size):{
		xfer Loops across;
		in reverse direction:{
			knit Loops;
		}
	}
}