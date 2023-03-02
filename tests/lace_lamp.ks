;;Width: 500;
import cast_ons;

def one_sheet_lace(width_reps, height_reps):{
	rep_width = 4;
	rep_start = 2;
	rep_end = 2 + (width_reps*rep_width);
	with sheet as s0, Gauge as 1:{
		xfer Back_Loops across to front bed; // move everything onto front bed
		tucks = Loops[1::2];
		left_xfer = [Loops[1]];
		left_xfer.extend(Loops[rep_start+3:rep_end: rep_width]);
		right_xfer = [Loops[-2]];
		right_xfer.extend(Loops[rep_start+1:rep_end: rep_width]);
		all_xfer = [n for n in left_xfer];
		all_xfer.extend(right_xfer);
		left_xfer = [n.opposite() for n in left_xfer]; // transfers will be from back bed
		right_xfer = [n.opposite() for n in right_xfer]; // transfer will be from back bed
		for r in range(0, height_reps):{
			in reverse direction:{ // knit lace base
				knit Loops;
			}
			xfer all_xfer across to back bed;
			if r%2==0:{//left xfers first
				xfer left_xfer 1 to Leftward to front bed;
				xfer right_xfer 1 to Rightward to front bed;
			} else: {//right xfers first
				xfer right_xfer 1 to Rightward to front bed;
				xfer left_xfer 1 to Leftward to front bed;
			}
			in reverse direction:{
				knit Loops;
				tuck tucks;// yarn overs
			}
		}
	}
}

def knit_back_loop(height):{
	xfer Front_Loops[1::2] across to back bed;
	print f"Loops before gauge change: {Loops}";
	with Gauge as 2, Sheet as s1:{
		print f"Sheet after gauge change: {Sheet}";
		print f"Loops after gauge change: {Loops}";
		for r in range(0, height):{
			in reverse direction:{
				knit Loops;
			}
		}
	}
	xfer Loops across to front bed;
}

def knit_front_loop(height):{
	with Gauge as 2, Sheet as s1:{
		push Loops to front;
		for r in range(0, height):{
			in reverse direction:{
				knit Loops;
			}
		}
	}
}

with Gauge as 1, Carrier as c1:{
	wr = 3;
	width = 2 +(wr*4) + 3;
	loop_reps = 2;
	cast_ons.alt_tuck_cast_on(width);
	for i in range(0, loop_reps):{
		one_sheet_lace(wr, 4);
		knit_back_loop(10);
		one_sheet_lace(wr, 4);
		knit_front_loop(10);
	}
	one_sheet_lace(wr, 4);
}