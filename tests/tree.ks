import Markov_Tree;
import cast_ons;
import needles;
import random;

//random.seed(1);
width  = 40;
height = 40;
m_tree = Markov_Tree.Markov_Tree(width, height);
tree = m_tree.tree;

print f"\n{m_tree}";
def prepare_row(row):{
	sorted_loops = needles.direction_sorted_needles(Loops, Rightward);
	print f"Loops before prep:{sorted_loops}";
	knits = [];
	purls = [];
	skip=False;
	for i in range(0, len(row)-1):{
		if skip:{
			skip = False;
		} else:{
			l_value = row[i];
			l_needle = sorted_loops[i];
			r_value = None;
			r_needle = None;
			if (i+1) < len(row):{
				r_value = row[i+1];
				r_needle = sorted_loops[i+1];
			}
			if l_value is None:{
				if r_value is Markov_Tree.Directions.Right_Branch:{ // rp-twist
					knits.append(l_needle);
					purls.append(r_needle);
					skip = True;
				} else:{
					purls.append(l_needle); // just a purl
				}
			} elif l_value is Markov_Tree.Directions.Left_Branch:{
				assert not (r_needle is None), "Prep: Cannot branch left on edge";
				knits.append(r_needle); // just a knit
				if r_value is Markov_Tree.Directions.Straight:{ // lk-twist
					knits.append(l_needle);
				} else:{ // lp-twist
					purls.append(l_needle);
				}
				skip=True;
			} elif l_value is Markov_Tree.Directions.Straight:{
				knits.append(l_needle);
				if r_value is Markov_Tree.Directions.Right_Branch:{ // rk-twist
					knits.append(l_needle);
					knits.append(r_needle);
					skip=True;
				}
			}
		}
	}
	xfer purls across to back bed;
	if len(Last_Pass)>0:{print f"Prepared purls: {Last_Pass}";}
	xfer knits across to front bed;
	if len(Last_Pass)>0:{print f"Prepared knits: {Last_Pass}";}
	in reverse direction:{
		knit Loops;
	}


}

def cable_row(row):{
	sorted_loops = needles.direction_sorted_needles(Loops, Rightward);
	print f"Loops before Cable Process: {sorted_loops}";
	cabled_knits = [];
	cables = []; // stitches involved in a cable (must send start xfers on back bed
	knit_lefts = []; // priority knits to transfer left
	knit_rights = []; // priority knits to transfer right
	lefts = []; // knits to transfer left
	rights = []; //knits to transfer left
	purl_lefts = []; // purls to transfer left
	purl_rights = []; // purls to transfer right
	skip=False;
	for i in range(0, len(row)-1):{
		if skip:{
			skip = False;
		} else:{
			l_value = row[i];
			l_needle = sorted_loops[i];
			r_value = None;
			r_needle = None;
			if (i+1) < len(row):{
				r_value = row[i+1];
				r_needle = sorted_loops[i+1];
			}
			if l_value is None:{
				if r_value is Markov_Tree.Directions.Right_Branch:{ // rp-twist
					cables.extend([l_needle, r_needle]);
					rights.append(Back_Needles[l_needle.position]);
					purl_lefts.append(Back_Needles[r_needle.position]);
					skip=True;
				}
			} elif l_value is Markov_Tree.Directions.Left_Branch:{
				assert not (r_needle is None), "Cable: Cannot branch on edge";
				cables.extend([l_needle, r_needle]);
				if r_value is Markov_Tree.Directions.Straight:{ // lk-twist
					knit_lefts.append(Back_Needles[r_needle.position]);
					rights.append(Back_Needles[l_needle.position]);
				} else:{ // lp-twist
					lefts.append(Back_Needles[r_needle.position]);
					purl_rights.append(Back_Needles[l_needle.position]);
				}
				skip=True;
			} elif l_value is Markov_Tree.Directions.Straight:{
				if r_value is Markov_Tree.Directions.Right_Branch:{ // rk-twist
					cables.extend([l_needle, r_needle]);
					knit_rights.append(Back_Needles[l_needle.position]);
					lefts.append(Back_Needles[r_needle.position]);
					skip=True;
				}
			}
		}
	}
	purl_xfers = [];
	xfer cables across to back bed;
	if len(Last_Pass)>0:{print f"Knits transferred for cable: {Last_Pass}";}
	xfer knit_lefts 1 to Leftward to front bed;
	if len(Last_Pass)>0:{print f"knit_lefts to front left: {Last_Pass}";}
	xfer knit_rights 1 to Rightward to front bed;
	if len(Last_Pass)>0:{print f"knit_rights to front right: {Last_Pass}";}
	xfer lefts 1 to Leftward to front bed;
	if len(Last_Pass)>0:{print f"lefts to front left: {Last_Pass}";}
	xfer rights 1 to Rightward to front bed;
	if len(Last_Pass)>0:{print f"rights to front right: {Last_Pass}";}
	xfer purl_lefts 1 to Leftward to front bed;
	if len(Last_Pass)>0:{print f"purl_lefts to front left: {Last_Pass}";}
	purl_xfers.extend(Last_Pass.values());
	xfer purl_rights 1 to Rightward to front bed;
	if len(Last_Pass)>0:{print f"purl_rights to front right: {Last_Pass}";}
	purl_xfers.extend(Last_Pass.values());
	xfer purl_xfers across to back bed;
	if len(Last_Pass)>0:{print f"Purls returned to back: {Last_Pass}";}
	in reverse direction:{
		knit Loops;
	}
}

with Carrier as 1:{
	start_row = tree[0];
	co_needles = [];
	for i, pos in enumerate(start_row):{
		if pos is None:{
			co_needles.append(Back_Needles[i]);
		} else:{
			co_needles.append(Front_Needles[i]);
		}
	}
	cast_ons.alt_tuck_needle_set(co_needles);
	in reverse direction:{
		knit Loops;
	}
//	prepare_row(tree[1]);
//	cable_row(tree[1]);

	for i, row in enumerate(tree):{
		print f"Row {i}: {row}";
		prepare_row(row);
		cable_row(row);
	}
}