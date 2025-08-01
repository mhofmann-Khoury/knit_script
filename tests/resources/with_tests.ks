p = "dog";
with Carrier as c1:{
	p = "cat";
	print f"p in with-1: {p}";
	in Leftward direction:{
		tuck Front_Needles[0:10];
	}
	releasehook;
}
print f"Carrier after with-1: {Carrier}";
print f"p after with-1: {p}";
assert p == "dog", p;

with p as "bird":{
	print f"p in with-2: {p}";
	assert p == "bird", p;
}
print f"p after with-2: {p}";
assert p == "dog", p;
