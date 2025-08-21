with Carrier as c1:{
	// Cast on loops to match the width of the first course.
	in Leftward direction:{
		tuck Front_Needles[0:width:2];
	}
	in Rightward direction:{
		tuck Front_Needles[1:width:2];
	}
	releasehook;
	// Knit all courses on the front bed;
	for _ in range(height):{
		in reverse direction:{
			knit Loops;
		}
	}
}
