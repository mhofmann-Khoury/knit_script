width = 159;
height = 1100;

with Carrier as c1:{
    kfb_one = [n for n in Front_Needles[0:width:4]];
    transfer_kfb_one = [n for n in Back_Needles[2:width:4]];
    kfb_two = [n for n in Front_Needles[0:width:2]];
    transfer_kfb_two = [n for n in Back_Needles[1:width:2]];


    in Leftward direction: {
        tuck kfb_one;
    }

    row = 1;
    r = 1;
    for i in range(0, height):{
        if row == 8:{
            print("second kfb: ");
            with racking as -1:{
                in reverse direction:{
                    split kfb_two;
                }
            }
            xfer transfer_kfb_two across;
            row = 1;
            r = 3;
        }

        if row == 4:{
            print("first kfb: ");
            with racking as -2:{
                in reverse direction:{
                    split kfb_one;
                }
            }
            xfer transfer_kfb_one across;
            row = 1;
            r = 2;
        }

        if row == 3:{
            print("knit 3: ");
            in reverse direction:{
                knit Loops;
            }
            print(r);
            if r == 1:{
                row = 4;
            }
            if r == 2:{
                row = 8;
            }
            if r == 3:{
                row = 69;
            }

        }

        if row == 2:{
            print("knit 2: ");
            in reverse direction:{
                knit Loops;
            }
            row = 3;
        }

        if row == 1:{
            print("gardner stitch (knit) three rows: ");
            print("knit 1: ");
            in reverse direction:{
                knit Loops;
            }
            row = 2;
        }
    }
}