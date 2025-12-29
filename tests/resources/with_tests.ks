p = "dog";
with Carrier as c1:{
	p = "cat";
	p2 = "bird";
	assert p=="cat", f"p in with-1: {p}";
	in Leftward direction:{
		tuck Front_Needles[0:10];
	}
	releasehook;
}
assert Carrier is None, f"Carrier after with-1: {Carrier}";
assert p == "dog", f"p after with-1: {p}";

with p as "bird", Racking as 2:{
	assert p == "bird", f"p in with-2: {p}";
}
assert Racking == 0.0, f"Expected racking of 0.0 but got {Racking}";
assert p == "dog", p;
