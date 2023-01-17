import cast_ons;
width = 4;
stripe_height = 2;

def knit_stripe():{
	for r in range(0, stripe_height):{
		in reverse direction:{
			knit Loops;
		}
	}
}

def knit_with_c2():{
	with Carrier as c2:{
		print f"Switching to carrier {Carrier}";
		knit_stripe();
	}
	print f"Switching back to carrier {Carrier}";
}

with Carrier as 1:{
	print f"Knitting with {Carrier}";
	cast_ons.alt_tuck_cast_on(width);
	knit_stripe();
	knit_with_c2();
	knit_stripe();
}