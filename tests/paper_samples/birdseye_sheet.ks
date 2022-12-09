// Make a swatch using a birdseye jacquard technique
// Produces a 2 sided fabric.
// Back side is an unbalanced birdseye pattern with 3 colors
// Front has an alternating stripes on a diagonal followed by a solid color block
width = 20;
height = 20;

def all_needle_knit(h):{
	for i in range(0,h):{
		in reverse direction:{
			knit Loops;
		}
	}
}

def all_needle_cast_on():{
	in Leftward direction:{
		tuck Front_Needles[0:width:2];
		tuck Back_Needles[1:width:2];
	}
	in reverse direction:{
		tuck Front_Needles[1:width:2];
		tuck Back_Needles[0:width:2];
	}
	all_needle_knit(2);

}

with Carrier as 1:{
	print f"Cast on with {Carrier}";
	all_needle_cast_on();
}
with Carrier as 2:{
	print f"Establish {Carrier}";
	all_needle_knit(2);
}
with Carrier as 3:{
	print f"Establish {Carrier}";
	all_needle_knit(2);
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