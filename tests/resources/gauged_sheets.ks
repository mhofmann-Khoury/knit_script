import cast_ons;

with Carrier as c:{
	with Gauge as 2:{
		with Sheet as 0:{
			cast_ons.alt_tuck_cast_on(pattern_width);
		}
		with Sheet as 1:{
			cast_ons.alt_tuck_cast_on(pattern_width, is_front=False);
		}
		for _ in range(4, pattern_height):{
			with Sheet as 0:{
				in reverse direction:{
					knit Loops;
				}
			}
			with Sheet as 1:{
				in reverse direction:{
					knit Loops;
				}
			}
		}
	}
}
