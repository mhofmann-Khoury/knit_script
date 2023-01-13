//make stripes of different sheets of color. Alternate layers to change colors
import cast_ons;
import stockinette;

stripe_width = 8;
height = 20;
colors = 3;
width = colors * stripe_width;

def cast_on_knit(w, knit_rows=2):{
	print f"cast on {width} loops";
	in Leftward direction:{
		tuck Front_Needles[1:width:2];
	}
	in reverse direction:{
		tuck Front_Needles[0:width:2];
	}
	for r in range(0,knit_rows):{
		in reverse direction:{
			knit Front_Loops;
		}
	}
}

with Gauge as colors:{

	for s in range(0, Gauge):{
		with Sheet as s, Carrier as s+1:{
			cast_ons.alt_tuck_cast_on(width);
			stockinette.stst(2);
		}
	}
    for c in range(0, colors):{
        start = c * stripe_width;
        end = (c+1) * stripe_width;
        stripe = [n for n in Front_Needles[start:end]];
        push stripe c Backward;
    }

	for r in range(0, height):{
		for s in range(0, Gauge):{
			with Sheet as s, Carrier as s+1:{
				in reverse direction:{
					knit Loops;
				}
			}
		}
	}
}