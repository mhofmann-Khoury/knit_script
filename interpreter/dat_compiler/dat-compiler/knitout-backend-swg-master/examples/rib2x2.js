#!/bin/sh
':' //; exec "$(command -v nodejs || command -v node)" "$0" "$@"

let min = 1;
let max = 20;

let Carrier = 5;

console.log(";!knitout-2")

console.log("inhook " + Carrier);

for (let n = max; n >= min; --n) {
	if ((max-n) % 2 == 0) {
		console.log("tuck - f" + n + " " + Carrier);
	}
}
for (let n = min; n <= max; ++n) {
	if ((max-n)%2 == 1) {
		console.log("tuck + f" + n + " " + Carrier);
	}
}

for (let n = max; n >= min; --n) {
	console.log("knit - f" + n + " " + Carrier);
}

console.log("releasehook " + Carrier);

let pattern = ['f', 'f', 'b', 'b'];

for (let n = min; n <= max; ++n) {
	if (pattern[(n-min)%pattern.length] === 'b') {
		console.log("xfer f" + n + " b" + n);
	}
}

let rows = 20;

for (let row = 0; row < rows; ++row) {
	if ((row % 2) === 0) {
		//knit to the right on even rows:
		for (let n = min; n <= max; ++n) {
			let bed = pattern[(n-min)%pattern.length];
			console.log("knit + " + bed + n + " " + Carrier);
		}
	} else {
		//knit to the left on odd rows:
		for (let n = max; n >= min; --n) {
			let bed = pattern[(n-min)%pattern.length];
			console.log("knit - " + bed + n + " " + Carrier);
		}
	}
}

console.log("outhook " + Carrier);
