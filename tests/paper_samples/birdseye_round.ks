width = 30;
stripe_width = 6;
stripe_1_start = 0;
stripe_2_start = (width * 2) - stripe_width;
height = 10;

def cast_on_front_back(front_sheet, back_sheet):{
	in Leftward direction:{
		tuck [f for f in front_sheet.Front_Needles[1:width:2]];
		tuck [b for b in back_sheet.Back_Needles[0:width:2]];
	}
	in reverse direction:{
		tuck [f for f in front_sheet.Front_Needles[0:width:2]];
		tuck [b for b in back_sheet.Back_Needles[1:width:2]];
	}
}


def map_tube_position(index, front_sheet, back_sheet):{
	if index < 0:{
		index = (width * 2) + index;
	}
	index = index % (width * 2);
	if index < width:{
		return front_sheet.needle(True, index);
	} else :{
		remainder = index % width;
		return back_sheet.needle(False, width - remainder - 1);
	}
}

with Gauge as 4:{
	front_0 = s0;
	back_0 = s2;
	front_1 = s1;
	back_1 = s3;
	with Sheet as front_0:{
		push Front_Needles to layer 0;
	}
	with Sheet as back_0:{
		push Front_Needles to layer 0;
	}
	with Sheet as front_1:{
		push Front_Needles to layer 1;
	}
	with Sheet as back_1:{
		push Front_Needles to layer 1;
	}
	with Carrier as 1:{
		with Sheet as front_0:{
			cast_on_front_back(front_0, back_0);
		}
		with Sheet as front_1:{
			cast_on_front_back(front_1, back_1);
		}
	}
	last_index = (width*2)-1;
	for i in range(0, height):{
		stripe_0 = [map_tube_position(j, front_0, back_1) for j in range(i, i+stripe_width)];
		print(f"{i}: stripe 0: {stripe_0}");
		stripe_1 = [map_tube_position(j, front_0, back_1) for j in range(last_index-i, last_index-i-stripe_width, -1)];
		stripe_1 = [n for n in stripe_1 if not n in stripe_0];//stripe 0 crosses over stripe 1
		with Sheet as front_0:{
			front_dir = reverse;
			with Carrier as 1: {
				// knit front of tube in base color
				in front_dir direction:{
					knit [f for f in front_0.Loops if (not f in stripe_0) and (not f in stripe_1)];
					knit [b for b in back_0.Loops[i%2::2]];
				}
			}
			with Carrier as 2:{
				//knit front of tube in stripe 0 color
				in front_dir direction:{
					knit [f for f in front_0.Loops if f in stripe_0];
					knit [b for b in back_0.Loops[(i+1)%2::2]];
				}
			}
			with Carrier as 3:{
				//knit front of tube in stripe 1 color
				in front_dir direction:{
					knit [f for f in front_0.Loops if f in stripe_1];
					knit [b for b in back_0.Loops[i%2::2]];
				}
			}
		}
		print(f"{i}: stripe 1: {stripe_1}");
		with Sheet as back_1:{
			back_dir = reverse;
			with Carrier as 1: {
				// knit back of tube in base color
				in back_dir direction:{
					knit [f for f in back_1.Loops if (not f in stripe_0) and (not f in stripe_1)];
					knit [b for b in front_1.Loops[(i+1)%2::2]];
				}
			}
			with Carrier as 2:{
				//knit front of tube in stripe 0 color
				in back_dir direction:{
					knit [f for f in back_1.Loops if f in stripe_0];
					knit [b for b in front_1.Loops[(i)%2::2]];
				}
			}
			with Carrier as 3:{
				//knit front of tube in stripe 1 color
				in back_dir direction:{
					knit [f for f in back_1.Loops if f in stripe_1];
					knit [b for b in front_1.Loops[(i+1)%2::2]];
				}
			}
		}
	}
}
