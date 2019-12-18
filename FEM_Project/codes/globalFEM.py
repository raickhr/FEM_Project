import numpy as np

def assembleKmatrix(elementList, numNodes):
    matsize = 2*numNodes
    global_Kmat = np.zeros((matsize,matsize), dtype=float)

    for element in elementList:
        nodeIDList = element.node_ID_list
        nodeIndxList = [nodeID - 1 for nodeID in nodeIDList]

        elementKmat = element.Kmatrix

        globalKmat_u_indx = [2*nodeIndx for nodeIndx in nodeIndxList]
        globalKmat_v_indx = [2*nodeIndx+1 for nodeIndx in nodeIndxList]

        for i in range(4):
            u_indx = globalKmat_u_indx[i]

            for j in range(4):                
                v_indx = globalKmat_v_indx[j]
                
                global_Kmat[u_indx, v_indx-1] += elementKmat[i*2,j*2]
                global_Kmat[u_indx, v_indx] += elementKmat[i*2, j*2+1]

                global_Kmat[u_indx+1, v_indx-1] += elementKmat[i*2+1, j*2]
                global_Kmat[u_indx+1, v_indx] += elementKmat[i*2+1, j*2+1]

    return global_Kmat

def solveFEM(globalK, BC_cond, Loads):
    mask_ind = [i for i in range(len(BC_cond)) if BC_cond[i] == True]
    subKmat = np.delete(globalK, mask_ind, axis=0)
    subKmat = np.delete(subKmat, mask_ind, axis=1)
    subLoad = np.delete(Loads,mask_ind, axis=0)
    invSubKmat = np.linalg.inv(subKmat)
    dis = np.matmul(invSubKmat,subLoad)
    dis = list(dis)
    for i in mask_ind:
        dis.insert(i,0)

    return np.array(dis)
    





