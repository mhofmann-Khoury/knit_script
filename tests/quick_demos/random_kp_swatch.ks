import cast_ons;
import bind_offs;
import needles;
import random;

with Carrier as chosen_carrier, width as 60, height as 60, border as 8:{
	total_width = width + 2*border;
	cast_ons.alt_tuck_cast_on(total_width, knit_lines=1);

	xfer Front_Loops[1:total_width:2] across to back bed;
	in reverse direction:{
		knit Loops;
	}
	for _ in range(1, border):{
		xfer Loops across;
		in reverse direction:{
			knit Loops;
		}
	}

	for r in range(0, height):{
		sorted_loops = needles.direction_sorted_needles(Loops, direction=Rightward);
		l_border = sorted_loops[:border];
		r_border = sorted_loops[-1*border::1];
		xfers = [];
		xfers.extend(l_border);
		xfers.extend(r_border);
		swatch_area = sorted_loops[border:-1*border];
		for active_needle in swatch_area:{
			if random.choice([True, False]):{
				xfers.append(active_needle);
			}
		}
		xfer xfers across;
		in reverse direction: {
			knit Loops;
		}
	}

	sorted_loops = needles.direction_sorted_needles(Loops, direction=Rightward);
	l_border = sorted_loops[:border];
	r_border = sorted_loops[-1*border::1];
	xfers = [];
	xfers.extend(l_border);
	xfers.extend(r_border);
	swatch_area = sorted_loops[border:-1*border];
	for i, active_needle in enumerate(swatch_area):{
		if (i % 2 == 1 and active_needle.is_front) or (i % 2 == 0 and active_needle.is_back):{
			xfers.append(active_needle);
		}
	}
	xfer xfers across;
	in reverse direction:{
		knit Loops;
	}
	for _ in range(1, border):{
		xfer Loops across;
		in reverse direction:{
			knit Loops;
		}
	}
	xfer Back_Loops across to back bed;
	bind_offs.chain_bind_off(Loops, reverse);


}


