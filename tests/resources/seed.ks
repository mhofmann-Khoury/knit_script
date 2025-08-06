import cast_ons;

with Carrier as c:{
	cast_ons.alt_tuck_cast_on(pattern_width);
	xfer Front_Loops[1::2] across to Back bed;
	for h in range(pattern_height):{
		in reverse direction:{
			knit Loops;
		}
		if h < (pattern_height -1):{
			xfer Loops across;
		} else:{
			xfer Back_Loops across to Front bed;
		}
	}
}
