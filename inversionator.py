#CIF_inverter
#site: https://github.com/Ash-Pera/CIF_inverter
#written by Ash Pera

import CifFile as cf
from typing import Dict, Tuple, List
import os

#inputFileName: str = input(".cif file name:")
inputFileName = "other_PZT.cif"
inFile = cf.ReadCif(inputFileName)

inputFileName = inputFileName[0:-4]

#probably only one, right?
dataBlock = inFile[inFile.keys()[0]]

from Atom import Atom



atomSpecs = []

for key in dataBlock.keys():
    if "atom" in key:
        atomSpecs.append(key)
        Atom.reverseLegend[key] = len(Atom.reverseLegend)

numAtoms = len(dataBlock[atomSpecs[0]])

atomList = []

for i in range(numAtoms):
    atom = Atom()
    for spec in atomSpecs:
        atom[spec] = dataBlock[spec][i]
    atomList.append(atom)

print("Loaded atoms as:\n" + str(atomList))
print("\n\n\n")

symAtomList = []
for atom in atomList:
    symAtomList.extend(atom.cell_edge_copies())

print("Copied atoms to unit cell boundries:\n" + str(symAtomList))



def atom_list_to_dic_list(atomList: List[Atom]) -> Dict[str, List[str]] :
    outputDict: Dict(str, List[str]) = dict()
    for key in atomSpecs:
        outputDict[key] = []

    for atom in atomList:
        for key,val in atom.data_vals.items():
            outputDict[key].append(val)
    return outputDict
        
def lerp_invert_atoms(atomList: List[Atom], num_steps:int, current_step:int) -> List[Atom] :
    newAtomList = []
    for atom in atomList:
        newAtomList.append(atom.lerp_to_inversion(num_steps,current_step))
    return newAtomList


number_of_steps = int(input("number of steps:"))

try:
    os.mkdir("output/");
except FileExistsError: 
    print("/output folder already exits, using that")

for i in range(number_of_steps+1):
    newData: Dict[str, List[str]] = atom_list_to_dic_list(lerp_invert_atoms(symAtomList, number_of_steps, i))

    for key, dataList in newData.items():
        dataBlock[key] = dataList

    with open("output/" + inputFileName + str(i) + ".cif", "w") as out_file :
        out_file.write(str(inFile))
    #print("Saved file #" + str(i))
