
def alt_tuck_cast_on(w, is_front=True):{
	print f"Cast on {w} loops";
	side = Back_Needles;
	if is_front:{
		side = Front_Needles;
	}
	in Leftward direction:{
		tuck [n for n in side[1:w:2]];
	}
	in reverse direction:{
		tuck [n for n in side[0:w:2]];
	}
}

def all_needle_cast_on(w):{
	print f"All needle cast on {w} needles (front and back)";
	in Leftward direction:{
		tuck Front_Needles[0:w:2];
		tuck Back_Needles[1:w:2];
	}
	in reverse direction:{
		tuck Front_Needles[1:w:2];
		tuck Back_Needles[0:w:2];
	}
}