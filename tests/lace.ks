;;Width: 500;
import cast_ons;
width = int(5*1);
patterns = 2;

def lace_line(left_first=True):{
	yo_needles = [];
	yo_needles.extend(Front_Loops[1::5]);
	yo_needles.extend(Front_Loops[3::5]);
	print "Storage transfers";
	xfer yo_needles across to back bed;
	if left_first:{
		print "left transfers";
		xfer Back_Loops[1::2] 1 to Leftward to front bed;
		xfer Back_Loops 1 to Rightward to front bed;
	} else:{
		print "right transfers";
		xfer Back_Loops[0::2] 1 to Rightward to front bed;
		xfer Back_Loops 1 to Leftward to front bed;
	}
	in reverse direction:{
		knit Loops;
	}

}

with Carrier as 1:{
	cast_ons.alt_tuck_cast_on(width);

	for p in range(0, patterns):{
		in reverse direction:{
			knit Loops;
		}
		if p%2==0:{
			lace_line(True);
		} else:{
			lace_line(False);
		}
		in reverse direction:{
			knit Loops;
		}
	}
}