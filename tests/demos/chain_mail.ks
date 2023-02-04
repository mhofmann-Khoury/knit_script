import cast_ons;
import stockinette;
import bind_offs;
import needles;

front_link_count = 2;
back_link_count = 1;

link_size = 2;
assert link_size%2 == 0;
buffer = 2;
assert buffer%2 == 0;
links = 4;

center_width = (2 * link_size) + (3 * buffer);
center_height = center_width;
outer_width = center_width + (2 * link_size);
outer_height = center_height + (2 * link_size);

back_link_offset = (link_size*2) + (buffer*2);

last_needle = front_link_count * outer_width + buffer * (front_link_count + back_link_count);

with Gauge as 2:{
	last_needle = needles.needle(True, last_needle * Gauge);
    front_sheet = s0;
    back_sheet = s1;

    front_link_carriers = [ [c, c+1] for c in range(1, front_link_count*2 +1, 2)];
    back_link_carriers = [ [c, c+1] for c in range(front_link_count*2+1, (front_link_count+back_link_count) * 2, 2)];

    front_link_needles = [];
    back_link_needles = [];
    with Sheet as front_sheet:{
        front_link_needles = [ [n for n in Front_Needles[l * (outer_width + buffer):
                                                        (l * (outer_width + buffer)) + outer_width]] for l in range(0, front_link_count)];
    }
    with Sheet as back_sheet:{
        back_link_needles = [ [n for n in Back_Needles[back_link_offset + (l * (outer_width + buffer)):
                                                        (l * (outer_width + buffer)) + outer_width + back_link_offset]] for l in range(0, back_link_count)];
    }

	def knit_front_bottom(link):{
		//make each bar separately
	    link_needles = front_link_needles[link];
	    link_carriers = front_link_carriers[link];
	    with Carrier as link_carriers:{
	        cast_ons.alt_tuck_needle_set(link_needles, co_dir=Leftward);
	        stockinette.stst(link_size, stst_loops=link_needles);
	    }
        with Carrier as link_carriers[0]:{//left carrier
            in Leftward direction:{ // knit right column
                knit link_needles[-2:];
            }
            bind_offs.chain_bind_off(link_needles[1:-2], Leftward);
            in Leftward direction:{
                knit link_needles[:2];
            }
        }
    }

    def knit_front_columns(link, rows):{
	    link_needles = front_link_needles[link];
		right_link_carrier = front_link_carriers[link][1];
		left_link_carrier = front_link_carriers[link][0];
        with Carrier as right_link_carrier:{
            stockinette.stst(rows, stst_loops=link_needles[-2:], start_dir=Leftward);
            in Rightward direction:{
                miss last_needle;
            }
        }
        with Carrier as left_link_carrier:{
            stockinette.stst(rows, stst_loops=link_needles[:2], start_dir=Leftward);
            cut carrier;
        }
    }

    def purl_back_bottom(link):{
       //make each bar separately
	    link_needles = back_link_needles[link];
	    link_carriers = back_link_carriers[link];
	    with Carrier as link_carriers:{
	        cast_ons.alt_tuck_needle_set(link_needles, co_dir=Leftward);
	        stockinette.stst(link_size, stst_loops=link_needles);
	    }
        with Carrier as link_carriers[0]:{//left carrier
            in Leftward direction:{ // knit right column
                knit link_needles[-2:];
            }
            bind_offs.chain_bind_off(link_needles[1:-2], Leftward);
            in Leftward direction:{
                knit link_needles[:2];
            }
        }
    }

    def purl_back_columns(link, rows):{
	    link_needles = back_link_needles[link];
		right_link_carrier = back_link_carriers[link][1];
		left_link_carrier =  back_link_carriers[link][0];
        with Carrier as right_link_carrier:{
            stockinette.stst(rows, stst_loops=link_needles[-2:], start_dir=Leftward);
            in Rightward direction:{
                miss last_needle;
            }
        }
        with Carrier as left_link_carrier:{
            stockinette.stst(rows, stst_loops=link_needles[:2], start_dir=Leftward);
            cut carrier;
        }
    }

    def knit_front_top(link):{
	    link_needles = front_link_needles[link];
	    link_carriers = front_link_carriers[link];
	    with Carrier as link_carriers[1]:{ // right carrier
	        stockinette.stst(link_size, stst_loops=link_needles);
	        bind_offs.chain_bind_off(link_needles, Leftward);
	        in Rightward direction:{
	            miss last_needle;
	        }
	    }
	    cut link_carriers[1];
    }

    def purl_back_top(link):{
	    link_needles =  back_link_needles[link];
	    link_carriers = back_link_carriers[link];
	    with Carrier as link_carriers[1]:{ // right carrier
	        stockinette.stst(link_size, stst_loops=link_needles);
	        bind_offs.chain_bind_off(link_needles, Leftward);
	        in Rightward direction:{
	            miss last_needle;
	        }
	    }
	    cut link_carriers[1];
    }
    front_link_height = 0;
    back_link_height = 0;
	while (front_link_height < links) and (back_link_height < links):{
		if front_link_height > 0:{
			with Sheet as front_sheet:{
		        for link in range(front_link_count-1, -1, -1):{ // working links from right to left
		            print f"row {front_link_height}: Bind off Front link {link}";
		            push Front_Needles to front; // bars are in front of
		            knit_front_top(link);
		        }
			}
		}
		if front_link_height < links:{
			with Sheet as front_sheet:{
		        for link in range(front_link_count-1, -1, -1):{ // working links from right to left
		            print f"row {front_link_height}: Cast On Front link {link}";
		            push Front_Needles to front; // bars are in front of
		            knit_front_bottom(link);
		            push Front_Needles to back; // columns are in back
		            knit_front_columns(link, center_height);
		        }
			}
			front_link_height = front_link_height + 1;
		}
		if back_link_height > 0:{
			with Sheet as back_sheet:{
	            for link in range(back_link_count-1, -1, -1):{
		            print f"row {back_link_height}: Bind off Back link {link}";
	                push Front_Needles to front; // bars are in front
	                purl_back_top(link);
	            }
			}
		}
		if back_link_height < links:{
			with Sheet as back_sheet:{
		        for link in range(back_link_count-1, -1, -1):{
		            print f"row {back_link_height}: Cast on Back link {link}";
		            push Front_Needles to front; // bars are in front
		            purl_back_bottom(link);
		            push Front_Needles to back; // columns are in back
		            purl_back_columns(link, center_height);
		        }
			}
			back_link_height = back_link_height + 1;
		}
	}


	with Sheet as front_sheet:{ // last bind off
        for link in range(front_link_count-1, -1, -1):{ // working links from right to left
            print f"row {front_link_height}: Bind off Front link {link}";
            push Front_Needles to front; // bars are in front of
            knit_front_top(link);
        }
	}
	with Sheet as back_sheet:{ // last bind off
        for link in range(back_link_count-1, -1, -1):{
            print f"row {back_link_height}: Bind off Back link {link}";
            push Front_Needles to front; // bars are in front
            purl_back_top(link);
        }
	}
}
