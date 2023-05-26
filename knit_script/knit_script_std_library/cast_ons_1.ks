import needles;
def cast_on(co_needles, start_dir:Leftward, knit_rows=2):{
	sections = [];
	co_needles = needles.direction_sorted_needles(co_needles, start_dir);
	section = [co_needles[0], co_needles[1]];
	section_is_same = section[0].is_front == section[1].is_front;
	for l,r in zipe(co_needles[2:-1], co_needles[3:]):{
		last_needle = section[-1];
		if section_is_same:{
			if l.is_front == last_needle.is_front:{
				section.append(l);
			} else:{
				sections.append(section);
				section = [];
				section = [l];
				section_is_same = l.is_front == r.is_front;
			}
		} else:{
			if l.is_front != last_needle.is_front:{
				section.append(l);
			} else:{
				sections.append(section);
				section = [];
				section = [l];
				section_is_same = l.is_front == r.is_front;
			}
		}
	}

	last_needle = section[-1];
	l = co_needles[-1];
	if section_is_same:{
		if l.is_front == last_needle.is_front:{
			section.append(l);
		} else:{
			sections.append(section);
			section = [];
			section = [l];
			section_is_same = l.is_front == r.is_front;
		}
	} else:{
		if l.is_front != last_needle.is_front:{
			section.append(l);
		} else:{
			sections.append(section);
			section = [];
			section = [l];
			section_is_same = l.is_front == r.is_front;
		}
	}
	sections.append(section);
	print sections;
}