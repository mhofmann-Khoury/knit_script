import cast_ons;

with Carrier as c:{
	cast_ons.alt_tuck_cast_on(pattern_width);
	go_right = True;
	for _ in range(0, pattern_height, 2):{
		in reverse direction:{
			knit Loops;
		}
		xfer Front_Loops[1::4] across to Back bed;
		tucks = Last_Pass.keys();
		if go_right:{
			xfer Back_Loops 1 to Right to Front bed;
		} else:{
			xfer Back_Loops 1 to Left to Front bed;
		}
		go_right = not go_right;
		in reverse direction:{
			knit Front_Loops;
			tuck tucks;
		}
	}
}
