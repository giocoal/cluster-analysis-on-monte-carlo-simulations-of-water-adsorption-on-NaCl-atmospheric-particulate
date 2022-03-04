import numpy as np

lista_liste_angoli = []

for i in np.arange(6.5,25.5,0.5):
    lista_liste_angoli.append([])

angoli_isole_distanza_database = np.array(lista_liste_angoli)
angoli_layers_distanza_database = np.array(lista_liste_angoli)
angoli_rumore_distanza_database = np.array(lista_liste_angoli)

test = np.array([[float('nan'),float('nan'),float('nan')],[float('nan'),1,2]])
print(len(test[1]))
print(np.size(test[1]) - np.count_nonzero(np.isnan(test[1])))
print((np.isnan(test[1]).sum()))
if np.isnan(test[0]).all() != False: print("diocan")

