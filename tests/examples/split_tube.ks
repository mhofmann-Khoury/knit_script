import cast_ons;
with Gauge as 2, Carrier as 1, width as 10, height as 20:{
    //cycle layers for first half of working needles
    push Front_Needles[0:width/2] to back;
    // cast on front and back of the tube
	for s in range(0, Gauge):{
		with Sheet as s:{
			cast_ons.alt_tuck_cast_on(width, is_front=s%2==0);
		}
	}
	for r in range(0, height):{
	    for s in range(0, Gauge):{
	        with Sheet as s:{
	            in reverse direction:{
	                knit Loops;
	            }
	        }
	    }
	}
}