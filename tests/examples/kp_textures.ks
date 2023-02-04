//methods that create sample swatches in common knit purl textures


import cast_ons;

def stst(width=20, height=20):{
	cast_ons.alt_tuck_cast_on(width);
	for r in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
	}
}

def garter(width=20, height=20):{
	cast_ons.alt_tuck_cast_on(width);
	for r in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
		xfer Loops across;
	}
}

def rib(knits=2, purls=2, width=20, height=20):{
	cast_ons.alt_tuck_cast_on(width);
	//collect purl xfers
	purl_needles = [];
	for i in range(0, purls):{
		purl_needles.extend([n for n in Front_Needles[knits+i:width:knits+purls]]);
	}
	xfer purl_needles across to Back bed;
	//knit pattern for each row
	for r in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
	}
}

def seed(knits=1, purls=1, swap=1, width=20, height=20):{
	cast_ons.alt_tuck_cast_on(width);
	//collect purl xfers
	purl_needles = [];
	for i in range(0, purls):{
		purl_needles.extend([n for n in Front_Needles[knits+i:width:knits+purls]]);
	}
	xfer purl_needles across to Back bed;
	//knit pattern for each row
	for r in range(1, height+1):{
		in reverse direction:{
			knit Loops;
		}
		//swap pattern
		if r%swap == 0:{
			xfer Loops across;
		}
	}
}

def jersey_knit(width=20, height=20):{
	cast_ons.all_needle_cast_on(width);

	for r in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
	}
}

def stst_tube(width=20, height=20):{
	cast_ons.alt_tuck_cast_on(width, is_front=True);
	cast_ons.alt_tuck_cast_on(width, is_front=False);

	for r in range(0, height):{
		in reverse direction:{
			knit Front_Loops;
		}
		in reverse direction:{
			knit Back_Loops;
		}
	}
}

with Carrier as 1:{
	seed();
}
