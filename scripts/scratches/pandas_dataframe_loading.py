import numpy as np
import pandas as pd
import timeit


numero_di_frame = 3000
path = "C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Dati\\Test\\CarboneGiorgio.pdb"
#Create le colonne del dataframe ottenuto dal file .pdb
colonne_nomi=np.array(["0","1","2","3","4","x","y","z"])
#L'intero file .pdb viene estratto e inserito in un dataframe, come delimiter gli spazi, come colonne i nomi
#Scritti precedentemente, nessuna compressione dei dati
dataframe = pd.read_csv(path, delim_whitespace=True, names=colonne_nomi,low_memory=False)
#print(dataframe.head(40)) #printa le prime 40 righe
colonne_elemento_e_coordinate = ["2","x","y","z"]
# to_numeric() rende float i numeri della colonna "1", .apply() applica la modifica al dataframe copia su cui sto agendo, devo eguagliare infine il database originale al database copia
dataframe.loc[1:,"1"] = dataframe.loc[1:,"1"].apply(pd.to_numeric,errors='coerce')
# trovo le posizioni dei model successivi a 1 e le unisco alla posizione di model 1 specificata a mano
posizione_model = np.append([0],np.where(dataframe.loc[1:,"1"]>1))
# correggo la posizione essendo che parte da 1 nel data.loc(), ottengo la posizione dei model nel dataframe
posizione_model += 1
for count in range(0,numero_di_frame):
    if count != 2999:
        # counter per il fine frame
        count1 = count + 1
        # Seleziono dati, saranno selezionati i dati dalla posizione del model del frame + 1(non si seleziona "model" nei dati)
        # alla posizione del model successivo - 2 (non si seleziona "model" e "endmodel"
        # le colonne sono quelle delle coordinate ma anche quella dell'elemento
        data = dataframe.loc[(posizione_model[count]+1):(posizione_model[count1]-2),colonne_elemento_e_coordinate].copy(deep=True)
    else:
        # nel caso siamo all'ultimo frame, non si può usare come delimitatore il model del frame successivo
        # quindi semplicemente gli dico di saltare le ultime due righe(uso iloc per questo, .loc non può farlo)
        # non serve neanche il count per trovare il model 3000(so che sarà l'ultimo quindi -1)
        # le colonne vanno indicate con numeri essendo iloc
        data = dataframe.iloc[(posizione_model[-1]+1):-2,[2,5,6,7]].copy(deep=True)
    data.reset_index(drop=True, inplace=True)
    # Vado a creare un np.array() contenente solo gli atomi di ossigeno, semplicemente usando una selezione
    # Che salta 2 righe ogni volta che deve prendere un elemento(le due righe degli idrogeni),
    # Il primo : indica di selezionare dall'intero data, il :3 indica che va preso 1 dato su tre
    data_solo_ossigeno = data.loc[::3,["x","y","z"]].to_numpy()
    print(data_solo_ossigeno)

