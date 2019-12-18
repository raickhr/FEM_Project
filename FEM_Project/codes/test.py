import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.path as mpath

x = np.arange(0,1,0.1)
dx = 0.1
dt = 0.0000025

T = np.ones((10,) , dtype=float) *10

Tnp1 = np.ones((10,), dtype=float)

for i in range(1000):
     for j in range(1,10-1):
          Tnp1[j] = 5*((T[j-1]-2*T[j] + T[j+1])/dx**2 )*dt + T[j]
     Tnp1[0] = Tnp1[1]
     Tnp1[-1] = 0
     T = Tnp1

plt.plot(Tnp1)
plt.show()