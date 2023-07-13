import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform
import csv
import os
import pandas as pd
import timeit

start = timeit.default_timer()
# COSTANTI FONDAMENTALI
cartella_e_nome_output = "2_300+300Ms_Parte2"
path_cartella = 'C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Dati\\Solo_Ossigeni\\Repliche_Divise\\' + cartella_e_nome_output #cartella contenente i files.pdb
path_output = "C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Risultati\\Test_Pandas\\" + cartella_e_nome_output + ".txt"
numero_di_frame = 3000 #numero di frame da analizzare per ogni file

# *** FUNZIONI ***
def periodicita(L = 39.606): #L larghezza della scatola
    total = 0
    for d in range(data_solo_ossigeno.shape[1]):
        pd = pdist(data_solo_ossigeno[:, d].reshape(-1, 1))
        if (d != 2):
            pd[pd > (0.5 * L)] -= L
        total += pd ** 2

    total = np.sqrt(total)
    square = squareform(total)
    return square

def outofbox():
    # TEST PER VALORI DI |X,Y| MAGGIORI DI 19.803 - OVVERO L/2
    data_solo_ossigeno[:, :2] = np.where((data_solo_ossigeno[:, :2] > 19.803) & (((data_solo_ossigeno[:, :2] // 19.803) % 2) == 1), (-(19.803) + (data_solo_ossigeno[:, :2] % 19.803)), data_solo_ossigeno[:, :2])
    data_solo_ossigeno[:, :2] = np.where((data_solo_ossigeno[:, :2] > 19.803) & (((data_solo_ossigeno[:, :2] // 19.803) % 2) == 0), data_solo_ossigeno[:, :2] % 19.803, data_solo_ossigeno[:, :2])
    # test per valori di x,y minori di -20
    data_solo_ossigeno[:, :2] = np.where((data_solo_ossigeno[:, :2] < (-19.803)) & (((data_solo_ossigeno[:, :2] // (-19.803)) % 2) == 1),
                                         [+19.803 + (data_solo_ossigeno[:, :2] % (-19.803))], data_solo_ossigeno[:, :2])
    data_solo_ossigeno[:, :2] = np.where((data_solo_ossigeno[:, :2] < (-19.803)) & (((data_solo_ossigeno[:, :2] // (-19.803)) % 2) == 0), data_solo_ossigeno[:, :2] % (-19.803),
                                         data_solo_ossigeno[:, :2])
    return data_solo_ossigeno

def clusterizzazione(eps=4, min_samples=3):

    db = DBSCAN(eps,min_samples,metric='precomputed')
    db.fit_predict(periodicita())
    db_labels = db.labels_

    """fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim3d(-19.803, 19.803)
    ax.set_ylim3d(-19.803, 19.803)
    ax.set_zlim3d(-25, +25)
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=db.labels_, s=150)
    ax.view_init(azim=200)
    plt.show()
    plt.close()"""

    #n_clusters_ = len(set(db_labels)) - (1 if -1 in db_labels else 0)
    #n_noise_ = list(db_labels).count(-1) NON SERVE
    n_elements_clusters = np.bincount(db_labels[db_labels >= 0])

    return n_elements_clusters, db_labels

def trova_linea(frase, filename):
    with open(filename, 'r') as f:
        for (i, line) in enumerate(f):
            if frase in line:
                return i
    return -1

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def splitta(database_originale):
    isole = database_originale[database_originale < 70]
    monolayers = database_originale[database_originale >= 70]
    return isole,monolayers



# *** INIZIO CODICE ***
# dichiarazione delle variabili necessarie nel ciclo for:
count = 0
# Definisco le colonne che caratterizzerano i dataframe successivi
colonne_nomi=np.array(["0","1","2","3","4","x","y","z"]) #colonne del dataframe .pdb
colonne_elemento_e_coordinate = ["2","x","y","z"]
n_isole_database = np.array([])
n_elements_isole_database = np.array([])
n_monolayers_database = np.array([])
n_elements_monolayers_database = np.array([])
# APRE FILE DA SCRIVERE
with open(path_output, 'w') as csvfile:
    fieldnames = ['nome_file', 'n_isole_medio', 'n_isole_medio_std_della_media', 'n_elements_isole_medio',
                  'n_elements_isole_medio_std_della_media','n_monolayers_medio', 'n_monolayers_medio_std_della_media',
                  'n_elements_monolayers_medio', 'n_elements_monolayers_medio_std_della_media']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
# CARICAMENTO FILES
    files_pdb = os.listdir(path_cartella)  #crea una lista contenente tutti i nomi dei file
    for x in range(len(files_pdb)):
        path = path_cartella + "\\" + files_pdb[x]
        print(path)
        # L'intero file .pdb viene estratto e inserito in un dataframe, come delimiter gli spazi, come colonne i nomi
        # Scritti precedentemente, nessuna compressione dei dati
        dataframe = pd.read_csv(path, delim_whitespace=True, names=colonne_nomi, low_memory=False)
        # to_numeric() rende float i numeri della colonna "1", .apply() applica la modifica al dataframe copia su cui sto
        # agendo, devo eguagliare infine il database originale al database copia
        dataframe.loc[1:, "1"] = dataframe.loc[1:, "1"].apply(pd.to_numeric, errors='coerce')
        # trovo TUTTE le posizioni dei model successivi a 1 e le unisco alla posizione di model 1 specificata a mano
        posizione_model = np.append([0], np.where(dataframe.loc[1:, "1"] > 1))
        # correggo la posizione essendo che parte da 1 nel data.loc(), ottengo la posizione dei model nel dataframe
        posizione_model += 1
        # lunghezza (numero di linee) del file nel path
        numero_di_linee_totali = file_len(path)
        # AZZERO VARIABILI
        n_isole_database = np.array([])
        n_elements_isole_database = np.array([])
        n_monolayers_database = np.array([])
        n_elements_monolayers_database = np.array([])

        for count in range(0, numero_di_frame):
            print("Elaborando il frame:", count + 1)
            if count != 2999:
                # counter per il fine frame
                count1 = count + 1
                # Seleziono dati, saranno selezionati i dati dalla posizione del model del frame + 1(non si seleziona "model" nei dati)
                # alla posizione del model successivo - 2 (non si seleziona "model" e "endmodel"
                # le colonne sono quelle delle coordinate ma anche quella dell'elemento
                data = dataframe.loc[(posizione_model[count] + 1):(posizione_model[count1] - 2),colonne_elemento_e_coordinate].copy(deep=True)
            else:
                # nel caso siamo all'ultimo frame, non si può usare come delimitatore il model del frame successivo
                # quindi semplicemente gli dico di saltare le ultime due righe(uso iloc per questo, .loc non può farlo)
                # non serve neanche il count per trovare il model 3000(so che sarà l'ultimo quindi -1)
                # le colonne vanno indicate con numeri essendo iloc
                data = dataframe.iloc[(posizione_model[-1] + 1):-2, [2, 5, 6, 7]].copy(deep=True)

            data.reset_index(drop=True, inplace=True)
            data_solo_ossigeno = data.loc[::3, ["x", "y", "z"]].to_numpy()

            if data_solo_ossigeno.size != 3:
                outofbox()
                n_elements_clusters_temp,labels = clusterizzazione()  # variabi temporanee da mergiare agli array totali
                """SPLITTA I DATI IN ISOLE E CLUSTERS"""
                n_elements_isole_temp, n_elements_monolayers_temp = splitta(n_elements_clusters_temp)
                n_monolayers_temp = len(n_elements_monolayers_temp)
                n_isole_temp = len(n_elements_isole_temp)
            else:
                n_monolayers_temp = np.array([0])
                n_isole_temp = np.array([0])
                n_elements_isole_temp = np.array([])
                n_elements_monolayers_temp = np.array([])
            """UNISCE I TEMP AI DATABASE (numero di clusters)"""
            n_isole_database = np.append(n_isole_database, n_isole_temp)  # .append permette di unire array con diverso numero di colonne (diverso numero di clusters in diversi frame) in un unico array 1-D
            n_monolayers_database = np.append(n_monolayers_database, n_monolayers_temp)
            """UNISCE I TEMP AI DATABASE (numero di elementi)"""
            n_elements_isole_database = np.append(n_elements_isole_database, n_elements_isole_temp)
            n_elements_monolayers_database = np.append(n_elements_monolayers_database, n_elements_monolayers_temp)
            #print(n_clusters_database)            # COSA BUONA: se ci sono 0 cluster viene registrato 0 (deve fare media)
            #print(n_elements_clusters_database)   # se non ci sono cluster non viene registrato un valore di numero di elementi(GIUSTO: non deve fare media)

            """STUDIO ANGOLI VETTORE H2O/NORMALE ALLA SUPERFICIE DI NaCl"""


        """ TROVA VALORI MEDI -> OUTPUT  ISOLE """
        n_isole_medio = np.mean(n_isole_database)
        n_isole_medio_std_della_media = np.std(n_isole_database) / ((len(n_isole_database)) ** (0.5))
        #n_isole_medio_std = np.std(n_isole_database)
        if n_elements_isole_database.size != 0:
            n_elements_isole_medio = (np.mean(n_elements_isole_database))
        #n_elements_clusters_medio_std = np.std(n_elements_isole_database)
            n_elements_isole_medio_std_della_media = np.std(n_elements_isole_database) / ((len(n_elements_isole_database)) ** (0.5))
        else:
            n_elements_isole_medio = 0.00
            n_elements_isole_medio_std_della_media = 0.00
        """TROVA VALORI MEDI -> OUTPUT  MONOLAYERS """
        n_monolayers_medio = np.mean(n_monolayers_database)
        #n_clusters_medio_std = np.std(n_isole_database)
        n_monolayers_medio_std_della_media = np.std(n_monolayers_database) / ((len(n_monolayers_database)) ** (0.5))
        if n_elements_monolayers_database.size != 0:
            n_elements_monolayers_medio = (np.mean(n_elements_monolayers_database))
        #n_elements_monolayers_medio_std = np.std(n_elements_isole_database)
            n_elements_monolayers_medio_std_della_media = np.std(n_elements_monolayers_database) / ((len(n_elements_monolayers_database)) ** (0.5))
        else:
            n_elements_monolayers_medio = 0.00
            n_elements_monolayers_medio_std_della_media = 0.00
        # STAMPA UNA RIGA DI OUTPUT
        writer.writerow({'nome_file': files_pdb[x], 'n_isole_medio': "%.2f" %n_isole_medio, 'n_isole_medio_std_della_media': "%.2f" %n_isole_medio_std_della_media,
                        'n_elements_isole_medio': "%.2f" %n_elements_isole_medio, 'n_elements_isole_medio_std_della_media': "%.2f" %n_elements_isole_medio_std_della_media
                        ,'n_monolayers_medio':"%.2f" %n_monolayers_medio, 'n_monolayers_medio_std_della_media':"%.2f" %n_monolayers_medio_std_della_media,
                        'n_elements_monolayers_medio':"%.2f" %n_elements_monolayers_medio, 'n_elements_monolayers_medio_std_della_media':"%.2f" %n_elements_monolayers_medio_std_della_media})
        csvfile.flush() #va a scrivere il txt che altrimenti sarebbe scritto totalmente alla fine

stop = timeit.default_timer()
print('Tempo totale di esecuzione: ', stop - start)