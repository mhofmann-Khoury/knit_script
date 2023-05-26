;;Width: 500;
;;Position: Left;
import cast_on_mod;

base_yarn = c1;
magic_yarn = c2;
copper_yarn = c3;

width = 100;

co_needles = [];
with Gauge as 3:{
	co_needles = (s0.Front_Needles)[0:width];
	co_needles.extend(s2.Back_Needles[0:width]);
}
with Gauge as 1, Carrier as base_yarn:{
	cast_on_mod.cast_on(co_needles);
}