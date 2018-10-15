# CIF_inverter
A simple python program that takes a cif file (with no symmetry, ie, P1)
and will produce a series of output .cif's that step through an inversion through the center of
the unit cell.

It's very fragile (I didn't know about PyCIFRW when I wrote this), but seems to work okay
