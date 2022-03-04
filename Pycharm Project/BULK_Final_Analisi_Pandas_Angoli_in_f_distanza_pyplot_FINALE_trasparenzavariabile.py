import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform
import csv
import os
import pandas as pd
import timeit
import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import PercentFormatter
import matplotlib.gridspec as gridspec
import matplotlib.colors as colors
from textwrap import wrap
import sys
#matplotlib.use('Qt5Agg')
start = timeit.default_timer()

"IMPOSTAZIONI"
#OPZIONI PRINCIPALI
clusterizzazione_grafico_onoff = "OFF" #fornisce rappresentazione 3D della clusterizzazione
calcolo_angoli_onoff = "ON" #calcola gli angoli delle H2O rispetto alla normale alla superficie di NaCl
funzione_della_distanza_onoff = "ON" #gli angoli vengono calcolati in funzione della distanza dalla superficie
tipo_di_ambiente = "NaCl" #Indica il tipo di ambiente in cui è inserita l'acqua, Parametri possibili: NaCl - BULK
unità_di_misura_angoli = "COSENO" # Parametri possibili: COSENO - GRADI
#OPZIONI SECONDARIE
periodicita_onoff = "ON" #la clusterizzazione tiene conto o meno delle pareti periodiche della scatola
outofbox_onoff = "ON" #reinserisce molecole erroneamente fuori dalla scatola sulla base della periodicità
#PATH INPUT
#All'interno del path_risultati vanno copiate le cartelle standard di output
path_risultati = "C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Risultati\\FINALE\\"
path_dati = 'C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Dati\\'

"IMPOSTAZIONI AUTOMATICHE"
#PATH ADATTIVI
cartella_e_nome_output = "Replica1"
if tipo_di_ambiente == "NaCl":
    path_cartella = path_dati + 'Solo_H2O\\' + cartella_e_nome_output #cartella contenente i files.pdb
if tipo_di_ambiente == "BULK":
    path_cartella = path_dati + 'Bulk\\' + cartella_e_nome_output  # cartella contenente i files.pdb
#PATH OUTPUT
if funzione_della_distanza_onoff == "ON" and calcolo_angoli_onoff == "ON":
    path_output_clusterizzazione = path_risultati + "Clusterizzazione_Angoli_H2O_in_funzione_della_distanza\\Clusterizzazione\\" + cartella_e_nome_output + ".txt"
    path_output_angoli = path_risultati + "Clusterizzazione_Angoli_H2O_in_funzione_della_distanza\\Angoli_Distanza\\" + cartella_e_nome_output + "_angoli_distanza" + ".txt"
    path_output_angoli_stat = path_risultati + "Clusterizzazione_Angoli_H2O_in_funzione_della_distanza\\Angoli_Statistica\\" + cartella_e_nome_output + "_angoli_distanza" + ".txt"
    path_plot_angoli_f_distanza = path_risultati + "Clusterizzazione_Angoli_H2O_in_funzione_della_distanza\\Plot_angoli\\"
    path_istogrammi = path_risultati + "Clusterizzazione_Angoli_H2O_in_funzione_della_distanza\\Angoli_Istogrammi\\"
    path_clusterizzazione_plot = path_risultati + "Clusterizzazione_Angoli_H2O_in_funzione_della_distanza\\Clusterizzazione_plot\\"
    path_impostazioni = path_risultati + "Clusterizzazione_Angoli_H2O_in_funzione_della_distanza\\"
if funzione_della_distanza_onoff == "OFF" and calcolo_angoli_onoff == "ON":
    path_output_clusterizzazione = path_risultati + "Clusterizzazione_Angoli_H2O\\Clusterizzazione\\" + cartella_e_nome_output + ".txt"
    path_output_angoli = path_risultati + "Clusterizzazione_Angoli_H2O\\Angoli\\" + cartella_e_nome_output + "_angoli_distanza" + ".txt"
    path_output_angoli_stat = path_risultati + "Clusterizzazione_Angoli_H2O\\Angoli_Statistica\\" + cartella_e_nome_output + "_angoli_distanza" + ".txt"
    path_istogrammi = path_risultati + "Clusterizzazione_Angoli_H2O\\Angoli_Istogrammi\\"
    path_clusterizzazione_plot = path_risultati + "Clusterizzazione_Angoli_H2O\\Clusterizzazione_plot\\"
    path_impostazioni = path_risultati + "Clusterizzazione_Angoli_H2O\\"

if funzione_della_distanza_onoff == "OFF" and calcolo_angoli_onoff == "OFF":
    path_output_clusterizzazione = path_risultati + "Clusterizzazione\\" + cartella_e_nome_output + ".txt"
    path_clusterizzazione_plot = path_risultati + "Clusterizzazione\\Clusterizzazione_plot\\"
    path_impostazioni = path_risultati + "Clusterizzazione\\"

#COSTANTI FONDAMENTALI
if tipo_di_ambiente == "BULK":
    dimensioni_scatola = [2.99883,2.99883,2.99883]
if tipo_di_ambiente == "NaCl":
    dimensioni_scatola = [39.606,39.606,50.]
if tipo_di_ambiente == "BULK":
    numero_di_frame = 1001 #numero di frame da analizzare per ogni file
if tipo_di_ambiente == "NaCl":
    numero_di_frame = 3000  # numero di frame da analizzare per ogni file
np.set_printoptions(precision=2)
if tipo_di_ambiente == "BULK":
    distanza_max_clusterizzazione = 3
    numero_minimo_elementi = 5
if tipo_di_ambiente == "NaCl":
    distanza_max_clusterizzazione = 4
    numero_minimo_elementi = 3
# *** FUNZIONI ***
def nuovi_indici(vecchi_indici):
    indici_o_nuovi = np.array(vecchi_indici + (vecchi_indici*2))
    indici_h1_nuovi = np.array(indici_o_nuovi + 1)
    indici_h2_nuovi = np.array(indici_o_nuovi + 2)
    return indici_o_nuovi, indici_h1_nuovi, indici_h2_nuovi

def periodicita(L = dimensioni_scatola[0]): #L larghezza della scatola
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

def clusterizzazione(eps=distanza_max_clusterizzazione, min_samples=numero_minimo_elementi):

    if periodicita_onoff == "ON":
        db = DBSCAN(eps, min_samples, metric='precomputed')
        db.fit_predict(periodicita())
    elif periodicita_onoff == "OFF":
        db = DBSCAN(eps, min_samples)
        db.fit_predict(data_solo_ossigeno)

    db_labels = db.labels_
    #print(db_labels)

    if clusterizzazione_grafico_onoff == "ON":
        for counter_plot in range (0,4):
            fig = plt.figure()
            ax = Axes3D(fig)
            ax.set_xlim3d(-19.803, 19.803)
            ax.set_ylim3d(-19.803, 19.803)
            ax.set_zlim3d(-25, +25)
            ax.scatter(data_solo_ossigeno[:, 0], data_solo_ossigeno[:, 1], data_solo_ossigeno[:, 2], c=db_labels, s=150)
            #Angolo di visione del plot3d, per capire che valori scegliere basta guardare che valori assumono in un plot muovendolo
            if counter_plot == 0:
                ax.view_init(azim=200)
                plt.savefig(path_clusterizzazione_plot + nome_immagine_ + "\\Prospettiva\\" + str(count + 1) + ".png")
            if counter_plot == 1:
                ax.view_init(elev=90,azim=90)
                plt.savefig(path_clusterizzazione_plot + nome_immagine_ + "\\1\\" + str(count + 1) + ".png")
            if counter_plot == 2:
                ax.view_init(elev=90,azim=0)
                plt.savefig(path_clusterizzazione_plot + nome_immagine_ + "\\2\\" + str(count + 1) + ".png")
            if counter_plot == 3:
                ax.view_init(elev=180,azim=0)
                plt.savefig(path_clusterizzazione_plot + nome_immagine_ + "\\3\\" + str(count + 1) + ".png")
            #plt.show()
            plt.close()

    #n_clusters_ = len(set(db_labels)) - (1 if -1 in db_labels else 0)
    #n_noise_ = list(db_labels).count(-1) NON SERVE
    n_elements_clusters = np.bincount(db_labels[db_labels >= 0])

    return n_elements_clusters, db_labels

def calcolo_angoli(dataset,indici_O,indici_H1,indici_H2):
    if funzione_della_distanza_onoff == "ON":
        """Creo una lista vuota che ospiterà gli angoli dei clusters(indipendentemente da che siano isole o altro
            questa distinzione viene fatta prima di richiamare la funzione"""
        lista_liste_angoli = []
        """#Ottengo dalla lista una LISTA DI LISTE, ogni lista conterrà gli angoli per le molecole d'acqua a diverse distanze dalla
        #superficie, a step di 0.5 (ipotizzando che la superficie sia a 6.0 A),l'algoritmo riconosce il numero di settori
        da creare sulla base dell'inizio e la fine dell'area da suddividere e della lunghezza dello step"""
        # Praticamente poi si suddivide z in tanti "settori" lunghi 0.5 A, gli angoli delle molecole d'acqua appartenenti ad un
        # Determinato settore saranno assegnate ad un valore di distanza corrispondente al limite massimo del settore
        # questo significa che tutto ciò che si trova tra
        # ad esempio, 6.5 e 7, sarà assegnato alla posizione 7, ma indicherà che si trova tra la posizione 7 e quella precedente
        for i in np.arange(6.5, 25.5, 0.5):
            lista_liste_angoli.append([])
        "Segue il calcolo vero e proprio, che si concentrerà su una molecola d'acqua alla volta"
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
            if tipo_di_ambiente == "NaCl":
                if O[2] > 0:
                    normale = [0, 0, 1]
                elif O[2] < 0:
                    normale = [0, 0, -1]
            elif tipo_di_ambiente == "BULK":
                normale = [0, 0, 1]
            # coseno angolo tra i due vettori
            prodotto_scalare_vettori = (v_H2O_normalized[0] * normale[0]) + (v_H2O_normalized[1] * normale[1]) + (
                        v_H2O_normalized[2] * normale[2])
            norma_v_H2O_normalized = math.sqrt(
                v_H2O_normalized[0] ** 2 + v_H2O_normalized[1] ** 2 + v_H2O_normalized[2] ** 2)
            norma_normale = math.sqrt(normale[0] ** 2 + normale[1] ** 2 + normale[2] ** 2)
            prodotto_norme = norma_v_H2O_normalized * norma_normale
            coseno_angolo = prodotto_scalare_vettori / prodotto_norme

            if unità_di_misura_angoli == "GRADI":
                # Ottengo angolo in radianti
                angolo = math.acos(coseno_angolo)
                # Converto in gradi
                angolo_gradi = math.degrees(angolo)
                """Aggiungo le molecole al database
                Creo il ciclo for che, dato un angolo per un'acqua specifica, determinerà a quale "settore di distanza" appartiene,
                Sulla base della posizione di O, andando quindi ad aggiungere il valore dell'angolo alla lista corrispondente"""
                contatore_settore = 0
                for distanza_max in np.arange(6.5, 25.5, 0.5):
                    #print(distanza_max)
                    # Viene utilizzato il valore assoluto abs() perchè abbiamo una funzione della distanza assoluta
                    if (abs(O[2]) < distanza_max) & (abs(O[2]) > (distanza_max - 0.5)):
                        lista_liste_angoli[contatore_settore].append(angolo_gradi)
                        break
                    contatore_settore += 1
            if unità_di_misura_angoli == "COSENO":
                """Aggiungo le molecole al database
                Creo il ciclo for che, dato un angolo per un'acqua specifica, determinerà a quale "settore di distanza" appartiene,
                Sulla base della posizione di O, andando quindi ad aggiungere il valore dell'angolo alla lista corrispondente"""
                contatore_settore = 0
                for distanza_max in np.arange(6.5, 25.5, 0.5):
                    # print(distanza_max)
                    # Viene utilizzato il valore assoluto abs() perchè abbiamo una funzione della distanza assoluta
                    if (abs(O[2]) < distanza_max) & (abs(O[2]) > (distanza_max - 0.5)):
                        lista_liste_angoli[contatore_settore].append(coseno_angolo)
                        break
                    contatore_settore += 1
        """Terminato il processo di calcolo e smistamento degli angoli per le acque dei vari settori ottengo una lista
        di liste disomogenea, ogni settore (ogni lista) avrà una lunghezza diversa dovuta al diverso numero di acque 
        presenti.
        Si genera ora un numpy array di array rendendolo omogeneo, vengono riempite le colonne vuote dei vari array
        dei vari settori con Nan, il quale poi non verrà calcolato nella media, ma l'omogeneità garantirà il corretto
        funzionamento dell'array di array(numpy lavora bene solo con matrici omogenee come colonne)"""
        pad = len(max(lista_liste_angoli, key=len))
        array_arrays_angoli = np.array([i + [float('nan')] * (pad - len(i)) for i in lista_liste_angoli])
        """L'array di array ottenuto, omogeneo, verrà concatenato(append su ogni riga) a quello database"""
        return array_arrays_angoli

    if funzione_della_distanza_onoff == "OFF":
        lista_angoli = []
        array_angoli = np.array([])
        np.set_printoptions(precision=3)
        "Segue il calcolo vero e proprio, che si concentrerà su una molecola d'acqua alla volta"
        for count_angoli in range(0, len(indici_O)):
            # Coordinate 3D acqua
            O = np.array(dataset[(indici_O[count_angoli]), :]).astype(np.float)
            H1 = np.array(dataset[(indici_H1[count_angoli]), :]).astype(np.float)
            H2 = np.array(dataset[(indici_H2[count_angoli]), :]).astype(np.float)
            #print(O)
            #print(H1)
            #print(H2)
            # Array legami
            d_OH1 = H1 - O
            d_OH2 = H2 - O
            # Vettore totale acqua
            v_H2O = d_OH1 + d_OH2
            # Normalizzazione vettore acqua
            norma_v_H2O = math.sqrt(v_H2O[0] ** 2 + v_H2O[1] ** 2 + v_H2O[2] ** 2)
            v_H2O_normalized = [v_H2O[0] / norma_v_H2O, v_H2O[1] / norma_v_H2O, v_H2O[2] / norma_v_H2O]
            # Dichiarazione Normale a superficie
            if tipo_di_ambiente == "NaCl":
                if O[2] > 0:
                    normale = [0, 0, 1]
                elif O[2] < 0:
                    normale = [0, 0, -1]
            elif tipo_di_ambiente == "BULK":
                normale = [0, 0, 1]
            # coseno angolo tra i due vettori
            prodotto_scalare_vettori = (v_H2O_normalized[0] * normale[0]) + (v_H2O_normalized[1] * normale[1]) + (
                    v_H2O_normalized[2] * normale[2])
            norma_v_H2O_normalized = math.sqrt(
                v_H2O_normalized[0] ** 2 + v_H2O_normalized[1] ** 2 + v_H2O_normalized[2] ** 2)
            norma_normale = math.sqrt(normale[0] ** 2 + normale[1] ** 2 + normale[2] ** 2)
            prodotto_norme = norma_v_H2O_normalized * norma_normale
            coseno_angolo = prodotto_scalare_vettori / prodotto_norme

            # TEST
            #print(v_H2O_normalized,normale)
            if unità_di_misura_angoli == "GRADI":
                # Ottengo angolo in radianti
                angolo = math.acos(coseno_angolo)
                # Converto in gradi
                angolo_gradi = math.degrees(angolo)
                lista_angoli.append(angolo_gradi)
                array_angoli = np.array(lista_angoli)
            elif unità_di_misura_angoli == "COSENO":
                lista_angoli.append(coseno_angolo)
                array_angoli = np.array(lista_angoli)
        np.set_printoptions(precision=2)
        return array_angoli


"""def trova_linea(frase, filename):
    with open(filename, 'r') as f:
        for (i, line) in enumerate(f):
            if frase in line:
                return i
    return -1"""

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def splitta(database_originale):
    isole = database_originale[database_originale < 70]
    monolayers = database_originale[database_originale >= 70]
    return isole,monolayers

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


# *** INIZIO CODICE ***
# dichiarazione delle variabili necessarie nel ciclo for:
count = 0
# Definisco le colonne che caratterizzerano i dataframe successivi
if tipo_di_ambiente == "NaCl":
    colonne_nomi=np.array(["0","1","2","3","4","x","y","z"]) #colonne del dataframe .pdb
if tipo_di_ambiente == "BULK":
    colonne_nomi = np.array(["0", "1", "2", "3","4","x", "y", "z", "MODEL", "altro"])  # colonne del dataframe .pdb
colonne_elemento_e_coordinate = ["2","x","y","z"]
n_isole_database = np.array([])
n_elements_isole_database = np.array([])
n_monolayers_database = np.array([])
n_elements_monolayers_database = np.array([])

#Printa opzioni
print("-Clusterizzazione 3D: " + clusterizzazione_grafico_onoff)
print("-Calcolo angoli: " + clusterizzazione_grafico_onoff)
print("-Clusterizzazione 3D: " + calcolo_angoli_onoff)
print("-Funzione della distanza: " + funzione_della_distanza_onoff)
print("-Tipo di ambiente : " + tipo_di_ambiente)
path_impostazioni
with open(path_impostazioni + "Impostazioni.txt", 'w') as impostazioni_txt:
    impostazioni_txt.write("-Clusterizzazione 3D: " + clusterizzazione_grafico_onoff + "\n")
    impostazioni_txt.write("-Calcolo angoli: " + clusterizzazione_grafico_onoff+ "\n")
    impostazioni_txt.write("-Clusterizzazione 3D: " + calcolo_angoli_onoff + "\n")
    impostazioni_txt.write("-Funzione della distanza: " + funzione_della_distanza_onoff + "\n")
    impostazioni_txt.write("-Tipo di ambiente : " + tipo_di_ambiente + "\n")
    impostazioni_txt.flush()
    impostazioni_txt.close()

# APRE FILE DA SCRIVERE
with open(path_output_clusterizzazione, 'w') as csvfile, open(path_output_angoli, 'w') as csv_angoli, open(path_output_angoli_stat, 'w') as angoli_stat:
    fieldnames = ['nome_file', 'n_isole_medio', 'n_isole_medio_std_della_media', 'n_elements_isole_medio',
                  'n_elements_isole_medio_std_della_media','n_monolayers_medio', 'n_monolayers_medio_std_della_media',
                  'n_elements_monolayers_medio', 'n_elements_monolayers_medio_std_della_media']
    fieldnames_angoli = ['titolo']
    #Modalità di scrittura per il file dei cluster
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writerStat = csv.DictWriter(angoli_stat, fieldnames=fieldnames)
    #Modalità di scrittura per il file degli angoli
    wr = csv.writer(csv_angoli)
    wrStat = csv.writer(angoli_stat)
    titoli = csv.DictWriter(csv_angoli,fieldnames=fieldnames_angoli)
    titoliStat = csv.DictWriter(angoli_stat, fieldnames=fieldnames_angoli)
    writer.writeheader()
# CARICAMENTO FILES
    files_pdb = os.listdir(path_cartella)  #crea una lista contenente tutti i nomi dei file
    for x in range(len(files_pdb)):
        path = path_cartella + "\\" + files_pdb[x]
        print(path)
        # L'intero file .pdb viene estratto e inserito in un dataframe, come delimiter gli spazi, come colonne i nomi
        # Scritti precedentemente, nessuna compressione dei dati
        dataframe = pd.DataFrame()
        dataframe = pd.read_csv(path, delim_whitespace=True, names=colonne_nomi, low_memory=False)
        print(dataframe)
        # Trovo il path per l'output di clusterizzazione_plot
        if (files_pdb[x])[-13:-4] == "300Msteps":
            troncone_numero_ = "1"
        if (files_pdb[x])[-17:-4] == "300+300Msteps":
            troncone_numero_ = "2"
        nome_immagine_ = "Pressione_" + (files_pdb[x])[36:41] + "_Milliatmosfere" + "_Replica_" + cartella_e_nome_output[
                -1] + "_Troncone_" + troncone_numero_
        # to_numeric() rende float i numeri della colonna "1", .apply() applica la modifica al dataframe copia su cui sto
        # agendo, devo eguagliare infine il database originale al database copia
        if tipo_di_ambiente == "NaCl":
            dataframe.loc[1:, "1"] = dataframe.loc[1:, "1"].apply(pd.to_numeric, errors='coerce')
        #if tipo_di_ambiente == "BULK":
            #dataframe.loc[1:, "MODEL"] = dataframe.loc[1:, "MODEL"].apply(pd.to_numeric, errors='coerce')
        # trovo TUTTE le posizioni dei model successivi a 1 e le unisco alla posizione di model 1 specificata a mano
        if tipo_di_ambiente == "NaCl":
            posizione_model = np.append([0], np.where(dataframe.loc[1:, "1"] > 1))
        if tipo_di_ambiente == "BULK":
            posizione_model = np.append([0], np.where(dataframe.loc[1:, "MODEL"] > 1))
        # correggo la posizione essendo che parte da 1 nel data.loc(), ottengo la posizione dei model nel dataframe
        posizione_model += 1
        # lunghezza (numero di linee) del file nel path
        numero_di_linee_totali = file_len(path)
        # AZZERO VARIABILI
        n_isole_database = np.array([])
        n_elements_isole_database = np.array([])
        n_monolayers_database = np.array([])
        n_elements_monolayers_database = np.array([])
        if calcolo_angoli_onoff == "ON":
            """Sempre parte di AZZERO VARIABILI, vado a creare degli array di arrays database che conterranno gli angoli
            Delle molecole d'acqau, ogni riga farà riferimento ad un determinato settore di distanza dalla superficie"""
            lista_liste_angoli_temp = []
            if funzione_della_distanza_onoff == "ON":
                for i in np.arange(6.5, 25.5, 0.5):
                    lista_liste_angoli_temp.append([])
            angoli_isole_distanza_database = np.array(lista_liste_angoli_temp)
            angoli_layers_distanza_database = np.array(lista_liste_angoli_temp)
            angoli_rumore_distanza_database = np.array(lista_liste_angoli_temp)

        for count in range(0, numero_di_frame):
            print("Elaborando il frame:", count + 1)
            if count != (numero_di_frame - 1):
                # counter per il fine frame
                count1 = count + 1
                # Seleziono dati, saranno selezionati i dati dalla posizione del model del frame + 1(non si seleziona "model" nei dati)
                # alla posizione del model successivo - 2 (non si seleziona "model" e "endmodel"
                # le colonne sono quelle delle coordinate ma anche quella dell'elemento
                if tipo_di_ambiente == "NaCl":
                    data = dataframe.loc[(posizione_model[count] + 1):(posizione_model[count1] - 2),colonne_elemento_e_coordinate].copy(deep=True)
                elif tipo_di_ambiente == "BULK":
                    data = dataframe.loc[(posizione_model[count] + 1):(posizione_model[count1] - 7),colonne_elemento_e_coordinate].copy(deep=True)
            else:
                # nel caso siamo all'ultimo frame, non si può usare come delimitatore il model del frame successivo
                # quindi semplicemente gli dico di saltare le ultime due righe(uso iloc per questo, .loc non può farlo)
                # non serve neanche il count per trovare il model 3000(so che sarà l'ultimo quindi -1)
                # le colonne vanno indicate con numeri essendo iloc
                data = dataframe.iloc[(posizione_model[-1] + 1):-2, [2, 5, 6, 7]].copy(deep=True)

            data.reset_index(drop=True, inplace=True)
            # ESTRAGGO I DATASET soloossigeno e ossigeno&idrogeno
            data_solo_ossigeno = data.loc[::3, ["x", "y", "z"]].to_numpy()
            """print(posizione_model)
            print(dataframe)
            print(data)
            print(data_solo_ossigeno)"""
            data_ossigeno_e_idrogeno = data.loc[:, ["x", "y", "z"]].to_numpy()

            if data_solo_ossigeno.size != 3:
                if outofbox_onoff == "ON":
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
                # Se ho una sola molecola, il vettore dei labels è un solo valore, di rumore
                labels = np.array([-1])


            """UNISCE I TEMP AI DATABASE (numero di clusters)"""
            n_isole_database = np.append(n_isole_database, n_isole_temp)  # .append permette di unire array con diverso numero di colonne (diverso numero di clusters in diversi frame) in un unico array 1-D
            n_monolayers_database = np.append(n_monolayers_database, n_monolayers_temp)
            """UNISCE I TEMP AI DATABASE (numero di elementi)"""
            n_elements_isole_database = np.append(n_elements_isole_database, n_elements_isole_temp)
            n_elements_monolayers_database = np.append(n_elements_monolayers_database, n_elements_monolayers_temp)
            #print(n_clusters_database)            # COSA BUONA: se ci sono 0 cluster viene registrato 0 (deve fare media)
            #print(n_elements_clusters_database)   # se non ci sono cluster non viene registrato un valore di numero di elementi(GIUSTO: non deve fare media)
            if calcolo_angoli_onoff == "ON":
                if data_solo_ossigeno.size != 3:
                    """STUDIO ANGOLI VETTORE H2O/NORMALE ALLA SUPERFICIE DI NaCl"""
                    # Definisco quali labels sono associati alle isole,layers e rumore
                    labels_delle_isole = np.where(n_elements_clusters_temp < 70)
                    labels_dei_layer = np.where(n_elements_clusters_temp >= 70)
                    label_rumore = -1
                    # Trovo le righe delle coordinate degli ossigeni appartenenti ad isole, layers e rumore nel
                    # dataset con solo ossigeni
                    indici_ossigeno_isole_in_solo_ox = np.where(np.in1d(labels, labels_delle_isole))
                    indici_ossigeno_layers_in_solo_ox = np.where(np.in1d(labels, labels_dei_layer))
                    indici_ossigeno_rumore_in_solo_ox = np.where(labels == -1)
                    #print(indici_ossigeno_isole_in_solo_ox)

                    # Trovo le righe delle coordinate degli ossigeni appartenenti ad isole, layers e rumore nel
                    # dataset con ossigeni ed idrogeni, ricavo da questi indici i medesimi indici per H1 ed H2
                    # ISOLE
                    indici_ossigeno_isole, indici_idrogeno1_isole, indici_idrogeno2_isole = nuovi_indici(
                        indici_ossigeno_isole_in_solo_ox[0])
                    # LAYERS
                    indici_ossigeno_layers, indici_idrogeno1_layers, indici_idrogeno2_layers = nuovi_indici(
                        indici_ossigeno_layers_in_solo_ox[0])
                    # RUMORE
                    indici_ossigeno_rumore, indici_idrogeno1_rumore, indici_idrogeno2_rumore = nuovi_indici(
                        indici_ossigeno_rumore_in_solo_ox[0])
                    #print(n_elements_isole_temp)
                    #print(indici_ossigeno_isole, indici_idrogeno1_isole, indici_idrogeno2_isole)
                    if funzione_della_distanza_onoff == "ON":
                        # TROVO GLI ANGOLI, PER TUTTE LE MOLECOLE D'ACQUA DI OGNI GRUPPO(tramite la funzione) e LI UNISCO AL DATABASE DEL FILE(che si azzera dopo l'apertura di ogni file)
                        angoli_isole_distanza_database = np.concatenate((angoli_isole_distanza_database, calcolo_angoli(data_ossigeno_e_idrogeno, indici_ossigeno_isole, indici_idrogeno1_isole, indici_idrogeno2_isole)),axis=1)
                        angoli_layers_distanza_database = np.concatenate((angoli_layers_distanza_database, calcolo_angoli(data_ossigeno_e_idrogeno, indici_ossigeno_layers, indici_idrogeno1_layers, indici_idrogeno2_layers)),axis=1)
                        #print(angoli_layers_distanza_database)
                        angoli_rumore_distanza_database = np.concatenate((angoli_rumore_distanza_database, calcolo_angoli(data_ossigeno_e_idrogeno, indici_ossigeno_rumore, indici_idrogeno1_rumore, indici_idrogeno2_rumore)),axis=1)
                        #print(angoli_isole_distanza_database, angoli_layers_distanza_database, angoli_rumore_distanza_database)
                    elif funzione_della_distanza_onoff == "OFF":
                        angoli_isole_distanza_database = np.append(angoli_isole_distanza_database,
                                                                         calcolo_angoli(data_ossigeno_e_idrogeno,
                                                                                        indici_ossigeno_isole,
                                                                                        indici_idrogeno1_isole,
                                                                                        indici_idrogeno2_isole))
                        angoli_layers_distanza_database = np.append(angoli_layers_distanza_database,
                                                                          calcolo_angoli(data_ossigeno_e_idrogeno,
                                                                                         indici_ossigeno_layers,
                                                                                         indici_idrogeno1_layers,
                                                                                         indici_idrogeno2_layers))
                        #print(angoli_layers_distanza_database)
                        angoli_rumore_distanza_database = np.append(angoli_rumore_distanza_database,
                                                                          calcolo_angoli(data_ossigeno_e_idrogeno,
                                                                                         indici_ossigeno_rumore,
                                                                                         indici_idrogeno1_rumore,
                                                                                         indici_idrogeno2_rumore))
                # nel caso in cui ci sia solo una molecola, il sistema con il clustering non funziona, quindi devo ovviare fornendo io l'indice dell'ossigeno e degli idrogeni
                # considero l'acqua alone come rumore
                else:
                    indici_ossigeno_alone = np.array([0])
                    indici_idrogeno1_alone = np.array([1])
                    indici_idrogeno2_alone = np.array([2])
                    if funzione_della_distanza_onoff == "ON":
                        angoli_rumore_distanza_database = np.concatenate((angoli_rumore_distanza_database, calcolo_angoli(data_ossigeno_e_idrogeno, indici_ossigeno_alone, indici_idrogeno1_alone, indici_idrogeno2_alone)),axis=1)
                    elif funzione_della_distanza_onoff == "OFF":
                        angoli_rumore_distanza_database = np.append(angoli_rumore_distanza_database,
                                                                          calcolo_angoli(data_ossigeno_e_idrogeno,
                                                                                         indici_ossigeno_alone,
                                                                                         indici_idrogeno1_alone,
                                                                                         indici_idrogeno2_alone))

        """ TROVA VALORI MEDI -> OUTPUT  CLUSTERS """
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
        if calcolo_angoli_onoff == "ON":
            if funzione_della_distanza_onoff == "ON":
                """TROVA VALORI MEDI -> ANGOLI """
                # Se non ho molecole in uno de tre database, devo settare la media su "Nan", se mettessi 0 sarebbe equivocabile, mentre una string adarebbe errore
                """Come il database degli angoli passa da vettore mono-dimensionale a matrice bidimensionale(in questo caso
                specifico in cui ho funzione della distanza),il contenitore delle medie degli angoli non sarà una variabile
                ma un vettore monodimensionale, ogni posizione indica la media degli angoli in certo settore di distanza."""
                #Inizializzo per prima cosa i vettori degli angoli medi come array mono-d vuoti
                angoli_isole_medio_distanza = np.array([])
                angoli_layers_medio_distanza = np.array([])
                angoli_rumore_medio_distanza = np.array([])
                angoli_isole_medio_std_della_media = np.array([])
                angoli_layers_medio_std_della_media = np.array([])
                angoli_rumore_medio_std_della_media = np.array([])
                #Ottengo anche la semplice std(per ora solo da usare nei grafici)
                angoli_isole_medio_std = np.array([])
                angoli_layers_medio_std = np.array([])
                angoli_rumore_medio_std = np.array([])

                angoli_isole_medio_min = np.array([])
                angoli_layers_medio_min = np.array([])
                angoli_rumore_medio_min = np.array([])

                angoli_isole_medio_max = np.array([])
                angoli_layers_medio_max = np.array([])
                angoli_rumore_medio_max = np.array([])
                #Inizializzo il counter che permetterà di studiare i diversi vettori (dell'array di array) contenenti
                #Gli angoli delle molecole nei diversi settori
                counter_media_angoli = 0
                for distanza_max in np.arange(6.5, 25.5, 0.5):
                    #Ora ottengo le medie, andando a verificare che non ci siano settori senza molecole d'acqua(restituirebbe
                    #Errore per media di soli nan
                    """.isnan ottiene un vettore identico dove i nan sono sostituiti da true ed i valori da false, all() verifica
                    se tutti i valori sono uguali(ad esempio tutti True perchè tutti nan) e restituisce True nel caso io abbia solo nan"""

                    """Sia per il calcolo delle medie che degli std si usano le specifiche nanmean e nanstd, che ignorano i NaNs"""
                    if np.isnan(angoli_isole_distanza_database[counter_media_angoli]).all() != True:
                        angoli_isole_medio_distanza = np.append(angoli_isole_medio_distanza,np.nanmean(angoli_isole_distanza_database[counter_media_angoli]))
                        angoli_isole_medio_std_della_media = np.append(angoli_isole_medio_std_della_media,np.nanstd(angoli_isole_distanza_database[counter_media_angoli]) / ((np.size(angoli_isole_distanza_database[counter_media_angoli]) - np.count_nonzero(np.isnan(angoli_isole_distanza_database[counter_media_angoli]))) ** (0.5)))
                        angoli_isole_medio_std = np.append(angoli_isole_medio_std,np.nanstd(angoli_isole_distanza_database[counter_media_angoli]))
                        angoli_isole_medio_min = np.append(angoli_isole_medio_min,np.nanmin(angoli_isole_distanza_database[counter_media_angoli]))
                        angoli_isole_medio_max = np.append(angoli_isole_medio_max,np.nanmax(angoli_isole_distanza_database[counter_media_angoli]))
                    else:
                        angoli_isole_medio_distanza = np.append(angoli_isole_medio_distanza,float("nan"))
                        angoli_isole_medio_std_della_media = np.append(angoli_isole_medio_std_della_media,float("nan"))
                        angoli_isole_medio_std = np.append(angoli_isole_medio_std, float("nan"))
                        angoli_isole_medio_min = np.append(angoli_isole_medio_min,float("nan"))
                        angoli_isole_medio_max = np.append(angoli_isole_medio_max,float("nan"))

                    if np.isnan(angoli_layers_distanza_database[counter_media_angoli]).all() != True:
                        angoli_layers_medio_distanza = np.append(angoli_layers_medio_distanza, np.nanmean(angoli_layers_distanza_database[counter_media_angoli]))
                        angoli_layers_medio_std_della_media = np.append(angoli_layers_medio_std_della_media,np.nanstd(angoli_layers_distanza_database[counter_media_angoli]) / ((np.size(angoli_layers_distanza_database[counter_media_angoli]) - np.count_nonzero(np.isnan(angoli_layers_distanza_database[counter_media_angoli]))) ** (0.5)))
                        angoli_layers_medio_std = np.append(angoli_layers_medio_std,np.nanstd(angoli_layers_distanza_database[counter_media_angoli]))
                        angoli_layers_medio_min = np.append(angoli_layers_medio_min,
                                                           np.nanmin(angoli_layers_distanza_database[counter_media_angoli]))
                        angoli_layers_medio_max = np.append(angoli_layers_medio_max,
                                                           np.nanmax(angoli_layers_distanza_database[counter_media_angoli]))
                    else:
                        angoli_layers_medio_distanza = np.append(angoli_layers_medio_distanza, float("nan"))
                        angoli_layers_medio_std_della_media = np.append(angoli_layers_medio_std_della_media, float("nan"))
                        angoli_layers_medio_std = np.append(angoli_layers_medio_std, float("nan"))
                        angoli_layers_medio_min = np.append(angoli_layers_medio_min, float("nan"))
                        angoli_layers_medio_max = np.append(angoli_layers_medio_max, float("nan"))

                    if np.isnan(angoli_rumore_distanza_database[counter_media_angoli]).all() != True:
                        angoli_rumore_medio_distanza = np.append(angoli_rumore_medio_distanza,np.nanmean(angoli_rumore_distanza_database[counter_media_angoli]))
                        angoli_rumore_medio_std_della_media = np.append(angoli_rumore_medio_std_della_media,np.nanstd(angoli_rumore_distanza_database[counter_media_angoli]) / ((np.size(angoli_rumore_distanza_database[counter_media_angoli]) - np.count_nonzero(np.isnan(angoli_rumore_distanza_database[counter_media_angoli]))) ** (0.5)))
                        angoli_rumore_medio_std = np.append(angoli_rumore_medio_std,np.nanstd(angoli_rumore_distanza_database[counter_media_angoli]))
                        angoli_rumore_medio_min = np.append(angoli_rumore_medio_min,
                                                           np.nanmin(angoli_rumore_distanza_database[counter_media_angoli]))
                        angoli_rumore_medio_max = np.append(angoli_rumore_medio_max,
                                                           np.nanmax(angoli_rumore_distanza_database[counter_media_angoli]))
                    else:
                        angoli_rumore_medio_distanza = np.append(angoli_rumore_medio_distanza,float("nan"))
                        angoli_rumore_medio_std_della_media = np.append(angoli_rumore_medio_std_della_media,float("nan"))
                        angoli_rumore_medio_std = np.append(angoli_rumore_medio_std, float("nan"))
                        angoli_rumore_medio_min = np.append(angoli_rumore_medio_min, float("nan"))
                        angoli_rumore_medio_max = np.append(angoli_rumore_medio_max, float("nan"))
                        #print(angoli_rumore_medio_std_della_media)
                    #Aggiorno il counter, al prossimo loop verrà analizzato il settore successivo
                    counter_media_angoli += 1
            elif funzione_della_distanza_onoff == "OFF":
                """TROVA VALORI MEDI -> ANGOLI (non in funzione della distanza)"""
                # Inizializzo per prima cosa i vettori degli angoli medi come array mono-d vuoti
                angoli_isole_medio_distanza = 0
                angoli_layers_medio_distanza = 0
                angoli_rumore_medio_distanza = 0
                angoli_isole_medio_std_della_media = 0
                angoli_layers_medio_std_della_media = 0
                angoli_rumore_medio_std_della_media = 0
                # Ottengo anche la semplice std(per ora solo da usare nei grafici)
                angoli_isole_medio_std = 0
                angoli_layers_medio_std = 0
                angoli_rumore_medio_std = 0

                angoli_isole_medio_min = 0
                angoli_layers_medio_min = 0
                angoli_rumore_medio_min = 0

                angoli_isole_medio_max = 0
                angoli_layers_medio_max = 0
                angoli_rumore_medio_max = 0
                # Inizializzo il counter che permetterà di studiare i diversi vettori (dell'array di array) contenenti
                # Gli angoli delle molecole nei diversi settori
                counter_media_angoli = 0
                # Ora ottengo le medie, andando a verificare che non ci siano settori senza molecole d'acqua(restituirebbe
                # Errore per media di soli nan
                """.isnan ottiene un vettore identico dove i nan sono sostituiti da true ed i valori da false, all() verifica
                se tutti i valori sono uguali(ad esempio tutti True perchè tutti nan) e restituisce True nel caso io abbia solo nan"""

                """Sia per il calcolo delle medie che degli std si usano le specifiche nanmean e nanstd, che ignorano i NaNs"""
                if np.isnan(angoli_isole_distanza_database).all() != True:
                    angoli_isole_medio_distanza = np.nanmean(angoli_isole_distanza_database)
                    angoli_isole_medio_std_della_media = np.nanstd(angoli_isole_distanza_database) / ((np.size(angoli_isole_distanza_database) - np.count_nonzero(np.isnan(angoli_isole_distanza_database))) ** (0.5))
                    angoli_isole_medio_std = np.nanstd(angoli_isole_distanza_database)
                    angoli_isole_medio_min = np.nanmin(angoli_isole_distanza_database)
                    angoli_isole_medio_max = np.nanmax(angoli_isole_distanza_database)
                else:
                    angoli_isole_medio_distanza = float("nan")
                    angoli_isole_medio_std_della_media = float("nan")
                    angoli_isole_medio_std = float("nan")
                    angoli_isole_medio_min = float("nan")
                    angoli_isole_medio_max = float("nan")

                if np.isnan(angoli_layers_distanza_database).all() != True:
                    angoli_layers_medio_distanza = np.nanmean(angoli_layers_distanza_database)
                    angoli_layers_medio_std_della_media = np.nanstd(angoli_layers_distanza_database) / ((np.size(
                        angoli_layers_distanza_database) - np.count_nonzero(
                        np.isnan(angoli_layers_distanza_database))) ** (0.5))
                    angoli_layers_medio_std = np.nanstd(angoli_layers_distanza_database)
                    angoli_layers_medio_min = np.nanmin(angoli_layers_distanza_database)
                    angoli_layers_medio_max = np.nanmax(angoli_layers_distanza_database)
                else:
                    angoli_layers_medio_distanza = float("nan")
                    angoli_layers_medio_std_della_media = float("nan")
                    angoli_layers_medio_std = float("nan")
                    angoli_layers_medio_min = float("nan")
                    angoli_layers_medio_max = float("nan")

                if np.isnan(angoli_rumore_distanza_database).all() != True:
                    angoli_rumore_medio_distanza = np.nanmean(angoli_rumore_distanza_database)
                    angoli_rumore_medio_std_della_media = np.nanstd(angoli_rumore_distanza_database) / ((np.size(
                        angoli_rumore_distanza_database) - np.count_nonzero(
                        np.isnan(angoli_rumore_distanza_database))) ** (0.5))
                    angoli_rumore_medio_std = np.nanstd(angoli_rumore_distanza_database)
                    angoli_rumore_medio_min = np.nanmin(angoli_rumore_distanza_database)
                    angoli_rumore_medio_max = np.nanmax(angoli_rumore_distanza_database)
                else:
                    angoli_rumore_medio_distanza = float("nan")
                    angoli_rumore_medio_std_della_media = float("nan")
                    angoli_rumore_medio_std = float("nan")
                    angoli_rumore_medio_min = float("nan")
                    angoli_rumore_medio_max = float("nan")



        """ !!! STAMPA UNA RIGA DI OUTPUT NEL FILE DELLA CLUSTERIZZAZIONE !!!"""
        writer.writerow({'nome_file': files_pdb[x], 'n_isole_medio': "%.2f" %n_isole_medio, 'n_isole_medio_std_della_media': "%.2f" %n_isole_medio_std_della_media,
                        'n_elements_isole_medio': "%.2f" %n_elements_isole_medio, 'n_elements_isole_medio_std_della_media': "%.2f" %n_elements_isole_medio_std_della_media
                        ,'n_monolayers_medio':"%.2f" %n_monolayers_medio, 'n_monolayers_medio_std_della_media':"%.2f" %n_monolayers_medio_std_della_media,
                        'n_elements_monolayers_medio':"%.2f" %n_elements_monolayers_medio, 'n_elements_monolayers_medio_std_della_media':"%.2f" %n_elements_monolayers_medio_std_della_media})
        csvfile.flush()
        if calcolo_angoli_onoff == "ON":
            if funzione_della_distanza_onoff == "ON":
                """!!! STAMPA FILE ANGOLI DI OUTPUT, UNA RIGA PER INDICARE IL NOM DEL FILE,UNA RIGA PER IL TIPO DI CLUSTER, UNA RIGA L?ARRAY DELLA MEDIA,UNA PER GLI ERRORI !!!"""
                titoli.writerow({'titolo':files_pdb[x]})
                titoli.writerow({'titolo': "Angoli_isole"})
                wr.writerow(angoli_isole_medio_distanza)
                titoli.writerow({'titolo':"Errori_Isole"})
                wr.writerow(angoli_isole_medio_std_della_media)

                titoli.writerow({'titolo':"Angoli_layers"})
                wr.writerow(angoli_layers_medio_distanza)
                titoli.writerow({'titolo':"Errori_layers"})
                wr.writerow(angoli_layers_medio_std_della_media)

                titoli.writerow({'titolo':"Angoli_rumore"})
                wr.writerow(angoli_rumore_medio_distanza)
                titoli.writerow({'titolo':"Errori_rumore"})
                wr.writerow(angoli_rumore_medio_std_della_media)
                csv_angoli.flush()
                #va a scrivere il txt che altrimenti sarebbe scritto totalmente alla fine
            if funzione_della_distanza_onoff == "OFF":
                """!!! STAMPA FILE ANGOLI DI OUTPUT, UNA RIGA PER INDICARE IL NOM DEL FILE,UNA RIGA PER IL TIPO DI CLUSTER, UNA RIGA L?ARRAY DELLA MEDIA,UNA PER GLI ERRORI !!!"""
                titoli.writerow({'titolo': files_pdb[x]})
                titoli.writerow({'titolo': "Angoli_isole"})
                titoli.writerow({'titolo': angoli_isole_medio_distanza})
                titoli.writerow({'titolo': "Errori_Isole"})
                titoli.writerow({'titolo': angoli_isole_medio_std_della_media})

                titoli.writerow({'titolo': "Angoli_layers"})
                titoli.writerow({'titolo':angoli_layers_medio_distanza})
                titoli.writerow({'titolo': "Errori_layers"})
                titoli.writerow({'titolo':angoli_layers_medio_std_della_media})

                titoli.writerow({'titolo': "Angoli_rumore"})
                titoli.writerow({'titolo':angoli_rumore_medio_distanza})
                titoli.writerow({'titolo': "Errori_rumore"})
                titoli.writerow({'titolo':angoli_rumore_medio_std_della_media})
                csv_angoli.flush()
                # va a scrivere il txt che altrimenti sarebbe scritto totalmente alla fine

        if funzione_della_distanza_onoff == "ON":
            """ !!! VADO A PLOTTARE I RISULTATI APPENA OTTENUTI IN TERMINE DI MEDIE DI ANGOLI IN FUNZIONE DELLA DISTANZA CON PYPLOT !!!"""
            # Valori di x
            distanza_asseX = np.arange(0.5, 19.5, 0.5)
            # Controllo il troncone sia per definire il nome dell'immagine ma anche per il titolo del grafico
            if (files_pdb[x])[-13:-4] == "300Msteps":
                terza_riga = "Primi 300M steps"
                troncone_numero = "1"
            if (files_pdb[x])[-17:-4] == "300+300Msteps":
                terza_riga = "Secondi 300M steps"
                troncone_numero = "2"
            nome_immagine = "Pressione_" + (files_pdb[x])[36:41] + "_Milliatmosfere" + "_Replica_" + cartella_e_nome_output[
                -1] + "_Troncone_" + troncone_numero
            path_output_immagini = path_plot_angoli_f_distanza + nome_immagine + ".png"
            # Vado a plottare isole,layers,rumore in un unico grafico, per ognuno di essi va inserita prima la X(distanza)
            # Gli ultimi tre parametri sono grafici, l'ultimo setta su non il "riempimento" dei simboli, che altrimenti sarebbero pieni

            "VADO A CREARE UN ARRAY DELLE SIZE DEI SIMBOLI IN FUNZIONE DEL NUMERO DI MOLECOLE PER SETTORE:" \
            "Ho tre liste, con un rumero di elementi pari al numero di sezioni della distanza, per ognuna di queste " \
            "sezioni uso np.count_nonzero(~np.isnan(angoli_isole_distanza_database[counter_plot_angoli])) per trovare" \
            "il numero di angoli non-nan in ogni sezione, quindi il numero di acque presenti"
            lista_size_marker_isole = []
            lista_size_marker_layers = []
            lista_size_marker_rumore = []
            counter_plot_angoli = 0
            for distanza_plot_angoli in np.arange(6.5, 25.5, 0.5):
                # lista_size_marker_isole.append([])
                lista_size_marker_isole.append(
                    np.count_nonzero(~np.isnan(angoli_isole_distanza_database[counter_plot_angoli])))
                # lista_size_marker_layers.append([])
                lista_size_marker_layers.append(
                    np.count_nonzero(~np.isnan(angoli_layers_distanza_database[counter_plot_angoli])))
                # lista_size_marker_rumore.append([])
                lista_size_marker_rumore.append(
                    np.count_nonzero(~np.isnan(angoli_rumore_distanza_database[counter_plot_angoli])))
                counter_plot_angoli += 1
            print(lista_size_marker_isole, lista_size_marker_layers, lista_size_marker_rumore)
            # Passaggi utili se si vuole scatter della dimensione
            """s = [i + 20 for i in lista_size_marker_isole ]
            s1 = [i + 20 for i in lista_size_marker_layers ]
            s2 = [i + 20 for i in lista_size_marker_rumore ]
            print(s,s1,s2)"""

            # Vado a creare delle colormap troncate, data la grande differenza tra i valori
            cmap_blu = plt.get_cmap('Blues')
            new_cmap_blu = truncate_colormap(cmap_blu, 0.2, 0.8)
            blu_standard = cmap_blu(0.8)
            cmap_rossa = plt.get_cmap('Oranges')
            new_cmap_rossa = truncate_colormap(cmap_rossa, 0.2, 0.8)
            rosso_standard = cmap_rossa(0.8)
            gs = gridspec.GridSpec(3, 1)
            fig = plt.figure(figsize=(8, 7))
            plt.subplot(gs[:2, :])
            # plt.plot(distanza_asseX, angoli_isole_medio_distanza,'bo', distanza_asseX, angoli_layers_medio_distanza, 'rs', distanza_asseX,
            #        angoli_rumore_medio_distanza, 'g+', linewidth=1, markersize=8, mfc='none')

            # Setto i limiti della colorbar(gli estremi, tutti i dati sopra/sotto tali limiti avranno il colore min e max) NON NORMALIZZA I DATI MA LA COLORBAR
            # Se voglio attivarlo devo impostare l'arg (di scatter)norm=normalize_isole
            normalize_isole = matplotlib.colors.Normalize(vmin=0., vmax=15000)
            """#Questo passaggio invece normalizza direttamenre i colori nell'intervallo desiderato, non serve a molto
            lista_size_marker_isole = np.array(lista_size_marker_isole)
            normalized = (lista_size_marker_isole - min(lista_size_marker_isole)) / (max(lista_size_marker_isole) - min(lista_size_marker_isole))"""
            plt.scatter(distanza_asseX, angoli_layers_medio_distanza, cmap=new_cmap_rossa, marker="o",
                        edgecolors='k', linewidths=0.1, s=200,c=lista_size_marker_layers,  alpha=1, norm=None)
            plt.scatter(distanza_asseX, angoli_isole_medio_distanza, marker="o", linewidths=0.1, s=150,
                        cmap=new_cmap_blu, c=lista_size_marker_isole, edgecolors='k', alpha=1, norm=None)
            plt.scatter(distanza_asseX, angoli_rumore_medio_distanza, marker="x", c="m", edgecolors='k',
                        linewidths=0.5, s=15, alpha=0.5)
            # L'immagine avrà una griglia tratteggiata
            plt.grid(True, linestyle='--', linewidth=0.5)
            # Setto i "divisori" in ogni asse,  con i relativi step ed eventuale rotazione(utile se ci sono sovrapposizioni)
            if unità_di_misura_angoli == "GRADI":
                plt.xticks(np.arange(0.5, 19.5, 1.0), rotation=30)
                plt.yticks(np.arange(0, 200, 20), rotation=0)
            if unità_di_misura_angoli == "COSENO":
                plt.xticks(np.arange(0.5, 19.5, 1.0), [], rotation=30)
                plt.yticks(np.arange(-1, 1.2, 0.2), rotation=0)
            # TITOLO
            """# Setto il titolo coincidente con quello del pdb,specificando la replica
            # Utilizzo la libreria wrap per wrappare il titolo con un massimo di 45 lettere per riga
            plt.title('\n'.join(wrap(cartella_e_nome_output + "_" + files_pdb[x],45)), fontsize=11, style='oblique',weight='heavy')"""
            # Faccio un titolo su tre righe, andando a specificare replica, pressione e troncone
            # Inizializzo le variabili delle tre righe
            prima_riga = "Pressione : " + (files_pdb[x])[36:41] + " Milliatmosfere"
            seconda_riga = "Replica : " + cartella_e_nome_output[-1]
            # Scrivo il titolo su tre righe - suptitle indica il titotolo dell'intera figura
            plt.suptitle(prima_riga + "\n" + seconda_riga + "\n" + terza_riga, fontsize=11, style='oblique',
                         weight='heavy')
            plt.title("(a)", loc="left")
            """#Imposto una proprietà degli assi, ovvero quella per cui i labels degli assi non iniziano/finiscono con i bordi
            #della "scatola"
            plt.axis(option='scaled')"""
            # Imposto i nomi assegnati ai vari simboli della legenda, l'ordine da seguire(nel caso di dati plottati) è
            # quello con cui sono inseriti in plt.plot(), vanno messi in un array
            # imposto la grandezza dei simboli che altrimenti si adegua a quello dei marker(quindi troppo grande)
            # imposto colore uguale alla cmap
            legend = plt.legend(['Layers', 'Isole', 'Rumore'], loc='upper right', scatterpoints=1)
            legend.legendHandles[0]._sizes = [200]
            legend.legendHandles[0].set_color(plt.cm.Oranges(.8))
            legend.legendHandles[1]._sizes = [150]
            legend.legendHandles[1].set_color(plt.cm.Blues(.8))
            legend.legendHandles[2]._sizes = [15]
            # Ridimensiono l'intera immagine per farla stare nell'immagine restituita come output
            # "pad" = Padding between the figure edge and the edges of subplots, as a fraction of the font size
            # plt.tight_layout(pad=3)
            # Setta i limiti degli assi(utile, xticks e yticks infatti settano le label ma non i limiti degli assi)
            if unità_di_misura_angoli == "GRADI":
                plt.xlim(0.5, 19.0)
                plt.ylim(0, 180)
            if unità_di_misura_angoli == "COSENO":
                plt.xlim(0.5, 19.0)
                plt.ylim(-1, 1)
            # Setto i titoli degli assi, wrap fa si che vada a capo da solo
            # plt.xlabel('Distanza dalla superficie di NaCl(Å)', wrap=True, fontsize=11, style='oblique')
            if unità_di_misura_angoli == "GRADI":
                plt.ylabel(
                    'θ(°)',
                    wrap=True, fontsize=11, style='oblique')
            if unità_di_misura_angoli == "COSENO":
                plt.ylabel(
                    'cosθ',
                    wrap=True, fontsize=11, style='oblique')
            # plt.savefig(path_output_immagini)
            # plt.close()

            """ !!! VADO A PLOTTARE I RISULTATI APPENA OTTENUTI IN TERMINE DI STD DI ANGOLI IN FUNZIONE DELLA DISTANZA CON PYPLOT !!!"""
            # Valori di x
            distanza_asseX = np.arange(0.5, 19.5, 0.5)
            # Controllo il troncone sia per definire il nome dell'immagine ma anche per il titolo del grafico
            """if (files_pdb[x])[-13:-4] == "300Msteps":
                terza_riga = "Primi 300M steps"
                troncone_numero = "1"
            if (files_pdb[x])[-17:-4] == "300+300Msteps":
                terza_riga = "Secondi 300M steps"
                troncone_numero = "2"
            nome_immagine = "Pressione_" + (files_pdb[x])[36:41] + "_Milliatmosfere" + "_Replica_" + \
                            cartella_e_nome_output[
                                -1] + "_Troncone_" + troncone_numero
            path_output_immagini = path_plot_angoli_f_distanza + nome_immagine + ".png" """
            # Vado a plottare isole,layers,rumore in un unico grafico, per ognuno di essi va inserita prima la X(distanza)
            # Gli ultimi tre parametri sono grafici, l'ultimo setta su non il "riempimento" dei simboli, che altrimenti sarebbero pieni
            plt.subplot(gs[2, :])
            fig.text(.1, .0005,
                     '\n'.join(wrap("(a) Angolo medio θ,(b) e relativo valore di deviazione standard, tra il vettore momento di dipolo dell'acqua ed il vettore normale alla superficie di NaCl(°), in funzione della distanza dalla superficie.",85))
                     + "\n" + "L'intensità del colore è proporzionale al numero di valori mediati."
                     , ha='left'
                     ,
                     wrap=True, fontsize=11, style='oblique',
                     weight='normal') #verticalalignment="bottom"
            plt.title("(b)", loc="left")
            plt.scatter(distanza_asseX, angoli_layers_medio_std, marker="o", facecolors=rosso_standard,
                        edgecolors='k', linewidths=0.5)
            plt.scatter(distanza_asseX, angoli_isole_medio_std, marker="o", facecolors=blu_standard,
                        edgecolors='k', linewidths=0.5)
            plt.scatter(distanza_asseX, angoli_rumore_medio_std, marker="x", facecolors='m', edgecolors='none',
                        s=15)
            # L'immagine avrà una griglia tratteggiata
            plt.grid(True, linestyle='--', linewidth=0.5)
            # Setto i "divisori" in ogni asse,  con i relativi step ed eventuale rotazione(utile se ci sono sovrapposizioni)
            if unità_di_misura_angoli == "GRADI":
                plt.xticks(np.arange(0.5, 19.5, 1.0), rotation=30)
                plt.yticks(np.arange(0, 100, 10), rotation=0)
            if unità_di_misura_angoli == "COSENO":
                plt.xticks(np.arange(0.5, 19.5, 1.0), rotation=30)
                plt.yticks(np.arange(0, 1.2, 0.2), rotation=0)
            # TITOLO
            """# Setto il titolo coincidente con quello del pdb,specificando la replica
            # Utilizzo la libreria wrap per wrappare il titolo con un massimo di 45 lettere per riga
            plt.title('\n'.join(wrap(cartella_e_nome_output + "_" + files_pdb[x],45)), fontsize=11, style='oblique',weight='heavy')"""
            # Faccio un titolo su tre righe, andando a specificare replica, pressione e troncone
            # Inizializzo le variabili delle tre righe
            prima_riga = "Pressione : " + (files_pdb[x])[36:41] + " Milliatmosfere"
            seconda_riga = "Replica : " + cartella_e_nome_output[-1]
            # Scrivo il titolo su tre righe
            # plt.title(prima_riga + "\n" + seconda_riga + "\n" + terza_riga, fontsize=11, style='oblique',weight='heavy')
            """#Imposto una proprietà degli assi, ovvero quella per cui i labels degli assi non iniziano/finiscono con i bordi
            #della "scatola"
            plt.axis(option='scaled')"""
            # Imposto i nomi assegnati ai vari simboli della legenda, l'ordine da seguire(nel caso di dati plottati) è
            # quello con cui sono inseriti in plt.plot(), vanno messi in un array
            # plt.legend(['Isole', 'Layers', 'Rumore'], loc='upper right')
            # Ridimensiono l'intera immagine per farla stare nell'immagine restituita come output
            # "pad" = Padding between the figure edge and the edges of subplots, as a fraction of the font size
            # fig.canvas.draw()

            # Setta i limiti degli assi(utile, xticks e yticks infatti settano le label ma non i limiti degli assi)
            if unità_di_misura_angoli == "GRADI":
                plt.xlim(0.5, 19.0)
                plt.ylim(0, 100)
            if unità_di_misura_angoli == "COSENO":
                plt.xlim(0.5, 19.0)
                plt.ylim(0, 1)
            # Setto i titoli degli assi, wrap fa si che vada a capo da solo
            plt.xlabel('Distanza dalla superficie di NaCl(Å)', wrap=True, fontsize=11, style='oblique')
            # Setta gli spazi ai lati della figura e tra i subplots(per questo poi viene corretto)
            fig.tight_layout(pad=5, w_pad=0, h_pad=0)
            # Setto le distanze tra i subplots
            plt.subplots_adjust(wspace=0, hspace=0.2)
            # plt.ylabel('Angolo medio tra il vettore momento di dipolo normalizzato acqua e vettore normale alla superficie di NaCl(°)',wrap=True, fontsize=11, style='oblique')
            # Vado a salvare la figura, eliminando gli spazi buoti con 'tight' e aggiungendo un piccolo spazio vuoto con
            # pad_inches
            print("5.8")
            plt.savefig(path_output_immagini, bbox_inches='tight', pad_inches=0.2, dpi=100)
            print("5.9")
            plt.close()
        elif funzione_della_distanza_onoff == "OFF":
            if (files_pdb[x])[-13:-4] == "300Msteps":
                terza_riga = "Primi 300M steps"
                troncone_numero = "1"
            if (files_pdb[x])[-17:-4] == "300+300Msteps":
                terza_riga = "Secondi 300M steps"
                troncone_numero = "2"
            nome_immagine = "Pressione_" + (files_pdb[x])[36:41] + "_Milliatmosfere" + "_Replica_" + cartella_e_nome_output[
                -1] + "_Troncone_" + troncone_numero


        if calcolo_angoli_onoff == "ON":
            if funzione_della_distanza_onoff == "ON":
                """VADO A STAMPARE IL FILE CON I DATI STATISTICI """
                """!!! STAMPA FILE ANGOLI DI OUTPUT, UNA RIGA PER INDICARE IL NOM DEL FILE,UNA RIGA PER IL TIPO DI CLUSTER, UNA RIGA L?ARRAY DELLA MEDIA,UNA PER GLI ERRORI !!!"""
                titoletto = "~" + nome_immagine
                titoletto1 = "Unità di misura angoli:" + unità_di_misura_angoli
                titoliStat.writerow({'titolo':(titoletto)})
                titoliStat.writerow({'titolo':(titoletto1)})
                titoliStat.writerow({'titolo': " "})
                titoliStat.writerow({'titolo': "-- ISOLE --"})
                titoliStat.writerow({'titolo': "Angoli media"})
                wrStat.writerow(angoli_isole_medio_distanza)
                titoliStat.writerow({'titolo':"Std della media"})
                wrStat.writerow(angoli_isole_medio_std_della_media)
                titoliStat.writerow({'titolo': "Std"})
                wrStat.writerow(angoli_isole_medio_std)
                titoliStat.writerow({'titolo': "Min"})
                wrStat.writerow(angoli_isole_medio_min)
                titoliStat.writerow({'titolo': "Max"})
                wrStat.writerow(angoli_isole_medio_max)
                titoliStat.writerow({'titolo': " "})

                titoliStat.writerow({'titolo':"-- LAYERS --"})
                titoliStat.writerow({'titolo': "Angoli media"})
                wrStat.writerow(angoli_layers_medio_distanza )
                titoliStat.writerow({'titolo': "Std della media"})
                wrStat.writerow(angoli_layers_medio_std_della_media )
                titoliStat.writerow({'titolo': "Std"})
                wrStat.writerow(angoli_layers_medio_std )
                titoliStat.writerow({'titolo': "Min"})
                wrStat.writerow(angoli_layers_medio_min )
                titoliStat.writerow({'titolo': "Max"})
                wrStat.writerow(angoli_layers_medio_max )
                titoliStat.writerow({'titolo': " "})

                titoliStat.writerow({'titolo':"-- RUMORE --"})
                titoliStat.writerow({'titolo': "Angoli media"})
                wrStat.writerow(angoli_rumore_medio_distanza)
                titoliStat.writerow({'titolo': "Std della media"})
                wrStat.writerow(angoli_rumore_medio_std_della_media)
                titoliStat.writerow({'titolo': "Std"})
                wrStat.writerow(angoli_rumore_medio_std)
                titoliStat.writerow({'titolo': "Min"})
                wrStat.writerow(angoli_rumore_medio_min)
                titoliStat.writerow({'titolo': "Max"})
                wrStat.writerow(angoli_rumore_medio_max)
                titoliStat.writerow({'titolo': " "})

                angoli_stat.flush()
            if funzione_della_distanza_onoff == "OFF":
                """VADO A STAMPARE IL FILE CON I DATI STATISTICI """
                """!!! STAMPA FILE ANGOLI DI OUTPUT, UNA RIGA PER INDICARE IL NOM DEL FILE,UNA RIGA PER IL TIPO DI CLUSTER, UNA RIGA L?ARRAY DELLA MEDIA,UNA PER GLI ERRORI !!!"""
                titoletto = "~" + nome_immagine
                titoletto1 = "Unità di misura angoli:" + unità_di_misura_angoli
                titoliStat.writerow({'titolo': (titoletto)})
                titoliStat.writerow({'titolo': (titoletto1)})
                titoliStat.writerow({'titolo': " "})
                titoliStat.writerow({'titolo': "-- ISOLE --"})
                titoliStat.writerow({'titolo': "Angoli media"})
                titoliStat.writerow({'titolo': angoli_isole_medio_distanza})
                titoliStat.writerow({'titolo': "Std della media"})
                titoliStat.writerow({'titolo': angoli_isole_medio_std_della_media})
                titoliStat.writerow({'titolo': "Std"})
                titoliStat.writerow({'titolo': angoli_isole_medio_std})
                titoliStat.writerow({'titolo': "Min"})
                titoliStat.writerow({'titolo': angoli_isole_medio_min})
                titoliStat.writerow({'titolo': "Max"})
                titoliStat.writerow({'titolo': angoli_isole_medio_max})
                titoliStat.writerow({'titolo': " "})

                titoliStat.writerow({'titolo': "-- LAYERS --"})
                titoliStat.writerow({'titolo': "Angoli media"})
                titoliStat.writerow({'titolo': angoli_layers_medio_distanza})
                titoliStat.writerow({'titolo': "Std della media"})
                titoliStat.writerow({'titolo': angoli_layers_medio_std_della_media})
                titoliStat.writerow({'titolo': "Std"})
                titoliStat.writerow({'titolo': angoli_layers_medio_std})
                titoliStat.writerow({'titolo': "Min"})
                titoliStat.writerow({'titolo': angoli_layers_medio_min})
                titoliStat.writerow({'titolo': "Max"})
                titoliStat.writerow({'titolo': angoli_layers_medio_max})
                titoliStat.writerow({'titolo': " "})

                titoliStat.writerow({'titolo': "-- RUMORE --"})
                titoliStat.writerow({'titolo': "Angoli media"})
                titoliStat.writerow({'titolo': angoli_rumore_medio_distanza})
                titoliStat.writerow({'titolo': "Std della media"})
                titoliStat.writerow({'titolo': angoli_rumore_medio_std_della_media})
                titoliStat.writerow({'titolo': "Std"})
                titoliStat.writerow({'titolo': angoli_rumore_medio_std})
                titoliStat.writerow({'titolo': "Min"})
                titoliStat.writerow({'titolo': angoli_rumore_medio_min})
                titoliStat.writerow({'titolo': "Max"})
                titoliStat.writerow({'titolo': angoli_rumore_medio_max})
                titoliStat.writerow({'titolo': " "})

                angoli_stat.flush()

        """!!! ISTOGRAMMI"""
        counter_istogrammi_angoli = 0
        if funzione_della_distanza_onoff == "ON" and calcolo_angoli_onoff == "ON":
            path_output_istogrammi_angoli = path_istogrammi + nome_immagine + "\\"
            "Copio il settore specifico(tramite il counter) del database degli angoli in un database1, " \
            "successivamente, vado a plottare selezioando come dati da plottare SOLO i non-nan del database1" \
            "imposto i weight, i quali permettono di ottenere una frequenza in termini di frazione di 1, imposto" \
            "quindi normed=0(o density è uguale) perchè è già normalizzato (quindi frazione di 1) " \
            "uso poi PercentFormatter(1) che trasforma in percentuale le frazioni di 1, il valore (1) inserito nella" \
            "parentesi, indica il valore di frequenza(prima della trasf) che indica il 100%, nel nostro caso 1 perchè" \
            "normalizzato"
            for distanza_istogrammi in np.arange(6.5, 25.5, 0.5):
                if unità_di_misura_angoli == "GRADI":
                    # ISOLE
                    angoli_isole_distanza_database1 = angoli_isole_distanza_database[counter_istogrammi_angoli]
                    plt.hist((angoli_isole_distanza_database1[~np.isnan(angoli_isole_distanza_database1)]), bins=18, range=(0, 190),
                             weights=np.ones(np.count_nonzero(
                                 ~np.isnan(angoli_isole_distanza_database[counter_istogrammi_angoli]))) / (
                                         np.count_nonzero(
                                             ~np.isnan(angoli_isole_distanza_database[counter_istogrammi_angoli]))),
                             density=0)
                    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                    plt.xticks(np.arange(0, 190, 10), rotation=30)
                    plt.xlabel('θ(°)')
                    plt.ylabel('Frequenza')
                    plt.tight_layout(pad=1)
                    plt.savefig(path_output_istogrammi_angoli + "Isole\\" + str(distanza_istogrammi - 6.0) + ".png")
                    plt.close()
                    # LAYERS
                    angoli_layers_distanza_database1 = angoli_layers_distanza_database[counter_istogrammi_angoli]
                    plt.hist((angoli_layers_distanza_database1[~np.isnan(angoli_layers_distanza_database1)]), bins=18, range=(0, 190),
                             weights=np.ones(np.count_nonzero(
                                 ~np.isnan(angoli_layers_distanza_database[counter_istogrammi_angoli]))) / (
                                         np.count_nonzero(
                                             ~np.isnan(angoli_layers_distanza_database[counter_istogrammi_angoli]))),
                             density=0)
                    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                    plt.xticks(np.arange(0, 190, 10), rotation=30)
                    plt.xlabel('θ(°)')
                    plt.ylabel('Frequenza')
                    plt.tight_layout(pad=1)
                    plt.savefig(path_output_istogrammi_angoli + "Layers\\" + str(distanza_istogrammi - 6.0) + ".png")
                    plt.close()
                    # RUMORE
                    angoli_rumore_distanza_database1 = angoli_rumore_distanza_database[counter_istogrammi_angoli]
                    plt.hist((angoli_rumore_distanza_database1[~np.isnan(angoli_rumore_distanza_database1)]), bins=18, range=(0, 190),
                             weights=np.ones(np.count_nonzero(
                                 ~np.isnan(angoli_rumore_distanza_database[counter_istogrammi_angoli]))) / (
                                         np.count_nonzero(
                                             ~np.isnan(angoli_rumore_distanza_database[counter_istogrammi_angoli]))),
                             density=0)
                    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                    plt.xticks(np.arange(0, 190, 10), rotation=30)
                    plt.xlabel('θ(°)')
                    plt.ylabel('Frequenza')
                    plt.tight_layout(pad=1)
                    plt.savefig(path_output_istogrammi_angoli + "Rumore\\" + str(distanza_istogrammi - 6.0) + ".png")
                    plt.close()
                    counter_istogrammi_angoli += 1

                if unità_di_misura_angoli == "COSENO":
                    # ISOLE
                    angoli_isole_distanza_database1 = angoli_isole_distanza_database[counter_istogrammi_angoli]
                    plt.hist((angoli_isole_distanza_database1[~np.isnan(angoli_isole_distanza_database1)]), bins=20,
                             range=(-1., 1.),
                             weights=np.ones(np.count_nonzero(
                                 ~np.isnan(angoli_isole_distanza_database[counter_istogrammi_angoli]))) / (
                                         np.count_nonzero(
                                             ~np.isnan(angoli_isole_distanza_database[counter_istogrammi_angoli]))),
                             density=0)
                    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                    plt.xticks(np.arange(-1, 1.2, 0.2), rotation=30)
                    plt.xlabel('cosθ')
                    plt.ylabel('Frequenza')
                    plt.tight_layout(pad=1)
                    plt.savefig(path_output_istogrammi_angoli + "Isole\\" + str(distanza_istogrammi - 6.0) + ".png")
                    plt.close()
                    # LAYERS
                    angoli_layers_distanza_database1 = angoli_layers_distanza_database[counter_istogrammi_angoli]
                    plt.hist((angoli_layers_distanza_database1[~np.isnan(angoli_layers_distanza_database1)]), bins=20,
                             range=(-1., 1.),
                             weights=np.ones(np.count_nonzero(
                                 ~np.isnan(angoli_layers_distanza_database[counter_istogrammi_angoli]))) / (
                                         np.count_nonzero(
                                             ~np.isnan(angoli_layers_distanza_database[counter_istogrammi_angoli]))),
                             density=0)
                    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                    plt.xticks(np.arange(-1, 1.2, 0.2), rotation=30)
                    plt.xlabel('cosθ')
                    plt.ylabel('Frequenza')
                    plt.tight_layout(pad=1)
                    plt.savefig(path_output_istogrammi_angoli + "Layers\\" + str(distanza_istogrammi - 6.0) + ".png")
                    plt.close()
                    # RUMORE
                    angoli_rumore_distanza_database1 = angoli_rumore_distanza_database[counter_istogrammi_angoli]
                    plt.hist((angoli_rumore_distanza_database1[~np.isnan(angoli_rumore_distanza_database1)]), bins=20,
                             range=(-1., 1.),
                             weights=np.ones(np.count_nonzero(
                                 ~np.isnan(angoli_rumore_distanza_database[counter_istogrammi_angoli]))) / (
                                         np.count_nonzero(
                                             ~np.isnan(angoli_rumore_distanza_database[counter_istogrammi_angoli]))),
                             density=0)
                    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                    plt.xticks(np.arange(-1, 1.2, 0.2), rotation=30)
                    plt.xlabel('cosθ')
                    plt.ylabel('Frequenza')
                    plt.tight_layout(pad=1)
                    plt.savefig(path_output_istogrammi_angoli + "Rumore\\" + str(distanza_istogrammi - 6.0) + ".png")
                    plt.close()
                    counter_istogrammi_angoli += 1

        if funzione_della_distanza_onoff == "OFF" and calcolo_angoli_onoff == "ON":
            if unità_di_misura_angoli == "GRADI":
                path_output_istogrammi_angoli = path_istogrammi
                # ISOLE
                plt.hist((angoli_isole_distanza_database), bins=18, range=(0, 190), weights= np.ones(len(angoli_isole_distanza_database)) / len(angoli_isole_distanza_database))
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.xticks(np.arange(0, 190, 10), rotation=30)
                plt.xlabel('θ(°)')
                plt.ylabel('Frequenza(%)')
                plt.tight_layout(pad=1)
                plt.savefig(path_output_istogrammi_angoli + "Isole\\" + nome_immagine + ".png")
                plt.close()
                # LAYERS
                plt.hist((angoli_layers_distanza_database), bins=18, range=(0, 190), weights= np.ones(len(angoli_layers_distanza_database)) / len(angoli_layers_distanza_database))
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.xticks(np.arange(0, 190, 10), rotation=30)
                plt.xlabel('θ(°)')
                plt.ylabel('Frequenza(%)')
                plt.tight_layout(pad=1)
                plt.savefig(path_output_istogrammi_angoli + "Layers\\" + nome_immagine + ".png")
                plt.close()
                # RUMORE
                plt.hist((angoli_rumore_distanza_database), bins=18, range=(0, 190), weights= np.ones(len(angoli_rumore_distanza_database)) / len(angoli_rumore_distanza_database))
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.xticks(np.arange(0, 190, 10), rotation=30)
                plt.xlabel('θ(°)')
                plt.ylabel('Frequenza(%)')
                plt.tight_layout(pad=1)
                plt.savefig(path_output_istogrammi_angoli + "Rumore\\" + nome_immagine + ".png")
                plt.close()
                counter_istogrammi_angoli += 1
            if unità_di_misura_angoli == "COSENO":
                path_output_istogrammi_angoli = path_istogrammi
                # ISOLE
                plt.hist((angoli_isole_distanza_database), bins=20, range=(-1.,1.),
                         weights=np.ones(len(angoli_isole_distanza_database)) / len(angoli_isole_distanza_database))
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.xticks(np.arange(-1, 1.2, 0.2), rotation=30)
                plt.xlabel('cosθ')
                plt.ylabel('Frequenza(%)')
                plt.tight_layout(pad=1)
                plt.savefig(path_output_istogrammi_angoli + "Isole\\" + nome_immagine + ".png")
                plt.close()
                # LAYERS
                plt.hist((angoli_layers_distanza_database), bins=20, range=(-1.,1.),
                         weights=np.ones(len(angoli_layers_distanza_database)) / len(angoli_layers_distanza_database))
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.xticks(np.arange(-1, 1.2, 0.2), rotation=30)
                plt.xlabel('cosθ')
                plt.ylabel('Frequenza(%)')
                plt.tight_layout(pad=1)
                plt.savefig(path_output_istogrammi_angoli + "Layers\\" + nome_immagine + ".png")
                plt.close()
                # RUMORE
                plt.hist((angoli_rumore_distanza_database), bins=20, range=(-1.,1.),
                         weights=np.ones(len(angoli_rumore_distanza_database)) / len(angoli_rumore_distanza_database))
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.xticks(np.arange(-1, 1.2, 0.2), rotation=30)
                plt.xlabel('cosθ')
                plt.ylabel('Frequenza(%)')
                plt.tight_layout(pad=1)
                plt.savefig(path_output_istogrammi_angoli + "Rumore\\" + nome_immagine + ".png")
                plt.close()
                counter_istogrammi_angoli += 1


stop = timeit.default_timer()
print('Tempo totale di esecuzione: ', (stop - start)/60,'minuti.')