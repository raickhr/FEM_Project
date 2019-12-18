import sys
import os
from errorMsg import *
from objects import *

def readNodeID(inputLocation):
    fileName = 'nodeid.txt'
    fullPath = inputLocation+'/'+fileName
    nodeID_list = []
    try:
        printProgressMSG('\nTrying to read node ID file ... ')
        with open(fullPath) as fh:
            for line in fh:
                line=line.strip()
                if not line or line.startswith('%'):
                    continue
                nodeid = int(line)
                nodeID_list.append(nodeid)
                #print(nodeid)
        printSuccessMSG(str(len(nodeID_list)) + ' node id found')
        return nodeID_list

    except:
        if os.path.exists(fullPath):
            printERR_MSG('CHECK "nodeid.txt" FILE')
            sys.exit(1)
        else:
            printERR_MSG('ERROR!! File '+fullPath+' not found!!!')
            sys.exit(1)


def readCoord(inputLocation):
    fileName = 'coord.txt'
    fullPath = inputLocation+'/'+fileName
    nodeID_list = readNodeID(inputLocation)
    coord_list = []
    try:
        printProgressMSG('\nTrying to read co-ordinates file ... ')
        with open(fullPath) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('%'):
                    continue
                line = line.replace(',', ' ')
                line = line.replace(';',' ')
                xyz = line.split()
                if len(xyz) == 2:
                    x = float(xyz[0])
                    y = float(xyz[1])
                    readPoint = point(x,y)
                    coord_list.append(readPoint)
                else:
                    printERR_MSG('The co-ordinates should be in x,y format')
                    os.exit(1)
        numNodeID = len(coord_list)
        numCoord = len(nodeID_list)
        if numCoord == numNodeID:
            for i in range(numCoord):
                coord_list[i].assignNodeID(nodeID_list[i])
        else:
            printERR_MSG('Length of node ID list and co-ordinate list mismatch')
            sys.exit(1)
                
        printSuccessMSG(str(numNodeID) + ' nodes created ')
        return coord_list
                
    except:
        if os.path.exists(fullPath):
            printERR_MSG('CHECK "coord.txt" FILE')
            sys.exit(1)
        else:
            printERR_MSG('ERROR!! File '+fullPath+' not found!!!')
            sys.exit(1)


def readElementID(inputLocation):
    fileName = 'elementid.txt'
    fullPath = inputLocation+'/'+fileName
    elementID_list = []
    try:
        printProgressMSG('\nTrying to read elements ID file ... ')
        with open(fullPath) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('%'):
                    continue
                readelemID = int(line)
                elementID_list.append(readelemID)

        printSuccessMSG(str(len(elementID_list)) + ' element IDs found')
        return elementID_list

    except:
        if os.path.exists(fullPath):
            printERR_MSG('CHECK "elementid.txt" FILE')
            sys.exit(1)
        else:
            printERR_MSG('ERROR!! File '+fullPath+' not found!!!')
            sys.exit(1)

#########################################################################
#
#   functions for quicksort copied from :
#   https://www.geeksforgeeks.org/python-program-for-quicksort/
#
#########################################################################
def partition(arr, start_index, end_index, nodeORelem):
    i = (start_index-1)         # index of smaller element
    pivot = arr[end_index]     # pivot

    for j in range(start_index, end_index):

        # If current element is smaller than or
        # equal to pivot
        if nodeORelem == 'node':
            compare = arr[j].nodeID
            pivotCompare = pivot.nodeID

        elif nodeORelem == 'elem':
            compare = arr[j].elemID
            pivotCompare = pivot.elemID
        
        if compare <= pivotCompare:

            # increment index of smaller element
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i+1], arr[end_index] = arr[end_index], arr[i+1]
    return (i+1)

# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# start_index  --> Starting index,
# end_index  --> Ending index

# Function to do Quick sort


def quickSort(arr, start_index, end_index, nodeORelem):
    if start_index < end_index:

        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, start_index, end_index, nodeORelem)

        # Separately sort elements before
        # partition and after partition
        quickSort(arr, start_index, pi-1, nodeORelem)
        quickSort(arr, pi+1, end_index, nodeORelem)

######################################################
#
#    Copied portion ends 
#
######################################################
def sortCoordAccToNodeID(coords):
    n = len(coords)
    quickSort(coords, 0, n-1,'node')
    return coords

def readElements(inputLocation):
    fileName = 'elemconn.txt'
    fullPath = inputLocation+'/'+fileName

    ### array for storing coordinates
    coord_list = readCoord(inputLocation)

    ### sorting coordinates according to node objects
    coord_list = sortCoordAccToNodeID(coord_list)
    num_Nodes = len(coord_list)

    ### array to find out corner nodes, border nodes and interior nodes
    nodeTOelem = np.zeros(num_Nodes,dtype=int)
    numCornerNodes = 0
    numBorderNodes = 0
    numInteriorNodes = 0

    ### array for storing element ID 
    elementID_list = readElementID(inputLocation)

    ### array for storing element objects
    element_list = []
    
    try:
        printProgressMSG('\nTrying to read element connection file ... ')
        with open(fullPath) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('%'):
                    continue
                line = line.replace(',', ' ')
                line = line.replace(';', ' ')
                xyz = line.split()
                if len(xyz) == 4:
                    n1 = int(xyz[0])
                    n2 = int(xyz[1])
                    n3 = int(xyz[2])
                    n4 = int(xyz[3])

                    nodeIDList = [n1, n2, n3, n4] 

                    indexList = [nodeID-1 for nodeID in nodeIDList]

                    nodeTOelem[n1 - 1] += 1
                    nodeTOelem[n2 - 1] += 1
                    nodeTOelem[n3 - 1] += 1
                    nodeTOelem[n4 - 1] += 1

                    Q4_coordList = [coord_list[index] for index in indexList ]

                    ### creating instance of element object
                    element = Q4_element(Q4_coordList)
                    element_list.append(element)
                else:
                    printERR_MSG(
                        'The node id should be in node1, node2, node3, node4 format')
                    os.exit(1)
        numElementID = len(elementID_list)
        numElements = len(element_list)
        for i in range(num_Nodes):
            if nodeTOelem[i] == 1:
                numCornerNodes += 1
            elif nodeTOelem[i] == 2:
                numBorderNodes += 1
            else:
                numInteriorNodes += 1

        if numElements == numElementID:
            for i in range(numElements):
                element_list[i].assignElemID(elementID_list[i])
        else:
            printERR_MSG(
                'Length of element ID list and element connection list mismatch')
            sys.exit(1)

        printSuccessMSG(str(len(elementID_list)) + ' elements created')
        printSuccessMSG(str(numCornerNodes) + ' corner nodes ')
        printSuccessMSG(str(numBorderNodes) + ' border nodes')
        printSuccessMSG(str(numInteriorNodes) + ' interior nodes')

        return element_list, coord_list

    except:
        if os.path.exists(fullPath):
            printERR_MSG('CHECK "elemconn.txt" FILE')
            sys.exit(1)
        else:
            printERR_MSG('ERROR!! File '+fullPath+' not found!!!')
            sys.exit(1)


def readMatProp(inputLocation):
    fileName = 'matprop.txt'
    fullPath = inputLocation+'/'+fileName
    t = 0
    E = 0
    nu =0

    try:
        printProgressMSG('\nTrying to read Material Properties file ... ')
        with open(fullPath) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('%'):
                    continue
                line = line.replace(',', ' ')
                line = line.replace(';', ' ')
                xyz = line.split()
                if len(xyz) == 3:
                    t = float(xyz[0])
                    nu = float(xyz[1])
                    E = float(xyz[2])
                else:
                    printERR_MSG('The Material Properties should be in thickness, nu, E format')
                    os.exit(1)
        printSuccessMSG(' Thickness :' + str(t))
        printSuccessMSG(" Young's Modulus :" +str(E))
        printSuccessMSG(" Poisson's ratio :" +str(nu))
        return t, E, nu
    except:
        if os.path.exists(fullPath):
            printERR_MSG('CHECK "matprop.txt" FILE')
            sys.exit(1)
        else:
            printERR_MSG('ERROR!! File '+fullPath+' not found!!!')
            sys.exit(1)


def readBC(inputLocation,nodeList):
    fileName = 'bc_code.txt'
    fullPath = inputLocation+'/'+fileName
    num_Nodes = len(nodeList)
    BC_list = []
    fixed_nodes = []
    X_fixed_nodes = []
    Y_fixed_nodes = []
    nodeCount = 0
    try:
        printProgressMSG('\nTrying to read Boundary Condition file ... ')
        with open(fullPath) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('%'):
                    continue
                line = line.replace(',', ' ')
                line = line.replace(';', ' ')
                xyz = line.split()
                nodeCount += 1
                Indx = nodeCount -1
                if len(xyz) == 2:
                    x = bool(int(xyz[0]))
                    y = bool(int(xyz[1]))
                    if x and y:
                        fixed_nodes.append(nodeList[Indx])
                    elif x and (not y):
                        X_fixed_nodes.append(nodeList[Indx])
                    elif y:
                        Y_fixed_nodes.append(nodeList[Indx])

                    BC_list.append(x)
                    BC_list.append(y)
                else:
                    printERR_MSG('The BC condition at node '+str(nodeCount)+' not correct')
                    os.exit(1)
            if num_Nodes != nodeCount:
                printERR_MSG('All nodes not properly constrained ')
                os.exit(1)


        printSuccessMSG('Boundary Conditions created ')

        printWARN_MSG('Fixed Nodes :')
        for nnode in fixed_nodes:
            print(' NodeID {0:3} x = {1:5.2f}, y = {2:5.2f}'.format(
                nnode.nodeID,nnode.x,nnode.y))
        
        printWARN_MSG('\nFixed in X direction :')
        for nnode in X_fixed_nodes:
            print(' NodeID {0:3} x = {1:5.2f}, y = {2:5.2f}'.format(
                nnode.nodeID, nnode.x, nnode.y))

        printWARN_MSG('\nFixed in Y direction :')
        for nnode in Y_fixed_nodes:
            print(' NodeID {0:3} x = {1:5.2f}, y = {2:5.2f}'.format(
                nnode.nodeID, nnode.x, nnode.y))

        return np.array(BC_list), fixed_nodes, X_fixed_nodes, Y_fixed_nodes

    except:
        if os.path.exists(fullPath):
            printERR_MSG('CHECK "bc_code.txt" FILE')
            sys.exit(1)
        else:
            printERR_MSG('ERROR!! File '+fullPath+' not found!!!')
            sys.exit(1)


def readLoads(inputLocation, num_Nodes):
    fileName = 'loads.txt'
    fullPath = inputLocation+'/'+fileName
    Load_list = []
    nodeCount = 0
    try:
        printProgressMSG('\nTrying to read Loading file ... ')
        with open(fullPath) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith('%'):
                    continue
                line = line.replace(',', ' ')
                line = line.replace(';', ' ')
                xyz = line.split()
                nodeCount += 1
                if len(xyz) == 2:
                    x = float(xyz[0])
                    y = float(xyz[1])
                    Load_list.append(x)
                    Load_list.append(y)
                else:
                    printERR_MSG('The BC condition at node ' +
                                 str(nodeCount)+' not correct\n' +
                                 'The format should be Fx, Fy ')
                    os.exit(1)
            if num_Nodes != nodeCount:
                printERR_MSG('All nodes not properly loaded ')
                os.exit(1)

        printSuccessMSG('Loading Conditions created ')
        return np.array(Load_list)

    except:
        if os.path.exists(fullPath):
            printERR_MSG('CHECK "loads.txt" FILE')
            sys.exit(1)
        else:
            printERR_MSG('ERROR!! File '+fullPath+' not found!!!')
            sys.exit(1)
