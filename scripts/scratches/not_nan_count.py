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
from textwrap import wrap

data = np.array([[1,33,24,float("nan"),4,float("nan")],[float("nan"),4,float("nan"),float("nan"),float("nan"),float("nan"),],[24,24,24,24,24,24]])
print(np.count_nonzero(~np.isnan(data[0])))
print(np.count_nonzero(~np.isnan(data[1])))
print(np.count_nonzero(~np.isnan(data[2])))
data1 = data[0]
print(data[0,~np.isnan(data)])
