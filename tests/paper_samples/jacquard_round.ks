//with Racking as 0.25:{
//	drop [n for n in Needles[0:40]];
//}

width = 4 ;
with Carrier as 1:{
//with Racking as -0.75:{
//	drop [n for n in Front_Needles[0:width]], [n for n in Back_Needles[0:width]];
//	print f"Left tuck at {Current_Racking}";
//	in Leftward direction:{
//		tuck [n for n in Front_Needles[0:width]];
//		tuck [n for n in Back_Needles[0:width]];
//	}
//	print f"Right knit at {Current_Racking}";
//	in Rightward direction:{
//		knit [n for n in Front_Needles[0:width]];
//		knit [n for n in Back_Needles[0:width]];
//	}
//	print f"Left knit  at {Current_Racking}";
//	in Leftward direction:{
//		knit [n for n in Front_Needles[0:width]];
//		knit [n for n in Back_Needles[0:width]];
//	}
//	print f"Right tuck  at {Current_Racking}";
//	in Rightward direction:{
//		tuck [n for n in Front_Needles[0:width]];
//		tuck [n for n in Back_Needles[0:width]];
//	}
//}
	rack = -1;
	with Racking as 0:{
		//drop [n for n in Front_Needles[0:width]], [n for n in Back_Needles[0:width]];
		print f"Left tuck at {Current_Racking}";
		in Leftward direction:{
			tuck [n for n in Front_Needles[0:width]];
			tuck [n for n in Back_Needles[0:width]];
		}
		print f"Right knit at {Current_Racking}";
		in Rightward direction:{
			knit [n for n in Front_Needles[0:width]];
			knit [n for n in Back_Needles[0:width]];
		}
		print f"Left knit  at {Current_Racking}";
		in Leftward direction:{
			knit [n for n in Front_Needles[0:width]];
			knit [n for n in Back_Needles[0:width]];
		}
		print f"Right tuck  at {Current_Racking}";
		in Rightward direction:{
			tuck [n for n in Front_Needles[0:width]];
			tuck [n for n in Back_Needles[0:width]];
		}
	}
}