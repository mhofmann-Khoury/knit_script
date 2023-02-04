
import cast_ons;
import stockinette;
import bind_offs;
width = 4;
height = 2;

with Carrier as 1:{
    cast_ons.alt_tuck_cast_on(width);
    stockinette.stst(height);
    xfer Loops[::2] across to Back bed;
	//knit pattern for each row
	for r in range(0, height):{
		in reverse direction:{
			knit Loops;
		}
	}
    bind_offs.chain_bind_off(Loops);
}