import cast_ons;
import needles;

loop_id_to_needle = {};

def update_loops_to_needles():{
	for needle in Loops:{
		for held_loop in needle.held_loops:{
			loop_id_to_needle[held_loop.loop_id] = needle;
		}
	}
}

def get_stitch_pull_direction(loop_id):{
	child_id = swatch.get_child_loop(loop_id);
	return_val = None;
	if not(child_id is None):{
		return_val = str(swatch.get_stitch_edge(loop_id, child_id, "pull_direction"));
	}
	return return_val;
}

def get_stitch_offset(loop_id):{
	child_id = swatch.get_child_loop(loop_id);
	return_val = None;
	if not(child_id is None):{
		return_val = swatch.get_stitch_edge(loop_id, child_id, "parent_offset");
	}
	return return_val;
}

def get_stitch_depth(loop_id):{
	child_id = swatch.get_child_loop(loop_id);
	return_val = None;
	if not(child_id is None):{
		return_val = swatch.get_stitch_edge(loop_id, child_id, "depth");
	}
	return return_val;
}

def prepare_knits_and_purls(course):{
	knits = [];
	purls = [];
	for loop_id in course:{
		current_needle = loop_id_to_needle[loop_id];
		stitch_type = get_stitch_pull_direction(loop_id);
		if stitch_type == "Knit":{
			knits.append(current_needle);
		} elif stitch_type == "Purl":{
			purls.append(current_needle);
		}
	}
	xfer knits across to front bed;
	xfer purls across to back bed;
	update_loops_to_needles();
}


def offset_new_loops(course):{
	depth_to_offsets_to_current_needle = {};
	for loop_id in course:{
		current_needle = loop_id_to_needle[loop_id];
		offset = get_stitch_offset(loop_id);
		depth = get_stitch_depth(loop_id);
		if not(offset is None):{
			if offset != 0:{
				if depth not in depth_to_offsets_to_current_needle:{
					depth_to_offsets_to_current_needle[depth] = {};
				}
				if offset not in depth_to_offsets_to_current_needle[depth]:{
					depth_to_offsets_to_current_needle[depth][offset]= [];
				}
				depth_to_offsets_to_current_needle[depth][offset].append(current_needle);
			}

		}
	}

	if len(depth_to_offsets_to_current_needle) > 0:{
		xfer Loops across to Front bed;

		returns = [];
		for depth, offsets in depth_to_offsets_to_current_needle.items():{
			for offset, needles_to_xfer in offsets.items():{
				if offset > 0:{
					xfer needles_to_xfer offset to Right;
				}
				else:{
					xfer needles_to_xfer abs(offset) to Left;
				}
				returns.extend(Last_Pass.values());
			}
		}
		xfer returns across;
		update_loops_to_needles();
	}
}

first_course = courses[0];

with Carrier as c1:{
	in Rightward direction:{
		tuck Front_Needles[0:len(first_course)];
	}
	update_loops_to_needles();
	offset_new_loops(first_course);
	prepare_knits_and_purls(first_course);
	for r, course in enumerate(courses):{
		if r > 0:{
			yos = [];
			for i in range(0, len(first_course)):{
				if (needles.needle(True, i) not in Loops) and (needles.needle(False, i) not in Loops):{
					yos.append(needles.needle(True, i));
				}
			}
			in reverse direction:{
				knit Loops;
				tuck yos;
			}
			update_loops_to_needles();
			offset_new_loops(course);
			prepare_knits_and_purls(course);
		}
	}
}