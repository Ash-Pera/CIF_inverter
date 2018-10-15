#CIF_inverter
#site: https://github.com/Ash-Pera/CIF_inverter
#written by Ash Pera

from typing import Dict, Tuple, List
from itertools import islice
import os
import copy

def lerp (a: float, b: float, total_steps: int, current_step: int) :
    diff = b - a;
    diff = diff / total_steps
    return a + diff * current_step

class Atom:
    legend: Dict[int, str] = dict()
    reverseLegend: Dict[str, int] = dict()

    def fill_self(self) :
        self.data_vals = [None] * len(Atom.legend)


    def __init__(self):
        self.data_vals = [];
        self.fill_self()

    def getXIndex():
        return Atom.reverseLegend["_atom_site_fract_x\n"]
    def getYIndex():
        return Atom.reverseLegend["_atom_site_fract_y\n"]
    def getZIndex():
        return Atom.reverseLegend["_atom_site_fract_z\n"]

    def getX(self) -> float:
        return float(self.data_vals[Atom.getXIndex()])
    def getY(self) -> float:
        return float(self.data_vals[Atom.getYIndex()])
    def getZ(self) -> float:
        return float(self.data_vals[Atom.getZIndex()])

   
    def setX(self, x) :
        self.data_vals[Atom.getXIndex()] = x
    def setY(self, y) :
        self.data_vals[Atom.getYIndex()] = y
    def setZ(self, z) :
        self.data_vals[Atom.getZIndex()] = z

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
    
    def slerp(self, total_steps: int, current_step : int):
        newAtom = Atom()
        newAtom.data_vals = self.data_vals.copy()
        oldX = self.getX()
        oldY = self.getY()
        oldZ = self.getZ()

        newX = lerp(oldX, -(oldX - 0.5)+0.5, total_steps, current_step)
        newY = lerp(oldY, -(oldY - 0.5)+0.5, total_steps, current_step)
        newZ = lerp(oldZ, -(oldZ - 0.5)+0.5, total_steps, current_step)

        newAtom.data_vals[Atom.getXIndex()] = newX
        newAtom.data_vals[Atom.getYIndex()] = newY
        newAtom.data_vals[Atom.getZIndex()] = newZ
        return newAtom
    def __add__(self, other_atom):
        newAtom: Atom = Atom()
        newAtom.data_vals = self.data_vals.copy()
        newX = self.getX() + other_atom.getX()
        newY = self.getY() + other_atom.getY()
        newZ = self.getZ() + other_atom.getZ()

        newAtom.data_vals[Atom.getXIndex()] = newX
        newAtom.data_vals[Atom.getYIndex()] = newY
        newAtom.data_vals[Atom.getZIndex()] = newZ
        return newAtom

    def __eq__(self, other):
        return self.data_vals == other.data_vals
    
    def __hash__(self):
        return tuple(self.data_vals).__hash__()



atomsList = [];

def try_parse_float(s: str, base: int = 10):
  try:
    return float(s)
  except ValueError:
    return s


inputFileName = input("Input file name (no extension):")
#inputFileName: str = "Symmetry_free_PZT_reg"
ext: str = ".cif"


startOfData: int = 0;
with open(inputFileName + ext, "r") as cif_file:
    line: str = cif_file.readline()
    lineNumber: int = 1
    while line:
        if "loop_" in line :
            line = cif_file.readline()
            lineNumber += 1
            
            if "_atom_site_label" in line :
                break;
            if "_symmetry_equiv_pos_as_xyz" in line :
                print("cif file might contain symmetry, this program doesn't handle that yet")
            continue;
        
        line = cif_file.readline()
        lineNumber += 1
    
    

    count: int = 0
    while "_" in line:
        Atom.legend[count] = line
        Atom.reverseLegend[line] = count
        count += 1
        line = cif_file.readline()
        lineNumber += 1
    
    count = 0;
    startOfData = lineNumber;
    print("Loading data as:")
    while "." in line:
        words = line.split()
        atomsList.append(Atom());
        atomsList[count].data_vals = words;
        print(atomsList[count].data_vals)
        count += 1
        line = cif_file.readline()
        lineNumber += 1

print("Finished loading data")


symmetryEqPoints: List[Atom] = []
for i in range(2):
    for j in range(2):
        for k in range(2):
            tempAtom: Atom = Atom()
            tempAtom.setXYZ(i,j,k)
            symmetryEqPoints.append(tempAtom)

def symmetricallyEqAtoms(atom: Atom) -> List[Atom] :
    tempSet = set()
    for symAtom in symmetryEqPoints:
        tempAtom = copy.deepcopy(atom)
        tempAtom = tempAtom + symAtom
        tempAtom.normalize()
        tempSet.add(tempAtom)
    return tempSet



with open(inputFileName + ext, "r") as cif_file:
    nonDataList = list(islice(cif_file, startOfData - 1))



output_folder_name: str = "output/"

try:
    os.mkdir(output_folder_name);
except FileExistsError: 
    print("/output folder already exits, using that")
steps: int = int(input("Number of steps:"))

for i in range(steps) :
    atomsList[0].slerp(steps, i)

sym_adap_atom_list = []

for atom in atomsList:
    sym_adap_atom_list += symmetricallyEqAtoms(atom)


for i in range(steps+1) :
    with open(output_folder_name + inputFileName + ("%02d" % (i,)) + ext, "w") as out_file:
        out_file.writelines(nonDataList)
        for atom in sym_adap_atom_list:

            out_file.write(" ".join(str(x) for x in atom.slerp(steps, i).data_vals) + "\n")
