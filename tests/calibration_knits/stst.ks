// Build a standard Stockinette Swatch with an alternating tuck cast on
import cast_ons;
width = 20;
height = 20;

with Carrier as 1:{
	cast_ons.alt_tuck_cast_on(width);
	for r in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
	}
}

import cast_ons;
w = 20;
h = 20;
with Carrier as c1:{
    cast_ons.alt_tuck_cast_on(w);
    for r in range(0, h):{
        in reverse direction:{
            knit Loops;
        }
    }
}