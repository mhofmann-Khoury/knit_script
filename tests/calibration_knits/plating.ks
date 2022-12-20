
import cast_ons;
width = 20;
stripe_height = 5;

def knit_stripe():{
	for r in range(0, stripe_height):{
		in reverse direction:{
			knit Loops;
		}
	}
}

with Carrier as c1:{
	print f"Knit with {Carrier}";
	cast_ons.alt_tuck_cast_on(width);
	knit_stripe();
}

with Carrier as 2:{
	print f"Knit with {Carrier}";
	knit_stripe();
}

with Carrier as [1,2]:{
	print f"Plate with {Carrier}";
	knit_stripe();
}

with Carrier as [c2, c1]:{
	print f"Plate with {Carrier}";
	knit_stripe();
}