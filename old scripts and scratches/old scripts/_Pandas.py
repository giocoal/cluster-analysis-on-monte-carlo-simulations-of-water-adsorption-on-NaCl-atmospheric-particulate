import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform
import csv
import os
import pandas

# COSTANTI FONDAMENTALI
path_cartella = 'C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Dati\\Solo_Ossigeni\\Tutte_Repliche' #cartella contenente i files.pdb
path_output = "C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Risultati\\analisi_completa.txt"
numero_di_frame = 3000 #numero di frame da analizzare per ogni file

# *** FUNZIONI ***
def periodicita(L = 39.606): #L larghezza della scatola
    total = 0
    for d in range(data.shape[1]):
        pd = pdist(data[:, d].reshape(-1, 1))
        if (d != 2):
            pd[pd > (0.5 * L)] -= L
        total += pd ** 2

    total = np.sqrt(total)
    square = squareform(total)
    return square

def outofbox():
    # TEST PER VALORI DI |X,Y| MAGGIORI DI 19.803 - OVVERO L/2
    data[:,:2] = np.where((data[:,:2]>19.803) & (((data[:,:2]//19.803)%2) == 1), (-(19.803) + (data[:,:2]%19.803)), data[:,:2])
    data[:, :2] = np.where((data[:, :2] > 19.803) & (((data[:, :2] // 19.803) % 2) == 0), data[:, :2] % 19.803, data[:, :2])
    # test per valori di x,y minori di -20
    data[:, :2] = np.where((data[:, :2] < (-19.803)) & (((data[:, :2] // (-19.803)) % 2) == 1),
                           [+19.803 + (data[:, :2] % (-19.803))], data[:, :2])
    data[:, :2] = np.where((data[:, :2] < (-19.803)) & (((data[:, :2] // (-19.803)) % 2) == 0), data[:, :2] % (-19.803),
                           data[:, :2])
    return data

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

    return n_elements_clusters

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
count = 1
numero_di_frame_maggiorato = numero_di_frame + 1
n_isole_database = np.array([]) #array mono-dimensionale che contiene il numero di cluster per tutti i 3000 frame
n_elements_isole_database = np.array([])  #array mono-dimensionale che contiene il numero di elementi di clusters per ogni frame
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
        numero_di_linee_totali = file_len(path) #lunghezza (numero di linee) del file nel path

    # *** CICLO FOR: carica progressivamente i frame e poi .append il valore di n_clusters e count(numero di elementi nei clusters) agli array che poi subiranno la media e la std ***

        for count in range(1,numero_di_frame_maggiorato):            #devo trovare il numero di MODEL, il range superiore è il NUMERO TOTALE DI FRAME+1
            if count < 9:
                inizio_frame = "MODEL     " + str(count)
                print("Elaborando il Frame n° " + str(count) + "/3000")
                count += 1
                fine_frame = "MODEL     " + str(count)
            elif count == 9 :
                inizio_frame = "MODEL     " + str(count)
                print("Elaborando il Frame n° " + str(count) + "/3000")
                count += 1
                fine_frame = "MODEL    " + str(count)
            elif count < 99:
                inizio_frame = "MODEL    " + str(count)
                print("Elaborando il Frame n° " + str(count) + "/3000")
                count += 1
                fine_frame = "MODEL    " + str(count)
            elif count == 99:
                inizio_frame = "MODEL    " + str(count)
                print("Elaborando il Frame n° " + str(count) + "/3000")
                count += 1
                fine_frame = "MODEL   " + str(count)
            elif count < 999:
                inizio_frame = "MODEL   " + str(count)
                print("Elaborando il Frame n° " + str(count) + "/3000")
                count += 1
                fine_frame = "MODEL   " + str(count)
            elif count == 999:
                inizio_frame = "MODEL   " + str(count)
                print("Elaborando il Frame n° " + str(count) + "/3000")
                count += 1
                fine_frame = "MODEL  " + str(count)
            else:
                inizio_frame = "MODEL  " + str(count)
                print("Elaborando il Frame n° " + str(count) + "/3000")
                count += 1
                fine_frame = "MODEL  " + str(count)

            if inizio_frame != ("MODEL  3000"):                                  # + str(numero_di_frame)): momentaneamente messo costante
                skip_header_ = trova_linea(inizio_frame,path) + 1           #+1 la linea di testa è la 0
                skip_footer_ = numero_di_linee_totali - (trova_linea(fine_frame,path)) + 1 #+1 è dovuto alla presenza di ENDMDL da skippare
                data = pandas.read_csv(path, skiprows=skip_header_, skipfooter=skip_footer_,delim_whitespace=True,usecols=(5,6,7),header=None, engine='python')
                data = data.to_numpy()
                #print(data)

            else:
                skip_header_ = trova_linea(inizio_frame,path) + 1
                skip_footer_ = 2  # se il frame è l'ultimo vado a skippare le ultime due righe ovvero ENDMDL e END
                data = pandas.read_csv(path, skiprows=skip_header_, skipfooter=skip_footer_,delim_whitespace=True,usecols=(5,6,7),header=None, engine='python')
                data = data.to_numpy()
                #print(data)
            outofbox()
            n_elements_clusters_temp = clusterizzazione() #variabi temporanee da mergiare agli array totali
            """SPLITTA I DATI IN ISOLE E CLUSTERS"""
            n_elements_isole_temp, n_elements_monolayers_temp = splitta(n_elements_clusters_temp)
            n_monolayers_temp = len(n_elements_monolayers_temp)
            n_isole_temp = len(n_elements_isole_temp)
            """UNISCE I TEMP AI DATABASE (numero di clusters)"""
            n_isole_database = np.append(n_isole_database, n_isole_temp)  # .append permette di unire array con diverso numero di colonne (diverso numero di clusters in diversi frame) in un unico array 1-D
            n_monolayers_database = np.append(n_monolayers_database, n_monolayers_temp)
            """UNISCE I TEMP AI DATABASE (numero di elementi)"""
            n_elements_isole_database = np.append(n_elements_isole_database, n_elements_isole_temp)
            n_elements_monolayers_database = np.append(n_elements_monolayers_database, n_elements_monolayers_temp)
            #print(n_clusters_database)            # COSA BUONA: se ci sono 0 cluster viene registrato 0 (deve fare media)
            #print(n_elements_clusters_database)   # se non ci sono cluster non viene registrato un valore di numero di elementi(GIUSTO: non deve fare media)

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