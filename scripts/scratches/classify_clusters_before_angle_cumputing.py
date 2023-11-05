import numpy as np
import math
#Converte gli indici degli ossigeni nell'array contenente le coordinate dei soli ossigeni negli indici degli ossigeni
#Nell'array contenente le coordinate di O e H, ricava poi gli indici degli idrogeni da esse
def nuovi_indici(vecchi_indici):
    indici_o_nuovi = np.array(vecchi_indici + (vecchi_indici*2))
    indici_h1_nuovi = np.array(indici_o_nuovi + 1)
    indici_h2_nuovi = np.array(indici_o_nuovi + 2)
    return indici_o_nuovi,indici_h1_nuovi,indici_h2_nuovi

def calcolo_angoli(dataset,indici_O,indici_H1,indici_H2):
    angoli = np.array([])
    for count_angoli in range(0,len(indici_O)):
        # Coordinate 3D acqua
        O = dataset[(indici_O[count_angoli]),:]
        H1 = dataset[(indici_H1[count_angoli]),:]
        H2 = dataset[(indici_H2[count_angoli]),:]
        # Array legami
        d_OH1 = H1 - O
        d_OH2 = H2 - O
        # Vettore totale acqua
        v_H2O = d_OH1 + d_OH2
        # Normalizzazione vettore acqua
        norma_v_H2O = math.sqrt(v_H2O[0] ** 2 + v_H2O[1] ** 2 + v_H2O[2] ** 2)
        v_H2O_normalized = [v_H2O[0] / norma_v_H2O, v_H2O[1] / norma_v_H2O, v_H2O[2] / norma_v_H2O]
        # Dichiarazione Normale a superficie
        if O[2] > 0:
            normale = [0, 0, 1]
        elif O[2] < 0:
            normale = [0, 0, -1]
        # coseno angolo tra i due vettori
        prodotto_scalare_vettori = (v_H2O_normalized[0] * normale[0]) + (v_H2O_normalized[1] * normale[1]) + (
                    v_H2O_normalized[2] * normale[2])
        norma_v_H2O_normalized = math.sqrt(
            v_H2O_normalized[0] ** 2 + v_H2O_normalized[1] ** 2 + v_H2O_normalized[2] ** 2)
        norma_normale = math.sqrt(normale[0] ** 2 + normale[1] ** 2 + normale[2] ** 2)
        prodotto_norme = norma_v_H2O_normalized * norma_normale
        coseno_angolo = prodotto_scalare_vettori / prodotto_norme
        # Ottengo angolo in radianti
        angolo = math.acos(coseno_angolo)
        # Converto in gradi
        angolo_gradi = math.degrees(angolo)
        #Aggiungo le molecole al database
        angoli = np.append(angoli,angolo_gradi)
    return angoli

labels = np.array([-1,1,2,3,4,1,-1,1,2,3,2,3,4,3,2,1,3,1,0,0,-1,1,2,3,4,1,-1,1,2,3,2,3,4,3,2,1,3,1,0,0,-1,1,2,3,4,1,-1,1
                      ,2,3,2,3,4,3,2,1,3,1,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2])
n_elements_clusters_temp = np.bincount(labels[labels >= 0])
#Vado a individuare gli indici dei n_el maggiori di 70 (nell'esempio 30, da cambiare !!!!!!)
#Gli indici corrisponderanno alla label di quel cluster
labels_delle_isole = np.where(n_elements_clusters_temp < 30)
labels_dei_layer = np.where(n_elements_clusters_temp >= 30)
label_rumore = -1
# Ora conosco quali labels sono associati a clusters di isole, quali layers e che -1 è per il rumore
# Ora vado as suddividere gli ossigeni(coordinate) in questi 3 gruppi in questo modo:
# individuo l'indice in labels(il quale è identico all'indice della riga nel dataset) degli ossigeni che appartengono
# alle isole, quelli dei layer e quelli dei monolayer, di fatto quindi ora so quali coordinate usare per trovare gli
# angoli_isole, angoli_layer, angoli_rumore

# Per fare questo uso where su labels, andando a trovare quali elementi di labels sono uguali alle labels che si
# sono dimostrate essere associate ad isole
"""Devo trovare l'indice ,in labels,degli elementi uguali alle labels indicate come labels_delle_isole,
fare però np.where(label = labels_delle_isole) non si può fare, si può infatti uguagliare
ad un solo valore oppure a più valori usando &, per ovviare al problema, se voglio uguagliare
a più valori, prendendoli da un array, uso np.in1d come visto sotto"""
indici_ossigeno_isole_in_solo_ox = np.where(np.in1d(labels, labels_delle_isole))
indici_ossigeno_layers_in_solo_ox = np.where(np.in1d(labels, labels_dei_layer))
indici_ossigeno_rumore_in_solo_ox = np.where(labels == -1)
print(indici_ossigeno_isole_in_solo_ox[0])
# Ora conosco, per ogni ossigeno(indice), se appartiene ad un'isola,un layer o è parte del rumore

# Ottengo, per questi tre gruppi, gli indici degli ossigeni nel database contenente anche gli idrogeni
# E da questi ottengo per somma di 1/2 righe gli indici di H1 e H2, ottengo 3 array,
# Rispettivamente per O,H1,H2 - Riconosco gli elementi appartenenti alla stessa molecola perchè avranno uguale indice
# Nei 3 array
"""ISOLE"""
indici_ossigeno_isole, indici_idrogeno1_isole, indici_idrogeno2_isole = nuovi_indici(indici_ossigeno_isole_in_solo_ox[0])
"""LAYERS"""
indici_ossigeno_layers, indici_idrogeno1_layers, indici_idrogeno2_layers = nuovi_indici(indici_ossigeno_layers_in_solo_ox[0])
"""RUMORE"""
indici_ossigeno_rumore, indici_idrogeno1_rumore, indici_idrogeno2_rumore = nuovi_indici(indici_ossigeno_rumore_in_solo_ox[0])
print(indici_ossigeno_isole)
print(len(indici_ossigeno_isole))

