with width as 12, height as 10, Carrier as 1:{

    // Collect needles for the front and back of the tube split up by stitch type. Knits on front needles, purl on back needles
    knit_front_tube = [n for n in Front_Needles[0:width:4]];
    purl_front_tube_back_needles = [n for n in Back_Needles[2:width:4]];
    purl_front_tube_front_needles = [n.opposite() for n in purl_front_tube_back_needles];//[n for n in Front_Needles[2:width:4]];

    knit_back_tube_front_needles = [n for n in Front_Needles[1:width:4]];
    knit_back_tube_back_needles = [n.opposite() for n in knit_back_tube_front_needles];
    purl_back_tube = [n for n in Back_Needles[3:width:4]];

    // cast on each side of the tube. Standard cast ons are not designed for half gauge so we have to do it manually
    in Leftward direction:{
        tuck purl_front_tube_front_needles;
    }
    in reverse direction:{
        tuck knit_front_tube;
    }
    in reverse direction:{
        tuck knit_back_tube_back_needles;
    }
    in reverse direction:{
        tuck purl_back_tube;
    }


    for r in range(0, height):{
        xfer purl_front_tube_front_needles across to back bed; // send front of tube cast ons to be back bed to be purled
        // knit front of the tube
        in reverse direction:{
            knit knit_front_tube;
            knit purl_front_tube_back_needles; // Note: knits and purls will merge to alternate based on bed order
        }
        xfer purl_front_tube_back_needles across to front bed; // move front tube purls out of way of back of tube knitting
        xfer knit_back_tube_back_needles across to front bed; // return knits back bed to their position on front bed needles
        // knit back of tube
        in reverse direction:{
            knit knit_back_tube_front_needles;
            knit purl_back_tube;
        }
        xfer knit_back_tube_front_needles across to back bed; // move back of tube knits out of way of front of tube knitting
    }

}