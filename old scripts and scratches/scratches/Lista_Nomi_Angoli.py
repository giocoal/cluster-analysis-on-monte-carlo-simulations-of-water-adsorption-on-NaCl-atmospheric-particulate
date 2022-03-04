import numpy as np
import pandas as pd

#Vado a definire un ciclo che crea un'array contenente i nomi delle righe associate agli angoli(per le acque) ad una determinata
#Distanza dalla superficie di NaCl(sapendo che la superficie è a circa 6 A dallo 0 ed il massimo valore raggiungibile è
#25 (dimensioni del box è 50 su z), gli step sono di 0.5, questo significa che tutto ciò che si trova tra
#ad esempio, 6.5 e 7, sarà assegnato alla posizione 7, ma indicherà che si trova tra la posizione 7 e quella precedente
distanza_da_superficie = pd.Series([1,2,3,4,5])
"""for distanza in pd.range(6.5,25.5,0.5):
    distanza_da_superficie = pd.DataFrame.append(distanza_da_superficie, distanza)
print(distanza_da_superficie)"""

#Ora genero un dataframe di pandas, per ogni tipologia di cluster(quindi 3:isole,layers,noise), ogni riga conterrà
#Gli angoli delle acque ad una certa distanza dalla superficie, l'unica differenza dal caso non dipendente da z
#E' quindi che ho una matrice di angoli e non un array

angoli_isole_dataframe = pd.DataFrame(index=distanza_da_superficie)
print(angoli_isole_dataframe)
angoli_isole_dataframe.iloc[0,:] = pd.DataFrame.append(angoli_isole_dataframe.iloc[0,:],distanza_da_superficie[:],ignore_index=True)
print(angoli_isole_dataframe)