import cast_ons;

width = 40;
height = 100;
with Carrier as c1:{
    in Leftward direction: {
        tuck Front_Needles[0:width:2];
    }
    in reverse direction: {
        tuck Back_Needles[1:width:2];
    }


    for i in range(0, height):{
        in reverse direction:{
            knit Loops;
        }
        xfer Loops across;
    }
}