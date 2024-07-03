import cast_ons;
import needles;
start_needle = 40;
def seed_section(height=10):{
	releasehook; // Should be a no-op
	xfer Back_Loops across to Front bed;
	assert len(Last_Pass) == 0;
	xfer Front_Loops[1::2] across to Back Bed;
	for _ in range(0, height-1):{
		in reverse direction:{
			knit Loops;
		}
		xfer Last_Pass across;
	}
	in reverse direction:{
		knit Loops;
	}
}

def lace(height=10):{
	for _ in range(0, height):{
		rightward_loops = needles.direction_sorted_needles(Loops);
		xfer rightward_loops[0::2], rightward_loops[-1] across to Front bed;
		in reverse direction:{
			knit Loops;
		}
		xfer rightward_loops[1:-1:4] across to Back bed;
		left_decs = Last_Pass.values();
		xfer rightward_loops[3:-1:4] across to Back bed;
		right_decs = Last_Pass.values();
		yo_spots = [];
		xfer right_decs 1 to Right to Front bed;
		yo_spots.extend(Last_Pass.keys());
		left_rack = 1;
		xfer left_decs left_rack to Left to Front Bed;
		yo_spots.extend(Last_Pass.keys());
		yo_spots = [n.opposite() for n in yo_spots];
		in reverse direction:{
			knit Loops;
			tuck yo_spots;
		}
	}
}

def split_sheets(front_carrier, back_carrier, height=10):{
	with Carrier as front_carrier:{
		in Leftward direction:{
			split Front_Loops;
		}
	}
	with Carrier as back_carrier:{
		in current direction:{
			knit Back_Loops;
		}
	}
	for _ in range(0, height):{
		with Carrier as front_carrier:{
			in reverse direction:{
				knit Front_Loops;
			}
		}
		with Carrier as back_carrier:{
			in current direction:{
				knit Back_Loops;
			}
		}
		releasehook;
	}
	cut back_carrier;
	xfer Back_Loops across to Front bed;
	with Carrier as front_carrier:{
		in reverse direction:{
			knit Front_Loops;
		}
	}
}

def third_gauge(height):{
	with Gauge as 3:{
		with Sheet as s2:{
			xfer Loops across to Back Bed;
			print f"S2 after Xfer {Loops}";
		}
		print f"S2 to back: {Last_Pass}";
		with Sheet as s1:{
			xfer Loops[1::2] across to Back bed;
			print f"S1 after Xfer {Loops}";
		}
		print f"S1 to back: {Last_Pass}";
		with Sheet as s0:{
			in reverse direction:{
				knit Loops;
			}
		}
//		for _ in range(0, height):{
//			with Sheet as s0:{
//				in reverse direction:{
//					knit Loops;
//				}
//			}
//			with Sheet as s1:{
//				in reverse direction:{
//					knit Loops;
//				}
//			}
//			with Sheet as s2:{
//				in reverse direction:{
//					knit Loops;
//				}
//			}
//			with Sheet as s0:{
//				in reverse direction:{
//					knit Loops;
//				}
//			}
//			with Sheet as s1:{
//				in reverse direction:{
//					knit Loops;
//				}
//			}
//			with Sheet as s2:{
//				in reverse direction:{
//					knit Loops;
//				}
//			}
//		}
	}
}

def split_slider_tube(left_carrier, right_carrier, height, courses_per_shift=4, split_needle=None):{
	if split_needle is None:{
		split_needle = int(width/2);
	}
	left_front = [];
	right_front = [];
	left_back = [];
	right_back = [];
	with Carrier as left_carrier:{
		in Leftward direction:{
			split Front_Loops;
		}
		left_front = Front_Loops[:split_needle];
		in Rightward direction:{
			knit Back_Loops[:split_needle];
		}
		left_back = Last_Pass;
		in Leftward direction:{
			miss left_front[0]-1;
		}
	}
	with Carrier as right_carrier:{
		in Leftward direction:{
			knit Back_Loops[split_needle::1];
		}
		right_back = Last_Pass;
		in Rightward direction:{
			knit Front_Loops[split_needle::1];
		}
		right_front = Last_Pass;
		in Rightward direction:{
			miss right_back[0] + 1;
		}
		releasehook;
	}
	current_height = 1;
	while current_height < (height-1):{
		for _ in range(0, courses_per_shift):{
			with Carrier as left_carrier:{
				in Leftward direction:{
					knit left_front;
				}
				in Rightward direction:{
					knit left_back;
				}
				in Leftward direction:{
					miss Front_Loops[0]-1;
				}
			}
			with Carrier as right_carrier:{
				in Leftward direction:{
					knit right_back;
				}
				in Rightward direction:{
					knit right_front;
				}
				in Rightward direction:{
					miss Front_Loops[-1] + 1;
				}
			}
		}
		xfer left_front across to Back bed sliders;
		left_front = Last_Pass.values();
		xfer right_front across to Back bed sliders;
		xfer left_front 1 to Left to Front bed;
		left_front = Last_Pass.values();
		xfer Back_Slider_Loops 1 to Right to Front bed;
		right_front = Last_Pass.values();
		xfer left_back across to Front bed sliders;
		left_back = Last_Pass.values();
		xfer right_back across to Front bed sliders;
		xfer left_back 1 to Leftward to Back bed;
		left_back = Last_Pass.values();
		xfer Slider_Loops 1 to Rightward to Back bed;
		right_back = Last_Pass.values();
		current_height = current_height+courses_per_shift;
	}
	with Carrier as left_carrier:{
		in Leftward direction:{
			knit left_front;
		}
		in Rightward direction:{
			knit left_back;
		}
	}
	with Carrier as right_carrier:{
		in Leftward direction:{
			knit right_back;
		}
		in Rightward direction:{
			knit right_front;
		}
	}
}

with Carrier as c:{
	cast_ons.alt_tuck_cast_on(width, first_needle=start_needle, is_front=True, tuck_lines=2, knit_lines=2);
	print "Imports from cast_on succeeded";
	print "Accessing Front and Back Needles Succeeded";
	print "Knitting and Tucking in a declared direction Succeeded";
	print "Releasing an inhooked carrier succeeded";
	print "Knitting in the reverse direction succeeded";
	print "Using Last_Pass from knit and tuck passes succeeded";
	print "Loading Carrier succeeded";
	print "Loading variables from Python input succeeded";
	seed_section();
	print "Used local function";
	print "Used front back across xfers. ";
	print "Included a No-op releasehook.";
	lace();
	print "Xfer racked 1 to left and right";
	print "Used dictionary Last_Pass from xfers";
	print "Combined multiple xfers in one carriage pass even when separating them out semantically.";
	print "Provided multiple needle lists to xfer statement";
	print "Knit and tuck in same carriage pass";
	split_sheets(c, cb);
	print "Used splits";
	print "Introduced new carrier";
	print "Cut a carrier";
	print "Used reverse and current directions";
	split_slider_tube(c, cb, height =20);
	print "Used slider needles in xfers";
	print "Used slider loop references";
	print "Used front and back misses";
	print "Used needle arithmetic";
}