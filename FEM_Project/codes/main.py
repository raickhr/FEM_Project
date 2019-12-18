from inputOutput import *
from errorMsg import *
from plotting import *
from globalFEM import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--inputDir', help=" Location of input folder ", type=str, default='../input')
parser.add_argument(
    '--integration', help="Integraion type, give 'reduced' or 'full' ", type=str, default='full')

args = parser.parse_args()

#input arguments
inputDir = args.inputDir
integration = args.integration

scale = 500000000 # this value is used so that the deformed shape is seen in the loads in example 

### READING ELEMENTS 
elements, nodeList = readElements(inputDir)
num_Nodes = len(nodeList)

### READING MATERIAL PROPERTIES
t, E, nu = readMatProp(inputDir)

### CALCULATING K matrix for each element
# 
printProgressMSG('\nTrying to calculate Kmatrix for each element ... ')
for i in range(len(elements)):
    if integration== 'reduced':
        elements[i].calcReducedKmatrix(t, E, nu)
        scale = 70000000
    else:
        elements[i].calcFullIntKmatrix(t, E, nu)

### ASSEMBLING K matrix

printProgressMSG('\nAssembling Kmatrix ... ')
globalK = assembleKmatrix(elements,num_Nodes )

printProgressMSG('\nGlobal Kmatrix calculated ... ')

#### READING BOUNDARY CONDTIONS

B_cond, fixed_nodes, X_fixed_nodes, Y_fixed_nodes\
     = readBC(inputDir,nodeList)

### READING LOADING CONDITIONS

Loads = readLoads(inputDir, num_Nodes)

### SOLVING FEM

result = solveFEM(globalK,B_cond,Loads)
fullLoads = np.matmul(globalK,result)  ## to get reaction forces

Y_reaction_node_indx = [node.nodeID-1 for node in Y_fixed_nodes]
Y_indices = 2*np.array(Y_reaction_node_indx)+1
Y_reaction = [fullLoads[index] for index in Y_indices]
x_y_of_Y_reaction_nodes = [[node.x, node.y] for node in Y_fixed_nodes]

X_reaction_node_indx = [node.nodeID-1 for node in X_fixed_nodes]
X_indices = 2*np.array(X_reaction_node_indx)
X_reaction = [fullLoads[index] for index in X_indices]
x_y_of_X_reaction_nodes = [[node.x, node.y] for node in X_fixed_nodes]

fixed_node_indx = [node.nodeID-1 for node in fixed_nodes]
X_indices = 2*np.array(fixed_node_indx)
X_reaction += [fullLoads[index] for index in X_indices]

Y_indices = 2*np.array(fixed_node_indx)+1
Y_reaction += [fullLoads[index] for index in Y_indices]

x_y_of_fixed_nodes = [[node.x, node.y] for node in fixed_nodes]
x_y_of_X_reaction_nodes += x_y_of_fixed_nodes
x_y_of_Y_reaction_nodes += x_y_of_fixed_nodes
result = result.reshape(num_Nodes, 2)

for i in range(len(elements)):
    elements[i].assignUVdisp(result)
    elements[i].calc_Fields(E, nu, scale=scale)

ax = plt.subplot(1,1,1)
plotElementUnDeformed(elements,ax)
plt.title('Undeformed Shape')
plt.show()

ax1 = plt.subplot(2, 3, 1)
pltElements(elements, ax1, field='strain_x', scale=scale)
plt.colorbar()
plt.title('Strain_xx')

ax2 = plt.subplot(2, 3, 2)
pltElements(elements, ax2, field='strain_y', scale=scale)
plt.colorbar()
plt.title('Strain_yy')

ax3 = plt.subplot(2, 3, 3)
pltElements(elements, ax3, field='strain_xy', scale=scale)
plt.colorbar()
plt.title('Strain_xy')

ax1 = plt.subplot(2, 3, 4)
pltElements(elements, ax1, field='stress_x', scale=scale)
plt.colorbar()
plt.title('Stress_xx')

ax2 = plt.subplot(2, 3, 5)
pltElements(elements, ax2, field='stress_y', scale=scale)
plt.colorbar()
plt.title('Stress_yy')

ax3 = plt.subplot(2, 3, 6)
pltElements(elements, ax3, field='stress_xy', scale=scale)
plt.colorbar()
plt.title('Stress_xy')

plt.show()

ax1 = plt.subplot(2, 3, 1)
pltElements(elements, ax1, field='disp_x', scale=scale)
plt.colorbar()
plt.title('Displacement in x direction')

ax2 = plt.subplot(2, 3, 2)
pltElements(elements, ax2, field='disp_y', scale=scale)
plt.colorbar()
plt.title('Displacement in y direction')

ax3 = plt.subplot(2, 3, 3)
pltElements(elements, ax3, field='disp_mag', scale=scale)
plt.colorbar()
plt.title('Magnitude of Displacement')

plt.show()

x = np.array(x_y_of_Y_reaction_nodes)[:,0]
plot_data=np.stack((x,np.array(Y_reaction)),axis=1)

plot_data = plot_data[plot_data[:,0].argsort()]


plt.plot(plot_data[:, 0], plot_data[:, 1])
plt.xlabel('Radius')
plt.ylabel('Y-Reaction')
plt.title('Vertical Reaction on base support')
plt.show()


# print('After Sorting')
# for i in range(len(coords)):
#     print(coords[i].nodeID, coords[i].x, coords[i].y)
