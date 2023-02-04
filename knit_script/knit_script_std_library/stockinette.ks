

def stst(rows, stst_loops=None, start_dir=None):{
	if stst_loops is None:{
	    stst_loops = Front_Loops;
	}
	if start_dir is None:{
		start_dir = reverse;
	}
	in start_dir direction:{
		knit stst_loops;
	}
	for r in range(1, rows):{
		in reverse direction:{
			knit stst_loops;
		}
	}
}

def reverse_stst(rows, start_dir=None):{
	print f"Reverse Stockinette for {rows} rows";
	if start_dir is None:{
		start_dir = reverse;
	}
	in start_dir direction:{
		knit Back_Loops;
	}
	for r in range(1, rows):{
		in reverse direction:{
			knit Back_Loops;
		}
	}
}

def all_needle_stst(rows, start_dir=None):{
	print f"Reverse Stockinette for {rows} rows";
	if start_dir is None:{
		start_dir = reverse;
	}
	in start_dir direction:{
		knit Loops;
	}
	for r in range(1, rows):{
		in reverse direction:{
			knit Loops;
		}
	}
}