// make three layers in the round forming two joined tubes.
// Front sheet: Stockinette layer
// Middle sheet: k2p2 rib
// Back sheet: Reverse stockinette

width = 10;
height = 20;

def cast_on(w):{
	print f"caston {width} loops";
	in Leftward direction:{
		tuck Front_Needles[1:w:2];
	}
	in reverse direction:{
		tuck Front_Needles[0:w:2];
	}
}

def prepare_rib_row(w):{
	// collect 2nd and 3rd loops to make purls on back bed
	xfer_knits = [f for i, f in enumerate(Front_Loops) if (i%4 == 2) or (i%4==3)];
	xfer xfer_knits across to Back bed;
}


with Gauge as 3, Carrier as 1:{
	for s in range(0, Gauge):{
		with Sheet as s:{
			cast_on(width);
		}
	}
	front_sheet = 0;
	mid_sheet = 1;
	back_sheet = 2;
	with Sheet as mid_sheet:{ // middle
		prepare_rib_row(width);
	}
	with Sheet as back_sheet:{
		xfer Front_Loops across to Back bed;
	}
	for r in range(0, height):{
		for s in range(0, Gauge):{
			with Sheet as s:{
				in reverse direction:{
					knit Loops;
				}
			}
		}
	}

}