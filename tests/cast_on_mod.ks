import needles;

def cast_on(co_needles, start_dir=Leftward, knit_rows=2):{
	p1 = [];
	p2 = [];
	racking_dir = -0.75;
	second_rack = 0.25;
	if start_dir is Rightward:{
		racking_dir = 0.25;
		second_rack = -0.75;
	}
	co_needles = needles.direction_sorted_needles(co_needles, start_dir, racking=0.25);
	first_knit = co_needles[0];
	p1.append(co_needles[0]);
	skip = True;
	for i in range(1, len(co_needles)):{
		last_p1 = p1[-1];
		n = co_needles[i];
		if last_p1.position == n.position:{
			skip=True;
		} elif not skip:{
			skip = True;
			p1.append(n);
		} elif last_p1.is_front == n.is_front:{
			skip = False;
		} else:{
			p1.append(n);
			skip = True;
		}
	}
	for n in co_needles:{
		if not (n in p1):{
			p2.append(n);
		}
	}

	if first_knit in p2:{
		in start_dir direction:{
			tuck p2;
		}
		in reverse direction:{
			tuck p1;
		}
	}else:{
		in start_dir direction:{
			tuck p1;
		}
		in reverse direction:{
			tuck p2;
		}
	}

	for r in range(0, knit_rows):{
		in reverse direction:{
			knit Loops;
		}
	}

}
