
from typing import Dict, Tuple, List
import copy


def lerp (a: float, b: float, total_steps: int, current_step: int) :
    diff = b - a;
    diff = diff / total_steps
    return a + diff * current_step


class Atom:
    reverseLegend: Dict[str, int] = dict()

    def __init__(self):
        self.data_vals = dict();

    def __getitem__(self, key):
        return self.data_vals[key]

    def __setitem__(self, key, value):
        self.data_vals[key] = value

    def getXIndex():
        return "_atom_site_fract_x"
    def getYIndex():
        return "_atom_site_fract_y"
    def getZIndex():
        return "_atom_site_fract_z"

    def getX(self) -> float:
        return float(self[Atom.getXIndex()])
    def getY(self) -> float:
        return float(self[Atom.getYIndex()])
    def getZ(self) -> float:
        return float(self[Atom.getZIndex()])

   
    def setX(self, x) :
        self[Atom.getXIndex()] = x
    def setY(self, y) :
        self[Atom.getYIndex()] = y
    def setZ(self, z) :
        self[Atom.getZIndex()] = z

    def setXYZ(self, x,y,z) :
       self.setX(x)
       self.setY(y)
       self.setZ(z)

    def normalize(self):
        if self.getX() > 1.0:
            self.setX(self.getX() % 1)
        if self.getY() > 1.0:
            self.setY(self.getY() % 1)
        if self.getZ() > 1.0:
            self.setZ(self.getZ() % 1)
    
    def lerp_to_inversion(self, total_steps: int, current_step : int):
        newAtom = Atom()
        newAtom.data_vals = self.data_vals.copy()
        oldX = self.getX()
        oldY = self.getY()
        oldZ = self.getZ()

        newX = lerp(oldX, -(oldX - 0.5)+0.5, total_steps, current_step)
        newY = lerp(oldY, -(oldY - 0.5)+0.5, total_steps, current_step)
        newZ = lerp(oldZ, -(oldZ - 0.5)+0.5, total_steps, current_step)

        newAtom[Atom.getXIndex()] = newX
        newAtom[Atom.getYIndex()] = newY
        newAtom[Atom.getZIndex()] = newZ
        return newAtom

    def move(self, x,y,z) :
        self.setX(self.getX() + x)
        self.setY(self.getY() + y)
        self.setZ(self.getZ() + z)

    def cell_edge_copies(self):
        tempSet = set()
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    tempAtom = copy.deepcopy(self)
                    tempAtom.move(i,j,k)
                    tempAtom.normalize()
                    tempSet.add(tempAtom)
        return tempSet


    def __eq__(self, other):
        return self.data_vals == other.data_vals
    
    def __hash__(self):
        return tuple(self.data_vals).__hash__()

    def __str__(self):
        return str(list(self.data_vals.values()))

    def __repr__(self):
        return self.__str__()