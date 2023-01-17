import cast_ons;
width = 24;
height = 20;
max_gauge = 3;


def knit_front(pass_dir):{
	in pass_dir direction:{
		knit Front_Loops;
	}
}

with Carrier as 1:{
	with Gauge as 1:{
		cast_ons.alt_tuck_cast_on(width);
	}
}

//increase gauges after many rows of stst at that gauge. Knit multiple sheets for each gauge
for g in range(1, max_gauge+1):{
	with Gauge as g:{
		print f"Gauge -> {g}";
		for i in range(0, height):{
			print f"row {i}";
			next_dir = reverse;
			for s in range(0, g):{
				print f"Sheet -> {s} of {g}";
				with Sheet as s, Carrier as s+1:{
					knit_front(next_dir);
				}
			}
		}
	}
}

