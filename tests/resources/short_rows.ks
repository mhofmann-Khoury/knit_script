import cast_ons;

with Carrier as c:{
	cast_ons.alt_tuck_cast_on(pattern_width, tuck_lines=1, knit_lines=base);
	for _ in range(0, pattern_height, 3):{
		in reverse direction:{
			knit Loops;
		}
		in reverse direction:{
			knit Last_Pass[shorts:];
		}
		in reverse direction:{
			knit Last_Pass;
		}
	}

	for _ in range(base):{
		in reverse direction:{
			knit Loops;
		}
	}
}
