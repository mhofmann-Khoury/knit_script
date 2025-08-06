import cast_ons;
pause; // before any action, including carrier setting -> sets after the first carriage pass
with Carrier as c:{
	in Leftward direction:{
		knit Front_Needles[0:pattern_width];
	}
	in Rightward direction:{
		knit Loops;
	}
	releasehook;
	pause; //pause before releashook -> occurs after next leftward carriage pass
	in Leftward direction:{
		knit Front_Needles[0:pattern_width];
	}
	in Rightward direction:{
		knit Loops;
	}
	pause;//pause before xfer ->> occurs with next xfer pass
	xfer Front_Loops[1::2] across to Back bed;
	pause;// pause between xfers ->> occurs with next xfer pass
	xfer Back_Loops across to Front bed;
	xfer Front_Loops[1::2] across to Back bed;
	xfer Back_Loops across to Front bed;
	pause; // pause after all xfers. ->> occurs with next pass
	in Leftward direction:{
		knit Front_Needles[0:pattern_width];
	}
	in Rightward direction:{
		knit Loops;
	}
	pause; // pause before Leftward -> set with this leftward pass
	in Leftward direction:{
		knit Loops;
	}
	in Rightward direction:{
		knit Loops;
	}
	in Leftward direction:{
		knit Loops;
	}
	pause; // pause after leftward, before rightward -> set with the following rightward pass
	in Rightward direction:{
		knit Loops;
	}
	in Leftward direction:{
		knit Loops;
	}
	in reverse direction:{
		knit Loops;
	}
	pause; // pause after rightward -> set on the outhook operation.
}
