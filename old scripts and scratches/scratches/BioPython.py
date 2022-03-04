from Bio.PDB import *

path = "C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Dati\\Test\\BioPython\\Replica1_7.750matm_300+300Msteps_SoloOssigeno.pdb"
parser = PDBParser()
structure = parser.get_structure('Ossigeni', path)
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print(atom.get_coord())

#Stampa solamente la prima riga(boh)
