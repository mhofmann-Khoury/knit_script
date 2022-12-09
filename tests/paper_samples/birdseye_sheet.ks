
width = 60;
height = 60;
color_1 = 1;

def all_needle_cast_on():{
	in reverse direction:{
		tuck [f for f in Front_Needles[0:width:2]];
		tuck [b for b in Back_Needles[1:width:2]];
	}
	in reverse direction:{
		tuck [f for f in Front_Needles[1:width:2]];
		tuck [b for b in Back_Needles[0:width:2]];
	}
}

with Carrier as 1:{
	all_needle_cast_on();
}

for r in range(0, height):{
	with Carrier as 2:{
		in reverse direction:{
			knit [b for b in Back_Loops[0: width: 2]];
			knit [f for f in Front_Loops[0:color_1:2]];
		}
	}
	with Carrier as 3:{
		in reverse direction:{
			knit [b for b in Back_Loops[1: width: 2]];
			knit [f for f in Front_Loops[1:color_1+1:2]];
		}
	}
	with Carrier as 1:{
		in reverse direction:{
			knit [b for b in Back_Loops[0:width:2]];
			knit [f for f in Front_Loops[color_1+1:width]];
		}
	}
	color_1 = (color_1 + 1) % width;
}