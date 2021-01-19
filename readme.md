# Porous like invariants

## Tool
Run everything from the `code` directory. The following assumes you invoke python3 via the command `python3`. Depending on your installation you may use just `python` (but this may be python2 which is not correct).

Ensure you have the python package `tabulate` installed (via `pip3 install tabulate`).

To run the tool either `python3 runner.py [problemfile]` for example `python3 runner.py problems/my.problem`

Or start the server `python3 server.py` (ensure port 8000 is clear) and visit `http://localhost:8000/`

See `runner.py` for examples of how to manually create instances and invoke from python code.

## Evaluations

`problembuilder.py` makes random instances. Change the max variable in the file to control the instances. The analysis is placed into `document.csv` and read by `analysis.py`.



