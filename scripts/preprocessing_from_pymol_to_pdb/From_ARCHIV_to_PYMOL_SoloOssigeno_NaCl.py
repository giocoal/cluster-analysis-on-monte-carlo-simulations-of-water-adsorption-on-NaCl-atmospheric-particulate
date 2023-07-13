#!/usr/bin/env python
import fileinput
import os

print('This program uses as an input a HISTORY.000 file in DL_MONTE format, the Title line of which starts with MgO, and the atom types of which are Mg, O, Oa, and H. If one wants to make the program put in the pdb the correct progressive number of atoms, one has to substitute the 1 number with altrecolonne in each occurrence of the pdb.write command below; notice that in that case when the progressive atome number goes equal or above 6 digits, the atom coordinates column in the pdb are shifted by one (or more, in case of 7 or more digits) positions, in such a way that pymol cannot read well the output pdb file anymore. In that case, one needs to manually remove one or more empti column(s) in the pdb, starting from the line in which such shifting occurs')

def getSize(inputFile):
    size = os.path.getsize('HISTORY.000')
    print(size)
    return size

def trimFile(inputFile):
    size = getSize(inputFile)
    if size >= 700000000000:
        inputFile.readlines()
        offset = size - 700000000000
        inputFile.seek(offset)
        print(inputFile.readline())
    else:
        return inputFile
    
inputmmc = open('HISTORY.000', "r")

trimFile(inputmmc)
linesCounter = 0

LINESinput = inputmmc.readlines()

for line in LINESinput:
    if line[0:3] == 'Tit':
        break
    linesCounter += 1

LISTApointer = []

for i in range(len(LINESinput)):

    if LINESinput[i][0:3] == 'Tit':
        pointer = i
        LISTApointer.append(pointer)
#    else:
#        print('HAI MODIFICATO IL PROGRAMMA INSERENDO IL TITOLO E LO SPAZIO RECIPROCO GIUSTI?')
#        continue
LineePerPDB = []

Xreciproco = 1.00000 
Yreciproco = 1.00000
Zreciproco = 1.00000


pdb = open("Replica2_7.875matm_300Msteps.pdb", "w")
pdb.write('REMARK ')

progress = 1
altrecolonne = 1
numeratorealtrecolonne=1

pdb.write("%s\n" % ('MODEL 1'))

print(linesCounter)
print(len(LINESinput))

PosizioniNa = []
PosizioniHa = []
PosizioniNn = []
PosizioniOn = []
Posizioniow = []
Posizionihw = []




for i in range(linesCounter, len(LINESinput)):
    
#    if LINESinput[i][0:3] == 'MgO':
        
#        LineePerPDB.append('MODEL')
#        pdb.write("%s %5.0f\n" % ('MODEL', progress))
#        progress = progress +1
    if LINESinput[i][0:3] == 'Tit':
        LineePerPDB.append('MODEL')
	if i != linesCounter:
		pdb.write("%s\n" % ('ENDMDL'))
        pdb.write("%s %5.0f\n" % ('MODEL', progress))
        progress = progress +1    
#    if LINESinput[i][0:3] == ' na' :
#        LineePerPDB.append(LINESinput[i+1])
#        SplitNa = LINESinput[i+1].split()
#        pdb.write("%s %5.0f %11.3f %7.3f %7.3f\n" % ('ATOM      1 NA   SLT',            1, float(SplitNa[0])/Xreciproco, float(SplitNa[1])/Yreciproco, float(SplitNa[2])/Zreciproco))
#        TreCoordinateMg = [float(SplitNa[0])/Xreciproco, float(SplitNa[1])/Yreciproco, float(SplitNa[2])/Zreciproco]
#	PosizioniNa.append(TreCoordinateMg)
	altrecolonne = altrecolonne +1
        #print(SplitMg)
#        pdb.write("%s\n" % ('TER'))
#    if LINESinput[i][0:3] == ' cl' :
#        LineePerPDB.append(LINESinput[i+1])
#        SplitCl = LINESinput[i+1].split()
#        pdb.write("%s %5.0f %11.3f %7.3f %7.3f\n" % ('ATOM      1 CL   SLT',            1, float(SplitCl[0])/Xreciproco, float(SplitCl[1])/Yreciproco, float(SplitCl[2])/Zreciproco))
#        TreCoordinateO = [float(SplitCl[0])/Xreciproco, float(SplitCl[1])/Yreciproco, float(SplitCl[2])/Zreciproco] 
#	PosizioniHa.append(TreCoordinateO)
        altrecolonne = altrecolonne +1
        #print(SplitO)
#        pdb.write("%s\n" % ('TER'))
#    if LINESinput[i][0:3] == ' nx' :
#        LineePerPDB.append(LINESinput[i+1])
#        SplitCl = LINESinput[i+1].split()
#        pdb.write("%s %5.0f %11.3f %7.3f %7.3f\n" % ('ATOM      1 NX   SLT',            1, float(SplitCl[0])/Xreciproco, float(SplitCl[1])/Yreciproco, float(SplitCl[2])/Zreciproco))
#        TreCoordinateO = [float(SplitCl[0])/Xreciproco, float(SplitCl[1])/Yreciproco, float(SplitCl[2])/Zreciproco]
#        PosizioniNn.append(TreCoordinateO)
        altrecolonne = altrecolonne +1
        #print(SplitO)
#        pdb.write("%s\n" % ('TER'))
#    if LINESinput[i][0:3] == ' cx' :
#        LineePerPDB.append(LINESinput[i+1])
#        SplitCl = LINESinput[i+1].split()
#        pdb.write("%s %5.0f %11.3f %7.3f %7.3f\n" % ('ATOM      1 CX   SLT',            1, float(SplitCl[0])/Xreciproco, float(SplitCl[1])/Yreciproco, float(SplitCl[2])/Zreciproco))
#        TreCoordinateO = [float(SplitCl[0])/Xreciproco, float(SplitCl[1])/Yreciproco, float(SplitCl[2])/Zreciproco]
#        PosizioniOn.append(TreCoordinateO)
        altrecolonne = altrecolonne +1
        #print(SplitO)
#        pdb.write("%s\n" % ('TER'))
    if LINESinput[i][0:3] == ' ow' :
        LineePerPDB.append(LINESinput[i+1])
        SplitOa = LINESinput[i+1].split()
        pdb.write("%s %5.0f %11.3f %7.3f %7.3f\n" % ('ATOM      1 OW   ACQ',            1, float(SplitOa[0])/Xreciproco, float(SplitOa[1])/Yreciproco, float(SplitOa[2])/Zreciproco))
        TreCoordinateOa = [float(SplitOa[0])/Xreciproco, float(SplitOa[1])/Yreciproco, float(SplitOa[2])/Zreciproco]
        Posizioniow.append(TreCoordinateOa)
	numeratorealtrecolonne=numeratorealtrecolonne+1
	if numeratorealtrecolonne == 4 :
		altrecolonne = altrecolonne +1
		numeratorealtrecolonne=1
        #print(SplitOm)        
#    if LINESinput[i][0:3] == ' hw' :
#        LineePerPDB.append(LINESinput[i+1])
#        SplitH  = LINESinput[i+1].split()
#        pdb.write("%s %5.0f %11.3f %7.3f %7.3f\n" % ('ATOM      1 HW   ACQ',            1, float(SplitH[0])/Xreciproco, float(SplitH[1])/Yreciproco, float(SplitH[2])/Zreciproco))
#        TreCoordinateH = [float(SplitH[0])/Xreciproco, float(SplitH[1])/Yreciproco, float(SplitH[2])/Zreciproco]
#        Posizionihw.append(TreCoordinateH)
#        numeratorealtrecolonne=numeratorealtrecolonne+1
#        if numeratorealtrecolonne == 4 :
#		altrecolonne = altrecolonne +1
#		numeratorealtrecolonne=1


pdb.write("%s\n" % ('ENDMDL'))
pdb.write('END')

#pdb.close

#print PosizioniMg[0:256]


#print('Distanze tra Mg ed O della acqua sotto una certa soglia')

#for u in range(len(PosizioniMg[0:256])):
#    for d in range(len(PosizioniOa)):
#	if (((PosizioniMg[u][0]-PosizioniOa[d][0])**2 + (PosizioniMg[u][1]-PosizioniOa[d][1])**2 + (PosizioniMg[u][2]-PosizioniOa[d][2])**2)**(1./2.)) < 1.94:
#        	print(((PosizioniMg[u][0] - PosizioniOa[d][0])**2 + (PosizioniMg[u][1] - PosizioniOa[d][1])**2 + (PosizioniMg[u][2] - PosizioniOa[d][2])**2)**(1./2.))



#print('Distanze tra Mg ed H della acqua sotto una certa soglia')

#for u in range(len(PosizioniMg[0:256])):
#    for d in range(len(PosizioniH)):
#        if (((PosizioniMg[u][0]-PosizioniH[d][0])**2 + (PosizioniMg[u][1]-PosizioniH[d][1])**2 + (PosizioniMg[u][2]-PosizioniH[d][2])**2)**(1./2.)) < 1.92:
#                print(((PosizioniMg[u][0] - PosizioniH[d][0])**2 + (PosizioniMg[u][1] - PosizioniH[d][1])**2 + (PosizioniMg[u][2] - PosizioniH[d][2])**2)**(1./2.))



#print('Distanze tra Ossigeni del solido ed O della acqua sotto una certa soglia')

#for u in range(len(PosizioniO[0:256])):
#    for d in range(len(PosizioniOa)):
#        if (((PosizioniO[u][0]-PosizioniOa[d][0])**2 + (PosizioniO[u][1]-PosizioniOa[d][1])**2 + (PosizioniO[u][2]-PosizioniOa[d][2])**2)**(1./2.)) < 2.5:
#                print(((PosizioniO[u][0] - PosizioniOa[d][0])**2 + (PosizioniO[u][1] - PosizioniOa[d][1])**2 + (PosizioniO[u][2] - PosizioniOa[d][2])**2)**(1./2.))

#print('Distanze tra Ossigeni del solido ed H della acqua sotto una certa soglia')

#for u in range(len(PosizioniO[0:256])):
#    for d in range(len(PosizioniH)):
#        if (((PosizioniO[u][0]-PosizioniH[d][0])**2 + (PosizioniO[u][1]-PosizioniH[d][1])**2 + (PosizioniO[u][2]-PosizioniH[d][2])**2)**(1./2.)) < 1.75:
#                print(((PosizioniO[u][0] - PosizioniH[d][0])**2 + (PosizioniO[u][1] - PosizioniH[d][1])**2 + (PosizioniO[u][2] - PosizioniH[d][2])**2)**(1./2.))




#    PosizioniMg = []
#    PosizioniO = []
#    PosizioniOa = []
#    PosizioniH = []	

        

#print(PosizioniMg[0:3])
#print(LineePerPDB)


#        Superstringa1.append(SodioStringheXYZ)
#        Superstringa1.append(CloroStringheXYZ)
#        Superstringa1.append(AcqueStringheXYZohh)
#print(SuperstringaFinale)

#print(AcqueStringheXYZohh[0].split())



#pdb = open("pdb_FROM-DLMONTE", "w")

#pdb.write('REMARK\n')

#for t in len(numerocicli):
#    for w in range(LISTApointer[w], LISTApointer[w+1]):
#for i in range(len(SodioStringheXYZ)):
#    SplitNa = SodioStringheXYZ[i].split()
#    pdb.write("%s %11.3f %7.3f %7.3f\n" % ('ATOM      1 NA   SLT A   1', float(SplitNa[0]), float(SplitNa[1]), float(SplitNa[2])))
#for i in range(len(CloroStringheXYZ)):
#    SplitCl = CloroStringheXYZ[i].split()
#    pdb.write("%s %11.3f %7.3f %7.3f\n" % ('ATOM      1 CL   SLT A   1', float(SplitCl[0]), float(SplitCl[1]), float(SplitCl[2])))
#pdb.write('END')

#pdb.close                                                                                                                                     



######### cancellare qua sotto #########

#pdb = open("pdb_FROM-DLMONTE", "w")
#pdb.write('REMARK\n')
#for i in range(len(SodioStringheXYZ)):
#    SplitNa = SodioStringheXYZ[i].split()
#    pdb.write("%s %11.3f %7.3f %7.3f\n" % ('ATOM      1 NA   SLT A   1', float(SplitNa[0]), float(SplitNa[1]), float(SplitNa[2])))
#for i in range(len(CloroStringheXYZ)):
#    SplitCl = CloroStringheXYZ[i].split()
#    pdb.write("%s %11.3f %7.3f %7.3f\n" % ('ATOM      1 CL   SLT A   1', float(SplitCl[0]), float(SplitCl[1]), float(SplitCl[2])))
#pdb.write('END')
#pdb.close                                                                                                                                     



#print(toBeRemoved)

#print(len(alldistances))
#for i in range(len(LINESinput)):
#    if LINESinput[i][0] == 'S':
#        if LINESinput[i][1] == 'L':
#            header = i
#            numberlines = LINESinput[i].split()
#            poscoord = int(numberlines[4])


#fo = open("HISTORY_FROM-DLMONTE", "w")
#fo.writelines(LINESinput[0])

#for i in range(len(toBeRemoved)):
#    fo.write("%s" % (toBeRemoved[i]))

#for i in range(int(numberlines[4])):
#    fo.write("%s %7.3f %s" % (StringsBeforeZ[i], NewPositionsAlongZ[i], StringsAfterZ[i]))

#fo.writelines(LINESinput[header+1+poscoord:])

#fo.close()

