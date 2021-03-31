# Porous Invariants Tool

## Easy Version

A live instance is available at [http://invariants.1251.uk](http://invariants.1251.uk)


## Licence

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.


## Installation

* Clone or copy the directory onto your machine.
* Ensure you have Python 3 installed. 
 - The following document assumes you invoke python3 via the command `python3`. Depending on your installation you may use just `python` (but some installations this may invoke python2 which is not correct and will not work).
* Ensure you have the python package `tabulate` installed (via `pip3 install tabulate`).

## Tool

To run the tool from a problem file run `python3 runner.py [problemfile]` for example `python3 runner.py problems/my.problem`. There are some example problems in the problems folder.

Or start the server `python3 server.py` (ensure port 8000 is clear) and visit `http://localhost:8000/`. To run on a `wsgi` webserver the file is `wsgi`, but a live instance of this can be seen at `http://invariants.1251.uk`.

See `directinvoke.py` for examples of how to manually create instances and invoke from python code.

If you want to inspect the guts of the code, which actually builds the invariants, see `tool.py`. This file cannot be invoked directly.

## Evaluations

`problembuilder.py` runs the analysis in the paper.
It creates random instances depending on a size parameter from 8 to 1024.
The output of each test is placed into `document.csv`. The analysis in the paper is computed by `analysis.py` (reading `document.csv`).

Every instance is stored inside the good and error folder within the problems folder, along with the output (below the ENDS of the input). Instances in the error folder are instances which did not produce a proof of reachability (a sequence of functions to get to the target), although it did decide that the instance is a reachable instance. This failure of detection is due to a timeout.

## Problem format

On the first line write the start point, target and optionally whether you expect it to be reachable. The only effect of this is that the problem will tell you whether expectation=reality and is not used as a hint in the analysis.

Supported targets are single numbers, or Z-linear sets, with {b+pZ} specified as b+p. Negative periods should be written as `4+-2` for example, although this is equivalent to `4+2` and will be considered as such. If the supplied base is outside of 0...p-1 it will be normalised into this set.

On subsequent lines, write the functions by writing the multiplier and the adder, i.e. a b means f(x) = ax+b. 

On the line after the last function, optionally, write ENDS. Everything after ENDS will be ignored.
<code>
start target[+period] [True|False]<br>
a b<br>
...<br>
a b<br>
[ENDS] 
</code>


