import cast_ons;

with Carrier as white:{
	cast_ons.all_needle_cast_on(pattern_width);
	releasehook;
}
width_split = int(pattern_width/2);
for _ in range(pattern_height):{
	with Carrier as white:{
		in reverse direction:{
			knit Front_Loops[0:width_split];
			knit Back_Loops[width_split:];
		}
	}
	with Carrier as black:{
		in current direction:{
			Knit Back_Loops[0:width_split];
			knit Front_Loops[width_split:];
		}
		releasehook;
	}
}
