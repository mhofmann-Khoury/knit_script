import cast_ons;
import needles;

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
		for _ in range(0, height):{
			with Sheet as s0:{
				in reverse direction:{
					knit Loops;
				}
			}
			with Sheet as s1:{
				in reverse direction:{
					knit Loops;
				}
			}
			with Sheet as s2:{
				in reverse direction:{
					knit Loops;
				}
			}
			with Sheet as s0:{
				in reverse direction:{
					knit Loops;
				}
			}
			with Sheet as s1:{
				in reverse direction:{
					knit Loops;
				}
			}
			with Sheet as s2:{
				in reverse direction:{
					knit Loops;
				}
			}
		}
	}
	with Sheet as s0, Gauge as 1:{
		xfer Back_Loops across to Front bed;
	}
}

def three_layers(block_height, carrier_0, carrier_1, carrier_2):{
	with Gauge as 3:{
		with Sheet as s2:{
			xfer Front_Loops across to Back bed;
		}
		half_width = int(len(s0.Front_Loops)/2);
		first_half = s0.Front_Loops[0:half_width];
		print f"First Half of s0: {first_half}";
		push first_half to Back;
		for _ in range(0, block_height):{
			with Sheet as s0, Carrier as carrier_0:{
				in Leftward direction:{
					knit Loops;
				}
				in Rightward direction:{
					knit Loops;
				}
				releasehook;
			}
			with Sheet as s1, Carrier as carrier_1:{
				in Leftward direction:{
					knit Loops;
				}
				in Rightward direction:{
					knit Loops;
				}
				releasehook;
			}
			with Sheet as s2, Carrier as carrier_2:{
				in Leftward direction:{
					knit Loops;
				}
				in Rightward direction:{
					knit Loops;
				}
				releasehook;
			}
		}
		swap s0.Needles with sheet 3;
		for _ in range(0, block_height):{
			with Sheet as s0, Carrier as carrier_0:{
				in Leftward direction:{
					knit Loops;
				}
				in Rightward direction:{
					knit Loops;
				}
				releasehook;
			}
			with Sheet as s1, Carrier as carrier_1:{
				in Leftward direction:{
					knit Loops;
				}
				in Rightward direction:{
					knit Loops;
				}
				releasehook;
			}
			with Sheet as s2, Carrier as carrier_2:{
				in Leftward direction:{
					knit Loops;
				}
				in Rightward direction:{
					knit Loops;
				}
				releasehook;
			}
		}
	}
}


with Carrier as c:{
	cast_ons.alt_tuck_cast_on(width, is_front=True, tuck_lines=1, knit_lines=1);
	third_gauge(10);
	three_layers(4, 1, 2, 3);

}