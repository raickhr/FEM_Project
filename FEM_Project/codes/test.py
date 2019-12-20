import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.path as mpath

x= np.array([0.0, 0.2,0.4,0.6,0.8,1.0])
y = np.array([0.186552,
              0.340269,
              0.255052,
              0.152271,
              0.0616277,
              0.00422811])

plt.plot(x,y)
plt.xlabel('Radius')
plt.ylabel('Y-Reaction')
plt.title('Vertical Reaction on base support')
plt.show()
