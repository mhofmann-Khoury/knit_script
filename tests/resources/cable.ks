import cast_ons;

with Carrier as c:{
	cast_ons.alt_tuck_cast_on(pattern_width);
	go_right = True;
	for _ in range(0, pattern_height, 2):{
		in reverse direction:{
			knit Loops;
		}
		left_cables = Front_Loops[1::6];
		left_cables.extend(Front_Loops[2::6]);
		right_cables = Front_Loops[3::6];
		right_cables.extend(Front_Loops[4::6]);
		xfer left_cables across to Back bed;
		left_cables = Last_Pass.values();
		xfer right_cables across to Back bed;
		right_cables = Last_Pass.values();
		if go_right:{
			xfer right_cables 2 to Left to Front Bed;
			xfer Back_Loops 2 to Right to Front Bed;
		} else:{
			xfer left_cables 2 to Right to Front Bed;
			xfer Back_Loops 2 to Left to Front Bed;
		}
		go_right = not go_right;
		in reverse direction:{
			knit Loops;
		}
	}
}
