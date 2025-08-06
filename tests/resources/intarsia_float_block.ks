import cast_ons;

pattern_width = border + block_width + border;
with Carrier as white:{
	cast_ons.alt_tuck_cast_on(pattern_width);
	for _ in range(border):{
		in reverse direction:{
			knit Loops;
		}
	}
}
left_border = Front_Loops[0:border];
right_border = Front_Loops[-1*border:];
block = Front_Loops[border:-1*border];
for i in range(block_height):{
	with Carrier as white:{
		in reverse direction:{
			knit left_border;
			knit right_border;
		}
	}
	with Carrier as black:{
		in current direction:{
			knit block;
		}
	}
	if i > 0:{ releasehook;}
}
cut black;
with Carrier as white:{
	for _ in range(border):{
		in reverse direction:{
			knit Loops;
		}
	}
}
