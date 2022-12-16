// Make a tube of kp ribbing. Front of the round is on sheet 0. Back is on Sheet 2
import cast_ons;
import stockinette;

width = 10;
height = 20;


def prepare_rib_row(start):{
	print "xfer for ribbing";
	xfer Front_Needles[start:width+1:2] across to Back bed;
}

with Gauge as 2, Carrier as 1:{
	//cast on;
	for s in range(0, Gauge):{
		with Sheet as s:{
			cast_ons.alt_tuck_cast_on(width);
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
					knit Loops;
				}
			}
		}
	}


}

