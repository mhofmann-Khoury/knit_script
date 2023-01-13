// Make a tube of kp ribbing. Front of the round is on sheet 0. Back is on Sheet 2
import cast_ons;

with Gauge as 2, Carrier as 1, width as 10, height as 20:{
	// cast on front and back of the tube
	for s in range(0, Gauge):{
		with Sheet as s:{
			cast_ons.alt_tuck_cast_on(width, is_front=s%2==0);
		}
	}
	for s in range(0, Gauge):{
		with Sheet as s:{
		    xfer Loops[s::2] across; // xfer every other loop to opposite bed for knit purl pattern
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


