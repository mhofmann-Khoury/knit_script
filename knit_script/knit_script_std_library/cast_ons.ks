
def alt_tuck_cast_on(w, is_front=True, first_needle=0, co_dir=Leftward):{
	print f"Cast on {w} loops";
	side = Back_Needles;
	if is_front:{
		side = Front_Needles;
	}
	first_pass_start = first_needle+1;
	second_pass_start = first_needle;
	if co_dir == Rightward:{
	    first_pass_start = first_needle;
	    second_pass_start = first_needle+1;
	}
	in co_dir direction:{
		tuck side[first_pass_start:first_needle+w:2];
	}
	in reverse direction:{
		tuck side[second_pass_start:first_needle+w:2];
	}
}

def alt_tuck_needle_set(co_needles, co_dir=Leftward):{
    if co_dir == Leftward:{
        in co_dir direction:{
            tuck co_needles[1::2];
        }
        in reverse direction:{
            tuck co_needles[0::2];
        }
    } else:{
        in co_dir direction:{
            tuck co_needles[0::2];
        }
        in reverse direction:{
            tuck co_needles[1::2];
        }
    }
}

def all_needle_cast_on(w, first_needle=0):{
	print f"All needle cast on {w} needles (front and back)";
	in Leftward direction:{
		tuck Front_Needles[first_needle:first_needle+w:2];
		tuck Back_Needles[first_needle+1:first_needle+w:2];
	}
	in reverse direction:{
		tuck Front_Needles[first_needle+1:first_needle+w:2];
		tuck Back_Needles[first_needle:first_needle+w:2];
	}
}