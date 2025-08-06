import cast_ons;

pattern_width = 4 * stripe_size;

with Carrier as white:{
	cast_ons.alt_tuck_cast_on(pattern_width);
}

with Carrier as black:{
	in Leftward direction:{
		knit Loops;
	}
	in reverse direction:{
		knit Loops;
	}
	releasehook;
}

for _ in range(0, stripes, 2):{
	with Carrier as [white, black]:{
		for __ in range(stripe_size):{
			in reverse direction:{
				knit Loops;
			}
		}
	}
	with Carrier as [black, white]:{
		for __ in range(stripe_size):{
			in reverse direction:{
				knit Loops;
			}
		}
	}
}

for _ in range(0, pattern_height, 2):{
	with Carrier as [black, white]:{
		in Leftward direction:{
			knit Loops[-1*stripe_size:];
		}
	}
	with Carrier as [white, black]:{
		in Leftward direction:{
			knit Loops[2*stripe_size:-1*stripe_size];
		}
	}
	with Carrier as [black, white]:{
		in Leftward direction:{
			knit Loops[stripe_size:stripe_size*2];
		}
	}
	with Carrier as [white, black]:{
		in Leftward direction:{
			knit Loops[0:stripe_size];
		}
	}
	with Carrier as [white, black]:{
		in Rightward direction:{
			knit Loops[0:stripe_size];
		}
	}
	with Carrier as [black, white]:{
		in Rightward direction:{
			knit Loops[stripe_size:stripe_size*2];
		}
	}
	with Carrier as [white, black]:{
		in Rightward direction:{
			knit Loops[2*stripe_size:-1*stripe_size];
		}
	}
	with Carrier as [black, white]:{
		in Rightward direction:{
			knit Loops[-1*stripe_size:];
		}
	}
}
