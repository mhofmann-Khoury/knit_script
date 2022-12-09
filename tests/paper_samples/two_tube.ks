

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


with Gauge as 3, Carrier as 1:{
	for s in range(0, Gauge):{
		with Sheet as s:{
			cast_on(width);
		}
	}
	with Sheet as 1:{
		prepare_rib_row(1);
	}
	with Sheet as 2:{
		xfer [f for f in Front_Loops] across to Back bed;
	}
	for r in range(0, height):{
		for s in range(0, Gauge):{
			with Sheet as s:{
				in reverse direction:{
					knit [ l for l in Loops];
				}
			}
		}
	}

}