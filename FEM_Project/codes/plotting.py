import matplotlib.collections
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.path as mpath


def plotElement(element, ax):
    verts = np.transpose([element.x_list, element.y_list])
    pc = matplotlib.collections.PolyCollection(
        [verts], color="black", facecolor="None")
    ax.add_collection(pc)
    plt.xlim(-0.2, 1.2)
    plt.ylim(-0.2, 1.2)
    return ax


def plotElementUnDeformed(elementList, ax):
    for element in elementList:
        verts = np.transpose([element.x_list, element.y_list])
        pc = matplotlib.collections.PolyCollection(
            [verts], color="Black", facecolor="green")
        ax.add_collection(pc)
    plt.xlim(-0.2, 1.2)
    plt.ylim(-0.2, 1.2)
    return ax


def plotElementField(element, ax, minV, maxV, Field, scale=200):
    verts = np.transpose([element.x_list, element.y_list])
    dispScaled = np.transpose([element.u, element.v]) * scale

    verts = verts+dispScaled
    poly_verts = [(verts[0, 0], verts[0, 1]),
                  (verts[1, 0], verts[1, 1]),
                  (verts[2, 0], verts[2, 1]),
                  (verts[3, 0], verts[3, 1]),
                  (verts[0, 0], verts[0, 1])]

    x = verts[:, 0]
    y = verts[:, 1]

    x0 = np.min(x)
    x1 = np.max(x)
    dx = (x1 - x0)/64
    XX = np.arange(x0, x1+dx, dx)
    XX = XX[0:65]

    y0 = np.min(y)
    y1 = np.max(y)
    dy = (y1 - y0)/64
    YY = np.arange(y0, y1+dy, dy)
    YY = YY[0:65]

    X, Y = np.meshgrid(XX, YY)

    levels = np.linspace(minV, maxV, 50)
    im2 = plt.contourf(X, Y, Field,levels, cmap='rainbow')
    # if not len(plt.gcf().axes) > 1:
    #     cbar = plt.colorbar(im2)
    #     #cbar.set_clim(1e-11, 1e-10)
    
    poly_codes = [mpath.Path.MOVETO, mpath.Path.LINETO, mpath.Path.LINETO,
                  mpath.Path.LINETO, mpath.Path.CLOSEPOLY]
    path = mpath.Path(poly_verts, poly_codes)
    patch = mpatches.PathPatch(path, facecolor='none', edgecolor='k')
    ax.add_patch(patch)
    for col in im2.collections:
        col.set_clip_path(patch)
    plt.xlim(-0.2, 1.2)
    plt.ylim(-0.2, 1.2)
    return ax


def pltElements(elementList, ax, field='disp_mag', scale=500):
    minVal = []
    maxVal = []

    for i in range(len(elementList)):
        element = elementList[i]
        if field == 'disp_mag':
            fieldVal = element.dispMag
        elif field == 'disp_x':
            fieldVal = element.ux
        elif field == 'disp_y':
            fieldVal = element.uy

        elif field == 'strain_x':
            fieldVal = element.strain_x
        elif field == 'strain_y':
            fieldVal = element.strain_y
        elif field == 'strain_xy':
            fieldVal = element.strain_xy
            
        elif field == 'stress_x':
            fieldVal = element.stress_x
        elif field == 'stress_y':
            fieldVal = element.stress_y
        elif field == 'stress_xy':
            fieldVal = element.stress_xy
        
        min_V = np.min(fieldVal)
        max_V = np.max(fieldVal)

        if len(minVal) == 0:
            minVal.append(min_V)
            maxVal.append(max_V)

        else:
            if minVal[0] > min_V:
                minVal[0] = min_V
            if maxVal[0] < max_V:
                maxVal[0] = max_V

    # one_fifth = (maxVal[0] - minVal[0])/5
    # maxVal[0] += one_fifth
    # minVal[0] -= one_fifth

    for i in range(len(elementList)):
        element = elementList[i]
        if field == 'disp_mag':
            fieldVal = element.dispMag
        elif field == 'disp_x':
            fieldVal = element.ux
        elif field == 'disp_y':
            fieldVal = element.uy

        elif field == 'strain_x':
            fieldVal = element.strain_x
        elif field == 'strain_y':
            fieldVal = element.strain_y
        elif field == 'strain_xy':
            fieldVal = element.strain_xy

        elif field == 'stress_x':
            fieldVal = element.stress_x
        elif field == 'stress_y':
            fieldVal = element.stress_y
        elif field == 'stress_xy':
            fieldVal = element.stress_xy

        ax = plotElementField(
            element, ax, minVal[0], maxVal[0], fieldVal, scale=scale)
        #ax = plotElement(element, ax)
        #ax = plotElementDeformed(element, ax, scale= scale )
