
width = 10;
height = 20;

def cast_on(w):{
	print f"caston {width} loops";
	in Leftward direction:{
		tuck [n for n in Front_Needles[width:1:-2]];
	}
	in Rightward direction:{
		tuck [n for n in Front_Needles[1:width:2]];
	}
}

def prepare_rib_row(start):{
	print "xfer for ribbing";
	xfer [f for f in Front_Needles[start:width+1:2]] across to Back bed;
}

with Gauge as 2, Carrier as 1:{
	//cast on;
	for s in range(0, Gauge):{
		with Sheet as s:{
			cast_on(width);
		}
	}
	for s in range(0, Gauge):{
		with Sheet as s:{
			prepare_rib_row(Sheet);
		}
	}
	for r in range(0, height):{
		for s in range(0, Gauge):{
			with Sheet as s:{
				in reverse direction:{
					knit [l for l in Loops];
				}
			}
		}
	}


}

