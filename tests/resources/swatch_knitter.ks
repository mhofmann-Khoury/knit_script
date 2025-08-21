import needles;

def get_needle_holding_loop(loop):{
	// Gets the current needle holding the given loop if the loop is on a needle.
	// Args: loop (Loop): The loop to find the needle of.
	// Returns: (None | Needle): None if the loop is not on a needle, otherwise return the needle that holds the loop.
	return needles.loops_to_current_needles(machine)[loop];
}

def get_stitch_pull_direction(child_loop):{
	// Gets the pull_direction (back to front for knits, front to back for purls) of a given loop's stitch through through the given child loop.
	// Arg: child_loop (Loop): The loop that is the child of a stitch of a given pull direction.
	// Returns: (None | str): Returns None if the given loop is not pulled through any parents. Otherwise, returns the string value of the pull-direction that this loop is pulled through its parent loops.
	if child_loop.has_parent_loops():{
		parent_loop = child_loop.parent_loops[0];
		return str(swatch.get_pull_direction(parent_loop, child_loop));
	} else:{
		return None;
	}
}

def get_positioned_parent_loop(child_loop):{
	// Gets the parent loop that the child loop is pulled through that is at the needle position where the child loop will be formed.
	// Args: child_loop (Loop): The child loop in the stitch to find the positioning parent of.
	// Returns: (None | Loop): None if the child_loop has no parents.
	//      Otherwise, returns the parent loop at the bottom of the parent loop stack, which should be on the needle that the child will be knit on.
	if child_loop.has_parent_loops():{
		return child_loop.parent_loops[0];
	}
	return None;
}

def prepare_knits_and_purls(course):{
	// Prepares the loops in the course to be knit or purled by transferring them to the appropriate bed.
	// Knit stitches are formed only on the Front bed.
	// Purl Stitches are formed only on the Back bed.
	knits = [];
	purls = [];
	for loop in course:{
		stitch_type = get_stitch_pull_direction(loop);
		if stitch_type is not None:{
			parent_loop = get_positioned_parent_loop(loop);
			parent_needle = get_needle_holding_loop(parent_loop);
			assert parent_needle is not None;
			if stitch_type == "Knit":{
				knits.append(parent_needle);
			} elif stitch_type == "Purl":{
				purls.append(parent_needle);
			}
		} // If the stitch_type is None, it is not added to the transfers
	}
	xfer knits across to Front bed; // Only the knits that are not on the front bed are transferred.
	xfer purls across to Back bed; // Only the purls that are not on the back bed are transferred.
}

def get_loop_offset(current_loop, target_loop):{
	// Gets the offset needed to move a loop from one needle to the position of another loop.
	// Args:
	//  current_loop (Loop): The loop at the current position. This loop is assumed to currently be held on a needle.
	//  target_loop (Loop): The loop at the target position. This loop is assumed to currently be held on a needle.
	// Returns: int: The offset distance from the current loop to the target loop.
	current_needle = get_needle_holding_loop(current_loop);
	assert current_needle is not None;
	target_needle = get_needle_holding_loop(target_loop);
	assert target_needle is not None;
	offset = target_needle.position - current_needle.position;
	return offset;
}

def get_stitch_offset(parent_loop, child_loop):{
	// Gets the offset needed to move a parent loop to align with the given child loop to form a stitch.
	// Args:
	//  parent_loop (Loop): The parent loop in the resulting stitch. This loop is assumed to currently be held on a needle.
	//  child_loop (Loop): The child loop in the resulting stitch. The position of this child loop will be determined by the first parent loop in it's stack.
	//      This parent is assumed to be on a needle. The parent_loop is assumed to be a parent of this child_loop.
	// Returns: int: The offset distance from the current position of the parent loop the position that the child loop will be formed.
	positioning_parent = get_positioned_parent_loop(child_loop);
	return get_loop_offset(parent_loop, positioning_parent);
}

def offset_loops_by_depth_and_offsets(depths_to_offsets_to_current_needles):{
	// Move loops based on the given depth and offset information.
	// Loops should be moved in groups of a given depth with the highest depths moved first, and later depths moved later.
	// Each loop held on a current needle will be moved by the given offset. Positive offsets move loops to the right, and negative offsets move loops to the Left.
	// All loops should be moved while on the front bed. Loops are offset to the back bed then returned to the front bed to land on their final position.
	// Args:
	//  depths_to_offsets_to_current_needles (Dict[int, Dict[int, List[Needle]]:
	//      dictionary of depth values keyed to dictionaries of offset values keyed to the needles currently holding a loop to moved by that offset.
	if (len(depths_to_offsets_to_current_needles) == 1) and (0 in depths_to_offsets_to_current_needles):{
		depths_to_offsets_to_current_needles = {}; // Everything is just 0 offsets, so you skip this.
	}
	if len(depths_to_offsets_to_current_needles) > 0:{
		xfer Loops across to Front bed; // Move everything to Front bed for rearrangement into decreases
		returns = [];
		for depth, offsets in depths_to_offsets_to_current_needles.items():{
			for offset, needles_to_xfer in offsets.items():{
				if offset > 0:{
					xfer needles_to_xfer offset to Right;
				}
				elif offset < 0:{
					xfer needles_to_xfer abs(offset) to Left;
				}
				returns.extend(Last_Pass.values());
			}
		}
		xfer returns across;
	}
}

def offset_loops_for_decreases(course):{
	depth_to_offsets_to_current_needles = {}; // dictionary of depth values keyed to dictionaries of offset values keyed to the needle currently holding a loop to moved by that offset.
	for child_loop in course:{
		for depth, parent_loop in enumerate(child_loop.parent_loops):{
			if depth not in depth_to_offsets_to_current_needles:{
				depth_to_offsets_to_current_needles[depth] = {}; // dictionary of offsets at this depth keyed to needles holding loops to move at that depth and offset.
			}
			offset = get_stitch_offset(parent_loop, child_loop);
			if offset not in depth_to_offsets_to_current_needles[depth]:{
				depth_to_offsets_to_current_needles[depth][offset] = [];
			}
			depth_to_offsets_to_current_needles[depth][offset].append(get_needle_holding_loop(parent_loop));
		}
	}
	offset_loops_by_depth_and_offsets(depth_to_offsets_to_current_needles);
}

def find_yarn_over_needles(course_width):{
	// Gets the front bed needles where Yarn-overs should be formed in the next course. Yarn-overs should be formed on any slot (front and back bed needle) that do not hold a loop.
	// Args: course_width (int): The width of the course. Yarn overs can be formed on the 0 index and course_width-1 slots.
	// Returns: List[Needle]: The list of front-bed needles where yarn-overs are to be formed.
	yos = [];
	for i in range(0, course_width):{
		if (not Front_Needles[i].has_loops) and (not Back_Needles[i].has_loops):{
			yos.append(Front_Needles[i]); // add yarn-overs on any slot that does not have a loop to knit through.
		}
	}
	return yos;
}

first_course = courses[0];

with Carrier as c1:{
	// Cast on loops to match the width of the first course.
	in Leftward direction:{
		tuck Front_Needles[0:len(first_course):2];
	}
	in Rightward direction:{
		tuck Front_Needles[1:len(first_course):2];
	}
	releasehook;
	for r, c in enumerate(courses[1:]):{
		offset_loops_for_decreases(c); // Move all loops to form decreases
		prepare_knits_and_purls(c); // Move loops to form knits and purls for the next row.
		yos = find_yarn_over_needles(len(first_course));
		in reverse direction:{
			knit Loops; // Knit through the stitches that were prepared.
			tuck yos; // Knit through needle slots that are missing a loop to form the yarn overs.
		}
	}
}
