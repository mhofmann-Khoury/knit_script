with Carrier as c:{
	in Leftward direction:{
		tuck Front_Needles[1:pattern_width:2];
	}
	assert reverse == Rightward, f"Expected rightward reverse but got {reverse}";
	in reverse direction:{
		tuck Front_Needles[0:pattern_width:2];
	}
	assert reverse == Leftward, f"Expected leftward reverse but got {reverse}";
	in reverse direction:{
		knit Loops;
	}
	in reverse direction:{
		knit Loops;
	}
	releasehook;
	for _ in range(pattern_height):{
		in reverse direction:{
			knit Loops;
		}
	}
}
