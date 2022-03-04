import math
import numpy as np
import matplotlib as plt

# Coordinate 2d acqua
O = np.array([2,0,3])
H1 = np.array([1,0,1])
H2 = np.array([3,0,1])
# Array legami
d_OH1 = H1 - O
d_OH2 = H2 - O
# Vettore totale acqua
v_H2O = d_OH1 + d_OH2
#Normalizzazione vettore acqua
norma_v_H2O = math.sqrt(v_H2O[0]**2 + v_H2O[1]**2 + v_H2O[2]**2)
v_H2O_normalized = [v_H2O[0]/norma_v_H2O,v_H2O[1]/norma_v_H2O,v_H2O[2]/norma_v_H2O]
#Dichiarazione Normale a superficie
if O[2]>0:
    normale = [0,0,1]
elif O[2]<0:
    normale = [0,0,-1]
#coseno angolo tra i due vettori
prodotto_scalare_vettori = (v_H2O_normalized[0]*normale[0]) + (v_H2O_normalized[1]*normale[1]) + (v_H2O_normalized[2]*normale[2])
norma_v_H2O_normalized = math.sqrt(v_H2O_normalized[0]**2 + v_H2O_normalized[1]**2 + v_H2O_normalized[2]**2)
norma_normale = math.sqrt(normale[0]**2 + normale[1]**2 + normale[2]**2)
prodotto_norme = norma_v_H2O_normalized*norma_normale
coseno_angolo = prodotto_scalare_vettori/prodotto_norme
#Ottengo angolo in radianti
angolo = math.acos(coseno_angolo)
#Converto in gradi
angolo_gradi = math.degrees(angolo)
print(list(d_OH1))
print(list(d_OH2))
print(list(v_H2O))
print(list(v_H2O_normalized))
print(prodotto_scalare_vettori)
print(norma_v_H2O_normalized)
print(norma_normale)
print(coseno_angolo)
print(angolo)
print(angolo_gradi)