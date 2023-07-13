import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt

points = np.array([[-1, -1, -1],
                  [1, -1, -1 ],
                  [1, 1, -1],
                  [-1, 1, -1],
                  [-1, -1, 1],
                  [1, -1, 1 ],
                  [1, 1, 1],
                  [-1, 1, 1]])

P = [[2.06498904e-01 , -6.30755443e-07 ,  1.07477548e-03],
 [1.61535574e-06 ,  1.18897198e-01 ,  7.85307721e-06],
 [7.08353661e-02 ,  4.48415767e-06 ,  2.05395893e-01]]

Z = np.zeros((8,3)) #otto vertici tre coordinate, crea array vuot odi coordinate
for i in range(8): Z[i,:] = np.dot(points[i,:],P)
print(Z)
Z = 10.0*Z
print(Z)

fig = plt.figure(figsize=plt.figaspect(1)*1.5)
ax = fig.add_subplot(111, projection='3d')

r = [-1,1]

X, Y = np.meshgrid(r, r)
# plot vertices
ax.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])

# list of sides' polygons of figure
verts = [[points[0],points[1],points[2],points[3]],
 [points[4],points[5],points[6],points[7]],
 [points[0],points[1],points[5],points[4]],
 [points[2],points[3],points[7],points[6]],
 [points[1],points[2],points[6],points[5]],
 [points[4],points[7],points[3],points[0]]]

# plot sides
ax.add_collection3d(Poly3DCollection(verts,
 facecolors='cyan', linewidths=1, edgecolors='black', alpha=.25))

ax.set_xlabel('X(Å)')
ax.set_ylabel('Y(Å)')
ax.set_zlabel('Z(Å)')
ax.view_init(20,-120)
#plt.axis('off')

ax.grid(True)
plt.show()
print('ax.azim {}'.format(ax.azim))
print('ax.elev {}'.format(ax.elev))