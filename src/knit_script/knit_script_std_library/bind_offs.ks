import needles;



def chain_bind_off(loops_to_bo, bo_direction, extra_knits=1, hold = True):{
    loops_bo_direction = needles.direction_sorted_needles(loops_to_bo, bo_direction);
    next_loop = None;
    hold_loops = [];
    for i, bo_loop in enumerate(loops_bo_direction[:-1]):{
        next_loop = loops_bo_direction[i+1];
//        print f"bind {bo_loop} onto {next_loop}";
        loop_pos = bo_loop;
        while next_loop.position != loop_pos.position:{
            xfer loop_pos 1 to bo_direction;
            loop_pos = Last_Pass[loop_pos]; // update bo_loop position
//            print f"bo moved to {loop_pos}";
        }
        if loop_pos.is_front != next_loop.is_front :{
            if hold:{
                in bo_direction.opposite() direction:{ // transfers bo_loop across onto next loop and leaves it held on machine for held bind off
                    split loop_pos;
                }
                hold_loops.extend(Last_Pass.keys());
            } else:{
                xfer loop_pos across;
            }

        }
        in bo_direction direction:{
            knit next_loop;
        }
    }
    if next_loop is not None:{
        if len(hold_loops) == 0:{
            hold_loops = [next_loop];
        }
        print f"Spare knitting on {hold_loops}";
        in bo_direction.opposite() direction:{
            knit hold_loops;
        }
        for _ in range(1, extra_knits):{
            in reverse direction:{
                knit hold_loops;
            }
        }
    }
}