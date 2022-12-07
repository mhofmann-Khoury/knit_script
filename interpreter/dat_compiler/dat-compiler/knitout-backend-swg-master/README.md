# Knitout Backend for SWG-N2

This repository contains a backend (/translator) that converts [knitout](https://textiles-lab.github.io/knitout/knitout.html) files to [dat](https://github.com/textiles-lab/DAT-format) files suitable for processing and eventual knitting on Shima Seiki SWGN2-type knitting machines.

## Example

To turn `small-square.knitout` into `small-square.dat`:
```
./knitout-to-dat.js examples/small-square.knitout small-square.dat
```

You can see the result by loading the file in knitpaint or in [show-dat.html](https://textiles-lab.github.io/DAT-format/show-dat.html) from the [dat format](https://github.com/textiles-lab/DAT-format) repository.

## Headers

This backend currently ignores all headers except:

### Position
Position: `Left`/`Center`/ `Right`/`Keep`

Translates needles to lie on the left-end, center, right-end of the needle-bed or keeps the absolute values specified in knitout. 

## Extensions

### Stitch Number: `x-stitch-number N`

On SWGN2 machines, leading and stitch numbers are stored in an on-machine table, and accessed by an index.
The `x-stitch-number N` command sets the stitch table index for the next operation to `N`, which must be an integer between 1 and 120.

### Speed Number: `x-speed-number N`

On SWGN2 machines, speeds are stored in an on-machine table, and accessed by an index between 0 and 15.
The `x-speed-number N` command sets the speed index for the next operation to `N`.

## Quirks

### Carrier Names

This backend assumes that there are ten carriers, named (front-to-back) as 1, 2, ..., 10.

### Stitch Size

SWGN2 machines use a table of stitch values stored on the machine to set the stitch and leading cam values.
This backend implements the knitout `stitch` command by using a lookup table to get stitch values for a given leading/stitch value.

If the lookup table (`STITCH_NUMBERS` in the code) does not match your machine, you may get unexpected results.
The `x-stitch-number` extension allows you to set table indices directly.
<!--
## TODO

### Split Stitches

Split stitches are not yet supported, owing to the weird way in which split stitch loop returns are handled in knitpaint.

### Plating

Plating is handled except for the code to come up with a yarn combination number given a carrier set with more than one carrier.
-->
