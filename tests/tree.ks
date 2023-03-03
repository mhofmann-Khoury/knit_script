import Markov_Tree;
import cast_ons;
import needles;
import random;

random.seed(1);
width  = 10;
height = 10;
m_tree = Markov_Tree.Markov_Tree(width, height);
tree = m_tree.tree;

print f"\n{m_tree}";

def prepare_row(row):{
	purls = [];
	lefts = [];
	straights = [];
	rights = [];
	sorted_loops = needles.direction_sorted_needles(Loops, Rightward);
	for i, pos in enumerate(row):{
		if pos is Markov_Tree.Directions.Left_Branch:{
			lefts.append(sorted_loops[i]);
		} elif pos is Markov_Tree.Directions.Right_Branch:{
			rights.append(sorted_loops[i]);
		} elif pos is Markov_Tree.Directions.Straight:{
			straights.append(sorted_loops[i]);
		} else:{
			purls.append(sorted_loops[i]);
		}
	}
	xfer lefts, straights, rights across to front bed;
	xfer purls across to back bed;
	in reverse direction:{
		knit Loops;
	}
}

def cable_row(row):{
	sorted_loops = needles.direction_sorted_needles(Loops, Rightward);
	purls = [p for p in Back_Loops];
	knits = [k for k in Front_Loops];
	print f"Xfer cables to back: {knits}";
	xfer knits across to back bed;
	knit_lefts = [];
	knit_rights = [];
	lefts = [];
	rights = [];
	purl_lefts = [];
	purl_rights = [];
	for i, p in enumerate(row):{
		n = sorted_loops[i];
		if p is Markov_Tree.Directions.Left_Branch:{
			if n in purls:{
				purl_lefts.append(n);
			} elif row[i+1] is Markov_Tree.Directions.Straight:{
				knit_lefts.append(n);
				rights.append(sorted_loops[i+1]);
			} else:{
				lefts.append(n);
			}
		} elif p is Markov_Tree.Directions.Right_Branch:{
			if n in purls:{
				purl_rights.append(n);
			} elif row[i-1] is Markov_Tree.Directions.Straight:{
				knit_rights.append(n);
				lefts.append(sorted_loops[i+1]);
			} else:{
				rights.append(n);
			}
		}
	}

	print f"Xfer knit_lefts to front left: {knit_lefts}";
	xfer knit_lefts 1 to Leftward to front bed;
	print f"Xfer knit_rights to front right: {knit_rights}";
	xfer knit_rights 1 to Rightward to front bed;
	print f"Xfer lefts to front left: {lefts}";
	xfer lefts 1 to Leftward to front bed;
	print f"Xfer rights to front right: {rights}";
	xfer rights 1 to Rightward to front bed;
	print f"Xfer purl_lefts to front left: {purl_lefts}";
	xfer purl_lefts 1 to Leftward to front bed;
	print f"Xfer purl_rights to front right: {purl_rights}";
	xfer purl_rights 1 to Rightward to front bed;
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

	prepare_row(tree[1]);
	cable_row(tree[1]);
}