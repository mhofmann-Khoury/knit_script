import needles;



def chain_bind_off(loops_to_bo, bo_direction):{
    loops_bo_direction = needles.direction_sorted_needles(loops_to_bo, bo_direction);

    for i, bo_loop in enumerate(loops_bo_direction[:-1 ]):{
        next_loop = loops_bo_direction[i+1];
        xfer bo_loop 1 to bo_direction;
        if(bo_loop.is_front == next_loop.is_front):{
            xfer next_loop.opposite() across;
        }
        in bo_direction direction:{
            knit next_loop;
        }
    }
}