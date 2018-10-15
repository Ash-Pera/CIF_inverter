# CIF_inverter
A simple python program that takes a cif file (with no symmetry, ie, P1)
and will produce a series of output .cif's that step through an inversion through the center of
the unit cell.

It's very fragile (I didn't know about PyCIFRW when I wrote this), but seems to work okay
It's designed to work with CrystalMaker's animation feature, so you can see the inversion.
Just open up the structures pane and drop the output files in (I can't figure out how 
Crystal Maker desieds the order, so maybe one at a time?), then you can play or export the 
animation. If you use the synconize, make sure "atom level syncronization" is NOT checked, 
as to properly visualize the inversion, there's a lot of duplicate atoms
