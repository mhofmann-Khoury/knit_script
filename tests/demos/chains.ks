import cast_ons;
import bind_offs;
import needles;

left_carrier = c1;
right_carrier = c2;
link_size = 2;
buffer = 2;

center_width = (2 * link_size) + (3 * buffer);
center_height = center_width;
outer_width = center_width + (2 * link_size);
outer_height = center_height + (2 * link_size);

with Carrier as left_carrier:{
    //bottom bar of link
    cast_ons.alt_tuck_cast_on(outer_width);
    push Front_Needles to front; // push first bar to front layer
    for r in range(0, link_size):{
        in reverse direction:{
            knit Loops;
        }
    }

    needles_in_bo_direction = needles.direction_sorted_needles(Loops, reverse);
    in reverse direction:{
        knit needles_in_bo_direction[0:2];
    }
    bind_offs.chain_bind_off(needles_in_bo_direction[2:-1], current);
    in current direction:{
        knit needles_in_bo_direction[-1];
    }
}
//middle columns
left_loops = Loops[:2];
right_loops = Loops[-2:];
for r in range(0, center_height-1):{ // knit up to top cast on
    if reverse == Leftward:{
        with Carrier as right_carrier:{
            in reverse direction:{
                knit right_loops;
            }
        }
        with Carrier as left_carrier:{
            in current direction:{
                knit left_loops;
            }
        }
    } else:{
        with Carrier as left_carrier:{
            in reverse direction:{
                knit left_loops;
            }
        }
        with Carrier as right_carrier:{
            in current direction:{
                knit right_loops;
            }
        }
    }
}
//top of link
co_needle = left_loops[-1]+1;
first_loops = right_loops;
second_loops = left_loops;
top_carrier = right_carrier;
cut_carrier = left_carrier;
if reverse == Rightward:{
    first_loops = left_loops;
    second_loops = right_loops;
    top_carrier = left_carrier;
    cut_carrier = right_carrier;
}
cut cut_carrier;
with Carrier as top_carrier:{
    in reverse direction:{
        knit first_loops;
    }
    cast_ons.alt_tuck_cast_on(center_width, first_needle=co_needle, co_dir=current);
    in reverse direction:{
        knit Loops[2:-2];
        knit second_loops;
    }
    for r in range(0, link_size):{
        in reverse direction:{
            knit Loops;
        }
    }
}

