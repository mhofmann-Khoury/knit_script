import cast_ons;

with Carrier as c:{
	cast_ons.alt_tuck_cast_on(pattern_width, tuck_lines=1, knit_lines=1);

	for _ in range(pattern_height):{
		in reverse direction:{
			knit Loops;
		}
		print "start right shift";
		xfer Loops shift to Right;
	}
	for _ in range(pattern_height):{
		in reverse direction:{
			knit Loops;
		}
		xfer Loops shift to Left;
	}
	in reverse direction:{
		knit Loops;
	}
}
