import cast_ons;
import sort;
import dictComp;
import sortPriority;

//trinity stitch pattern (aka Raspberry or Blackberry) but with fake (k1, p1, k1)

width = 12;
height = 12;

//def knit_Transfer(loops, offsetVals, minOff, maxOff):{
    //for i in range(minOff, maxOff):{
        //if offset < 0:{
            //xfer loops offset to Leftward to Front bed;
        //}
        //else:{
            //xfer loops offset to Rightward to Front bed;
        //}
    //}
//}

//helper func that creates dict for position offsets
//currently intended use not user but helper func for transfer func
//but could make it so user creates dict using function and carries it in as param for transfer func
//Pre: list of offsets for pattern, int for pattern width, int for num of repeats
//Post: dictionary that represents transfer planning that contains offset for each position
//      key = needle position/num, value = offset
def createDict(offsetList, patternWidth, repeatNum):{
    //repeatNum = repeatNum + 1; //add 1 for appropriate amount of repeat (if default repeatNum is 0)
    positionList = [x for x in range(patternWidth * repeatNum)]; //create position key list
    offsetList = offsetList * repeatNum; //create offset value list
    posOffsetDict = dictComp.dictCo(positionList, offsetList); //create dict
    //print(posOffsetDict);
    return posOffsetDict;
}

//could also use start/end needles for each
//transfer planning func for when stack order does not matter
//Pre: loops being transferred, offset list for pattern, int for num of repeats (default val of 1 of not given)
//Post: appropriate transfers made with not guaranteed stack order
def knit_transfer_schoolbus(loops, offList, repeatN = 1):{//, minOff, maxOff):{
    xfer Loops across to Back bed;
    pWid = len(offList);
    //print(pWid);
    loopsDict = createDict(offList, pWid, repeatN);
    sortedLoopsDict = sort.sortD(loopsDict); //sort dict in increasing order by offset val

    //print(sortedLoopsDict);
    for i, offset in sortedLoopsDict.items():{ //iterate through dict (in order of smallest offset to largest)
        if offset < 0:{ //neg offset go left
            absOffset = abs(offset);
            xfer loops[i] absOffset to Left to Front bed;
        }
        else:{ //pos offset go right
            xfer loops[i] offset to Rightward to Front bed;
        }
    }
}

//helper func for transfer planning when stack order matters
//creates and sorts dict by stack layer
//Pre: list of offsets for pattern, list of stack layer num, int for pattern width, int for num of repeats
//Post: dictionary of lists that represents transfer planning ordered by stack layer and contains offset for each position
//      key = needle position/num, value = list with list[0]: offset, list[1]: stack layer num
def createPriorityDict(offsetList, layerList, patternWidth, repeatNum):{
    //repeatNum = repeatNum + 1; //add 1 for appropriate amount of repeat (if default repeatNum is 0)
    positionList = [x for x in range(patternWidth * repeatNum)]; //create position key list
    offsetList = offsetList * repeatNum; //create offset value list
    layerList = layerList * repeatNum;
    layerPriorityDict = sortPriority.sortCompDictPriority(positionList, offsetList, layerList); //create dict and sort by layers
    //print(posOffsetDict);
    return layerPriorityDict;
}

//transfer planning func for when stack order matters
//Pre: loops being transferred, offset list for pattern, List for stack layer, int for num of repeats (default val of 1 of not given)
//Post: appropriate transfers made with correct stack order
def transfer_schoolbus_stackOrder(loops, offList, stackLayerList, repeatN = 1):{
    xfer Loops across to Back bed;
    pWid = len(offList);
    //print(pWid);
    sortedLoopsPriorityDict = createPriorityDict(offList, stackLayerList, pWid, repeatN); //only one instance of pattern regardless of if user wants repeats --> repeats happen in sorting
    //print(sortedLoopsPriorityDict);

    for i in sortedLoopsPriorityDict.items():{ //iterate through each key in dict
        //print(i);
        if i[1][0] < 0:{ //neg offset go left
            absOffset = abs(i[1][0]);
            xfer loops[i[0]] absOffset to Leftward to Front bed;
        }
        else:{ //pos offset go right
            xfer loops[i[0]] i[1][0] to Rightward to Front bed;
        }
    }
}

with Carrier as c1:{

    p3tog_l2 = [n for n in Front_Needles[3:width:4]];
    tuck_p_l2 = [n for n in Back_Needles[1:width:4]];
    tuck_k_l2 = [n for n in Front_Needles[2:width:4]];

    p3tog_l4 = [n for n in Front_Needles[0:width:4]];
    tuck_p_l4 = [n for n in Back_Needles[2:width:4]];
    tuck_k_l4 = [n for n in Front_Needles[1:width:4]];

    offsetTrinityL2 = [0, 2, 1, 0];
    offsetTrinityL4 = [0, -1, -2, 0];
    stackOrderTrinityL4 = [0, 1, 2, 0];

    //print(p3tog);

//    in Leftward direction: {
//        tuck Back_Needles[0:width:2];
//    }
//    in reverse direction: {
//        tuck Back_Needles[1:width:2];
//    }

	cast_ons.alt_tuck_cast_on(width, is_front=False);

    //exDict = {0: 0, 1: -1, 2: -1, 3: -2, 4: -1, 5: -2};
    //oList = [0, -1, -1, -2, -1, -2];
    //pList = [0, 1, 1, 0, 1, 0];

    count = 1;
    for i in range(0, height):{
        //row one: purl
        if count == 1:{
            xfer Loops across to Back bed;
            in reverse direction:{
                knit Loops;
            }
            count = 2;
        }

        //row two: (k1, p1, k1) into next stitch (increase, fake version), p3tog (decrease)
        if count == 2:{
            knit_transfer_schoolbus(Back_Needles, offsetTrinityL2, 3);
            xfer p3tog_l2 across to Back bed;

            in reverse direction:{
                tuck tuck_p_l2;
            }
            in reverse direction:{
                tuck tuck_k_l2;
            }

            in reverse direction:{
                knit Loops;
            }

            count = 3;
        }

        if count == 3:{
            xfer Loops across to Back bed;
            in reverse direction:{
                knit Loops;
            }
            count = 4;
        }

        if count == 4:{
            transfer_schoolbus_stackOrder(Back_Needles, offsetTrinityL4, stackOrderTrinityL4, 3);
            xfer p3tog_l4 across to Back bed;

            in reverse direction:{
                tuck tuck_k_l4;
            }
            in reverse direction:{
                tuck tuck_p_l4;
            }

            in reverse direction:{
                knit Loops;
            }

            count = 1;
        }

        //in reverse direction:{
            //split Front_Needles;
        //}

        //transfer_schoolbus_stackOrder(Back_Needles, oList, pList);
        //xfer Loops across to Back bed;
    }
}