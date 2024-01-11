import needles;

def alt_tuck_cast_on(w, is_front=True, first_needle=0, co_dir=Leftward, tuck_lines=2, knit_lines=2, release=True):{
	side = Back_Needles;
	if is_front:{
		side = Front_Needles;
	}
	first_pass = side[first_needle: first_needle + w: 2];
	second_pass = side[first_needle + 1: first_needle + w: 2];
	if w%2 == 0:{
		left_shifted_pass = side[first_needle: first_needle+w: 2];
		right_shifted_pass = side[first_needle + 1: first_needle+w: 2];
		if co_dir == Rightward:{ // needs to end on left shifted loop
			first_pass = left_shifted_pass;
			second_pass = right_shifted_pass;
		} else:{ // needs to end on right shifted loop
			first_pass = right_shifted_pass;
			second_pass = left_shifted_pass;
		}
	}
	print f"Cast on {w} loops from {first_needle} to {first_needle+w}";
	co_loops = [];
	for _ in range(0, tuck_lines):{
		in co_dir direction:{
			tuck first_pass;
		}
		co_loops = Last_Pass;
		in reverse direction:{
			tuck second_pass;
		}
		co_loops.extend(Last_Pass);
	}
	if release:{
		releasehook;
	}
	for k in range(0, knit_lines):{
		in reverse direction:{
			knit co_loops;
		}
		in reverse direction:{
			knit co_loops;
		}
	}
}

def alt_tuck_needle_set(co_needles, co_dir=Leftward):{
	co_needles= needles.direction_sorted_needles(co_needles, co_dir);
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

def all_needle_cast_on(w, first_needle=0, tuck_lines=2, knit_lines=1, cross=True):{
	fronts_tucks_1 = Front_Needles[first_needle: first_needle+w:2];
	backs_tucks_1 = Back_Needles[first_needle+1: first_needle+w:2];

	fronts_tucks_2 = Front_Needles[first_needle+1: first_needle+w:2];
	backs_tucks_2 = Back_Needles[first_needle: first_needle+w:2];
	print f"All needle cast on {w} needles (front and back) from {first_needle}";
	for _ in range(0, tuck_lines):{
		if fronts_tucks_1[-1] < backs_tucks_1[-1]:{ // tucks would start on back, unstable
			in Leftward direction:{
				tuck fronts_tucks_2;
				tuck backs_tucks_2;
			}
			in reverse direction:{
				tuck fronts_tucks_1;
				tuck backs_tucks_1;
			}
		} else: {
			in Leftward direction:{
				tuck fronts_tucks_1;
				tuck backs_tucks_1;
			}
			in reverse direction:{
				tuck fronts_tucks_2;
				tuck backs_tucks_2;
			}
		}
	}
	if cross:{
		for _ in range(0, knit_lines):{
			in reverse direction:{
				knit [l.opposite() for l in Last_Pass];
			}
			in reverse direction:{
				knit [l.opposite() for l in Last_Pass];
			}
		}
	} else:{
		for _ in range(0, knit_lines):{
			in reverse direction:{
				knit Front_Loops;
			}
			in reverse direction:{
				knit Back_Loops;
			}
		}
	}
}

def all_needle_wasted_cast_on(w, waste_yarn, thread_yarn, waste_size=10, first_needle=0):{
	//cast_on with waste_yarn
	with Carrier as waste_yarn:{
		in Leftward direction:{
			tuck Front_Needles[first_needle + w - 2];
		}
		in Leftward direction:{
			tuck Back_Needles[first_needle+1:first_needle+w:2];
			tuck Front_Needles[first_needle:first_needle+w:2];
		}
		for _ in range(0, 2):{
			in reverse direction:{
				knit Back_Loops;
			}
		}
		in reverse direction:{
			knit Front_Loops;
			tuck Back_Loops;
		}
		in reverse direction:{
			knit Back_Loops;
		}
		in reverse direction:{
			knit Front_Loops;
		}
		for _ in range(0, waste_size):{
			in reverse direction:{
				knit Front_Needles[first_needle: first_needle+w];
			}
			in reverse direction:{
				knit Back_Needles[first_needle: first_needle+w];
			}
		}
		cut waste_yarn;
	}
	with Carrier as thread_yarn:{
		in Leftward direction:{
			tuck Front_Needles[first_needle+w: first_needle + w +6];
			knit Front_Loops;
		}
		in reverse direction:{
			knit Back_Loops;
			tuck Back_Needles[first_needle+w: first_needle + w +6];
		}
		drop Front_Loops[-6::1];
		drop Back_Loops[-6::1];
		cut thread_yarn;
	}

}


//	in Leftward direction:{
//		tuck Front_Needles[first_needle:first_needle+w:2];
//		tuck Back_Needles[first_needle+1:first_needle+w:2];
//	}
//	in reverse direction:{
//		tuck Front_Needles[first_needle+1:first_needle+w:2];
//		tuck Back_Needles[first_needle:first_needle+w:2];
//	}
