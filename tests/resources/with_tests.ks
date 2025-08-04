p = "dog";
with Carrier as c1:{
	p = "cat";
	p2 = "bird";
	print f"p in with-1: {p}";
	in Leftward direction:{
		tuck Front_Needles[0:10];
	}
	releasehook;
}
print f"Carrier after with-1: {Carrier}";
assert Carrier is None;
print f"p after with-1: {p}";
assert p == "cat", p;

with p as "bird", Racking as 2:{
	print f"p in with-2: {p}";
	assert p == "bird", p;
}
print f"Racking after with-2: {Racking}";
assert Racking == 0.0;
print f"p after with-2: {p}";
assert p == "bird", p;
