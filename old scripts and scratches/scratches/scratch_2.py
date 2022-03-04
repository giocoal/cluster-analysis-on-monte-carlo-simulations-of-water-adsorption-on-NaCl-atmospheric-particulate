import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
data_solo_ossigeno = np.array([[1,3,2],[1,4,2],[4,1,2],[1,7,4],[3,3,2],[5,1,2],[4,4,2]])
matplotlib.use('Qt5Agg')

fig = plt.figure()
ax = Axes3D(fig)
ax.set_xlim3d(-19.803, 19.803)
ax.set_ylim3d(-19.803, 19.803)
ax.set_zlim3d(-25, +25)
ax.scatter(data_solo_ossigeno[:, 0], data_solo_ossigeno[:, 1], data_solo_ossigeno[:, 2], s=150)
ax.view_init(elev=90,azim=90)
plt.show()