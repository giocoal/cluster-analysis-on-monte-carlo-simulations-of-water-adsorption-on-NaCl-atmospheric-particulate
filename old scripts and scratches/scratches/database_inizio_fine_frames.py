import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist, squareform
import csv
import os
import pandas as pd
total_frames_plus = 3001
path = "C:\\Users\\Giorgio\\Desktop\\Tirocinio\\Dati\\Test\\BioPython\\Replica1_7.750matm_300+300Msteps_SoloOssigeno.pdb"
inizio_fine_frames_database = np.array([])

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


for count in range(1,total_frames_plus):  # devo trovare il numero di MODEL, il range superiore è il NUMERO TOTALE DI FRAME+1
    print("Frame" + str(count))
    if count < 9:
        inizio_frame = "MODEL     " + str(count)
        count += 1
        fine_frame = "MODEL     " + str(count)
    elif count == 9:
        inizio_frame = "MODEL     " + str(count)
        count += 1
        fine_frame = "MODEL    " + str(count)
    elif count < 99:
        inizio_frame = "MODEL    " + str(count)
        count += 1
        fine_frame = "MODEL    " + str(count)
    elif count == 99:
        inizio_frame = "MODEL    " + str(count)
        count += 1
        fine_frame = "MODEL   " + str(count)
    elif count < 999:
        inizio_frame = "MODEL   " + str(count)
        count += 1
        fine_frame = "MODEL   " + str(count)
    elif count == 999:
        inizio_frame = "MODEL   " + str(count)
        count += 1
        fine_frame = "MODEL  " + str(count)
    else:
        inizio_frame = "MODEL  " + str(count)
        count += 1
        fine_frame = "MODEL  " + str(count)
    print(inizio_frame)
    with open(path) as myFile:
        for num, line in enumerate(myFile, 1):
            if inizio_frame in line:
                print("found at line:" + str(num))
