// Make a swatch using a birdseye jacquard technique
// Produces a 2 sided fabric.
// Back side is an unbalanced birdseye pattern with 3 colors
// Front has an alternating stripes on a diagonal followed by a solid color block

import stockinette;
import cast_ons;

width = 20;
height = 20;

with Carrier as 1:{
	print f"Cast on with {Carrier}";
	cast_ons.all_needle_cast_on(width);
	stockinette.all_needle_stst(2);
}
with Carrier as 2:{
	print f"Establish {Carrier}";
	stockinette.all_needle_stst(2);
}
with Carrier as 3:{
	print f"Establish {Carrier}";
	stockinette.all_needle_stst(2);
}

color_switch = 1; // index to switch to full color block

for r in range(0, height):{
	print f"Color Switch at {color_switch}";
	with Carrier as 1:{
		print "Knit 1 on even backs, even up to color switch front";
		in reverse direction:{
			knit Back_Loops[0: width: 2];
			knit Front_Loops[0:color_switch:2];
		}
	}
	with Carrier as 2:{
		print "Knit 2 on odd backs, odd up to color switch front";
		in reverse direction:{
			knit Back_Loops[1: width: 2];
			knit Front_Loops[1:color_switch:2];
		}
	}
	with Carrier as 3:{
		print "Knit 3 on even backs, all after color switch on front";
		in reverse direction:{
			knit Back_Loops[0:width:2];
			knit Front_Loops[color_switch:width];
		}
	}

	color_switch = (color_switch + 1) % width;
}