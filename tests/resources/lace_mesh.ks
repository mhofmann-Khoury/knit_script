with Carrier as c1:{
	// Cast on loops to match the width of the first course.
	in Leftward direction:{
		tuck Front_Needles[0:width:2];
	}
	in Rightward direction:{
		tuck Front_Needles[1:width:2];
	}
	releasehook;
	// Knit all courses on in the seed pattern.
	for _ in range(0, height, 2):{
		in reverse direction:{
			knit Loops;
		}
		right_decreases = Front_Loops[1::6];
		left_decreases = Front_Loops[5::6];
		yos = [];
		xfer right_decreases 1 to Right to Back bed;
		yos.extend(Last_Pass.keys());
		xfer left_decreases 1 to Left to Back bed;
		yos.extend(Last_Pass.keys());
		xfer Back_Loops across to Front bed;
		in reverse direction:{
			knit Loops;
			tuck yos;
		}
	}
}
