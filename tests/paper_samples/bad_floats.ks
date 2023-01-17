// Make a single sheet sample that demonstrates how floats fall between beds
import stockinette;
stripe_count = 9;
stripe_width = 3;
width = stripe_count * stripe_width;
height = 20;

def cast_on_stst(w, h=4):{
	print f"Cast on {w} loops";
	in Leftward direction:{
		tuck Front_Needles[1:w:2];
	}
	in reverse direction:{
		tuck Front_Needles[0:w:2];
	}
	stockinette.stst(h);
}

def add_splits(stripes = [0, 4, 8]):{
	split_dir = reverse;
	backs = [];
	fronts = [];
	stripe_range = None;
	if split_dir is Decreasing:{
		stripe_range = range(stripe_count-1, -1, -1);
	} else: {
		stripe_range = range(0, stripe_count);
	}
	for stripe in stripe_range:{
		start = stripe * stripe_width;
		stripe_needles = Front_Needles[start:start+stripe_width];
		back_stripe_needles = Back_Needles[start:start+stripe_width];
		if stripe in stripes:{
			in split_dir direction:{
				split stripe_needles;
			}
		} else:{
			in split_dir direction:{
				knit stripe_needles;
			}
		}

	}
	in reverse direction:{
		knit Front_Loops;
		knit Back_Loops;
	}
}

def collect_needles(f_stripes = [0,4,6], b_stripes = [2,4,8]):{
	needles = [];
	for s in f_stripes:{
		start = s * stripe_width;
		needles.extend(Front_Needles[start: start+stripe_width]);
	}
	for s in b_stripes:{
		start = s * stripe_width;
		needles.extend(Back_Needles[start: start+stripe_width]);
	}
	return needles;
}



with Carrier as 1:{
	cast_on_stst(width);
	add_splits();
}

first_needles = collect_needles();
second_needles = collect_needles([5,7,8], [0,1,3]);
print first_needles;
print second_needles;

for r in range(0, height):{
	next_direction = reverse;
	with Carrier as 1:{
		in next_direction direction:{
			knit first_needles;
		}
	}
	with Carrier as 2:{
		in next_direction direction:{
			knit second_needles;
		}
	}
}





