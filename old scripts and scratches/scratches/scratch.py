import numpy as np

#MODIFICHE DA APPLICARE ALLA FUNZIONE CALCOLO_ANGOLO PER RENDERLA ADATTA AL CALCOLO DIFFERENZIATO IN FUNZIONE DI Z

"""#Creo una lista vuota che ospiterà gli angoli delle isole(aggiungere quelli dei layers e noise)"""
lista_liste_angoli_isole = []
lista_liste_angoli_layer = []
lista_liste_angoli_rumore = []
"""#Ottengo dalla lista una LISTA DI LISTE, ogni lista conterrà gli angoli per le molecole d'acqua a diverse distanze dalla
#superficie, a step di 0.5 (ipotizzando che la superficie sia a 6.0 A),l'algoritmo riconosce il numero di settori
da creare sulla base dell'inizio e la fine dell'area da suddividere e della lunghezza dello step"""
#Praticamente poi si suddivide z in tanti "settori" lunghi 0.5 A, gli angoli delle molecole d'acqua appartenenti ad un
#Determinato settore saranno assegnate ad un valore di distanza corrispondente al limite massimo del settore
#questo significa che tutto ciò che si trova tra
#ad esempio, 6.5 e 7, sarà assegnato alla posizione 7, ma indicherà che si trova tra la posizione 7 e quella precedente
for i in np.arange(6.5,25.5,0.5):
    lista_liste_angoli_isole.append([])
    lista_liste_angoli_layer.append([])
    lista_liste_angoli_rumore.append([])
O = [0,1,-23.2]
#Creo il ciclo for che, dato un angolo per un'acqua specifica, determinerà a quale "settore di distanza" appartiene,
#Sulla base della posizione di O, andando quindi ad aggiungere il valore dell'angolo alla lista corrispondente
contatore_settore = 0
for distanza_max in np.arange(6.5,25.5,0.5):
    print(distanza_max)
    # Viene utilizzato il valore assoluto abs() perchè abbiamo una funzione della distanza assoluta
    if (abs(O[2]) < distanza_max) & (abs(O[2]) > (distanza_max-0.5)):
        lista_liste_angoli_isole[contatore_settore].append(60)
        break
    contatore_settore += 1
    print("Distanza non è",distanza_max)
print("distanza è",distanza_max)
print(lista_liste_angoli_isole)
pad = len(max(lista_liste_angoli_isole, key=len))
array = np.array([i + [float('nan')]*(pad-len(i)) for i in lista_liste_angoli_isole])
print(array)

"LO SCRIPT RICONOSCE CORRETTAMENTE IL SETTORE DI APPARTENENZA(in termini di distanza dalla superficie)" \
"aggiunge l'angolo alla lista corrispondente(tramite l'apposito contatore)" \
" ed in seguito ferma il ciclo for, nell'esempio restituisce il" \
"valore dell'estremo superiore del settore."