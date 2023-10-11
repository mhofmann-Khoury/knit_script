
width = 3;
height = 100;

with Carrier as c1:{
    in Leftward direction:{
        tuck Front_Needles[0:width];
    }

    in reverse direction:{
        tuck Back_Needles[0:width];
    }

    for i in range(0, height):{
        in reverse direction:{
            knit Front_Needles[0:width];
        }
        in reverse direction:{
            knit Back_Needles[0:width];
        }
    }

}