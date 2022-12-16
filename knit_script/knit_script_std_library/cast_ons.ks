
def alt_tuck_cast_on(w):{
	print f"Cast on {w} loops";
	in Leftward direction:{
		tuck [n for n in Front_Needles[1:w:2]];
	}
	in reverse direction:{
		tuck [n for n in Front_Needles[0:w:2]];
	}
}

def all_needle_cast_on(w):{
	in Leftward direction:{
		tuck Front_Needles[0:w:2];
		tuck Back_Needles[1:w:2];
	}
	in reverse direction:{
		tuck Front_Needles[1:w:2];
		tuck Back_Needles[0:w:2];
	}
}