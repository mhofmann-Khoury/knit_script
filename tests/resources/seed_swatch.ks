with Carrier as c1:{
	// Cast on loops to match the width of the first course.
	in Leftward direction:{
		tuck Front_Needles[0:width:2];
	}
	in Rightward direction:{
		tuck Front_Needles[1:width:2];
	}
	releasehook;
	xfer Front_Loops[1::2] across to back bed; // from alternating knit purl pattern.
	// Knit all courses on in the seed pattern.
	for _ in range(height-1):{
		in reverse direction:{
			knit Loops;
		}
		xfer Loops across;
	}
	in reverse direction:{
		knit Loops;
	}
}
