// Build a standard Stockinette Swatch with an alternating tuck cast on
width = 20;
height = 20;

def cast_on(w):{
	print f"Cast on {w} loops";
	in Leftward direction:{
		tuck [n for n in Front_Needles[1:w:2]];
	}
	in reverse direction:{
		tuck [n for n in Front_Needles[0:w:2]];
	}
}

with Carrier as 1:{
	cast_on(width);
	for r in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
	}
}