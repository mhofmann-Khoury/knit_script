import cast_ons;
with Carrier as c1, width as 20, height as 20:{
	cast_ons.alt_tuck_cast_on(width);
	xfer Loops[1::2] across to back bed;
	for r in range(0, height):{
		in reverse direction:{ knit Loops; }
	}
}