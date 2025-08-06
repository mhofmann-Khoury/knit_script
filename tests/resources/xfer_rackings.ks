with Carrier as 1:{
	in Leftward direction:{
		knit Front_Needles[3: 10];
	}
	releasehook;
	cut Carrier;
}
xfer Loops across to Back bed; // Move only front to back, 0 rack
xfer Loops across to Front Bed; // Move only back to front, 0 rack
xfer Loops[0::2] across; // move some front to back, 0 rack
xfer Loops across; // move mix, 0 rack
xfer Back_Loops across to Front bed; // return everything to front, 0 rack
xfer Loops 2 to Left; // Move front loops 2 left
xfer Loops 2 to Right; // move back loops 2 right
xfer Front_Loops across to Back bed; // return everything to back, 0 rack
xfer Loops 2 to Left; // Move back loops 2 left
xfer Loops 2 to Right; // move front loops 2 right
