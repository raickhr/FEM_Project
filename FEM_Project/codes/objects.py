import numpy as np
class point:
        def __init__(self, x, y):
            self.nodeID = -999
            self.x = x
            self.y = y
        
        def assignNodeID(self,ID):
            self.nodeID = ID


class Q4_element:
    def __init__(self, coordList):
        self.elemID = -999

        self.node_ID_list = np.array([point.nodeID for point in coordList])

        self.x_list = np.array([point.x for point in coordList])
        self.y_list = np.array([point.y for point in coordList])

        self.u = np.array([0 for point in coordList])
        self.v = np.array([0 for point in coordList])
        
        Xlen = 65
        Ylen = 65

        self.ux = np.zeros((Xlen, Ylen), dtype=float)
        self.uy = np.zeros((Xlen, Ylen), dtype=float)
        self.dispMag = np.zeros((Xlen, Ylen), dtype=float)

        self.strain_x = np.zeros((Xlen, Ylen), dtype=float)
        self.strain_y = np.zeros((Xlen, Ylen), dtype=float)
        self.strain_xy = np.zeros((Xlen, Ylen), dtype=float)

        self.stress_x = np.zeros((Xlen, Ylen), dtype=float)
        self.stress_y = np.zeros((Xlen, Ylen), dtype=float)
        self.stress_xy = np.zeros((Xlen, Ylen), dtype=float)

        self.Kmatrix = np.empty((8,8), dtype=float)

    def assignElemID(self, ID):
        self.elemID = ID

    def assignUVdisp(self, uvArray):
        self.u = [uvArray[nodeID-1, 0] for nodeID in self.node_ID_list]
        self.v = [uvArray[nodeID-1, 1] for nodeID in self.node_ID_list]

    def calc_Fields(self, E, nu, scale=200):
        verts = np.transpose([self.x_list, self.y_list])
        dispScaled = np.transpose([self.u, self.v]) * scale

        verts = np.array(verts)+np.array(dispScaled)

        ux = np.array(self.u)
        uy = np.array(self.v)

        x = verts[:, 0]
        y = verts[:, 1]
        xy = x * y

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

        Amat = np.array(
            [[1, x[0], y[0], xy[0]],
             [1, x[1], y[1], xy[1]],
             [1, x[2], y[2], xy[2]],
             [1, x[3], y[3], xy[3]]])

        Ainv = np.linalg.inv(Amat)

        def N1(x, y): 
            return Ainv[0, 0] + x * \
            Ainv[1, 0] + y*Ainv[2, 0] + x*y*Ainv[3, 0]

        def N2(x, y): return Ainv[0, 1] + x * \
            Ainv[1, 1] + y*Ainv[2, 1] + x*y*Ainv[3, 1]

        def N3(x, y): return Ainv[0, 2] + x * \
            Ainv[1, 2] + y*Ainv[2, 2] + x*y*Ainv[3, 2]

        def N4(x, y): return Ainv[0, 3] + x * \
            Ainv[1, 3] + y*Ainv[2, 3] + x*y*Ainv[3, 3]

        def N1_x(y): 
            return Ainv[1, 0] + y*Ainv[3, 0]

        def N2_x(y): 
            return Ainv[1, 1] + y*Ainv[3, 1]

        def N3_x(y):
            return Ainv[1, 2] + y*Ainv[3, 2]

        def N4_x(y):
            return Ainv[1, 3] + y*Ainv[3, 3]

        def N1_y(x): 
            return Ainv[2, 0] + x*Ainv[3, 0]

        def N2_y(x): 
            return Ainv[2, 1] + x*Ainv[3, 1]

        def N3_y(x):
            return Ainv[2, 2] + x*Ainv[3, 2]

        def N4_y(x):
            return Ainv[2, 3] + x*Ainv[3, 3]


        nodalVal = ux
        self.ux = \
            nodalVal[0] * N1(X, Y) +\
            nodalVal[1] * N2(X, Y) +\
            nodalVal[2] * N3(X, Y) +\
            nodalVal[3] * N4(X, Y)

        self.strain_x = \
            nodalVal[0] * N1_x(Y) +\
            nodalVal[1] * N2_x(Y) +\
            nodalVal[2] * N3_x(Y) +\
            nodalVal[3] * N4_x(Y)

        self.strain_xy = \
            nodalVal[0] * N1_y(X) +\
            nodalVal[1] * N2_y(X) +\
            nodalVal[2] * N3_y(X) +\
            nodalVal[3] * N4_y(X)

        nodalVal = uy
        self.uy = \
            nodalVal[0] * N1(X, Y) +\
            nodalVal[1] * N2(X, Y) +\
            nodalVal[2] * N3(X, Y) +\
            nodalVal[3] * N4(X, Y)

        self.strain_y = nodalVal[0] * N1_y(X) +\
            nodalVal[1] * N2_y(X) +\
            nodalVal[2] * N3_y(X) +\
            nodalVal[3] * N4_y(X)
        
        self.strain_xy += nodalVal[0] * N1_x(Y) +\
            nodalVal[1] * N2_x(Y) +\
            nodalVal[2] * N3_x(Y) +\
            nodalVal[3] * N4_x(Y)

        self.dispMag = np.sqrt(self.ux**2 + self.uy**2)

        self.stress_x = E/(1-nu**2)*(self.strain_x + nu * self.strain_y)
        self.stress_y = E/(1-nu**2)*(nu * self.strain_x + self.strain_y)

        self.stress_xy = 0.5*E/(1+nu) * self.strain_xy

    def calcJmatrix(self, xi, eta):
        d_ShapeF = np.array(\
            [[-(1-eta), (1-eta), (1+eta), -(1+eta)],
             [ -(1-xi), -(1+xi),  (1+xi),   (1-xi)]])

        XY_matrix = np.transpose([self.x_list, self.y_list])
        Jmatrix = np.matmul(d_ShapeF,XY_matrix)
        return Jmatrix

    def getBetaMatrix(self,xi, eta):
        J = self.calcJmatrix(xi, eta)
        Jinv = np.linalg.inv(J)
        detJ = np.linalg.det(J)
        beta = np.array(
            [[Jinv[0, 0], Jinv[0, 1], 0, 0],
             [Jinv[1, 0], Jinv[1, 1], 0, 0],
             [0, 0, Jinv[0, 0], Jinv[0, 1]],
             [0, 0, Jinv[1, 0], Jinv[1, 1]]])

        return beta, detJ

    def getGammaMatrix(self,xi, eta):
        gamma = np.array(
            [[-(1 - eta), 0, (1 - eta),  0, (1 + eta), 0, -(1 + eta), 0],
             [-(1 - xi), 0, -(1 + xi),  0,  (1 + xi), 0,   (1 - xi), 0],
             [0, -(1 - eta),  0, (1 - eta),  0, (1 + eta), 0, -(1 + eta)],
             [0,  -(1 - xi),  0, -(1 + xi),  0,  (1 + xi), 0,   (1 - xi)]],dtype=float)

        return gamma

    def getKmat(self, xi, eta, alpha, t, Emat):
        beta, detJ = self.getBetaMatrix(xi, eta)
        gamma = self.getGammaMatrix(xi, eta)
        Bmat = np.matmul(alpha, beta)
        Bmat = np.matmul(Bmat, gamma)
        Btrans = np.transpose(Bmat)
        Kmat = np.matmul(Btrans, Emat)
        Kmat = np.matmul(Kmat, Bmat)
        Kmat = detJ * t * Kmat
        return Kmat
            

    def calcFullIntKmatrix(self, t, E, nu):    
        Emat = E/(1-nu**2)* np.array(\
            [[  1, nu,          0],
             [ nu,  1,          0],
             [  0,  0, (1 - nu)/2]])

        alpha =np.array([[1, 0, 0, 0],
                          [0, 0, 0, 1],
                          [0, 1, 1, 0]])
        
        #### Values of xi and eta for full integration

        xi_list = [-1/np.sqrt(3), 1/np.sqrt(3)]
        eta_list = [-1/np.sqrt(3), 1/np.sqrt(3)]

        ### first point
        xi = xi_list[0]
        eta = eta_list[0]

        Kmat1 = self.getKmat(xi, eta, alpha, t, Emat)

        ### second point
        xi = xi_list[1]
        eta = eta_list[0]

        Kmat2 = self.getKmat(xi, eta, alpha, t, Emat)

        ### third point
        xi = xi_list[1]
        eta = eta_list[1]

        Kmat3 = self.getKmat(xi, eta, alpha, t, Emat)

        ### fourth point
        xi = xi_list[0]
        eta = eta_list[1]

        Kmat4 = self.getKmat(xi, eta, alpha, t, Emat)

        Kmat = Kmat1 + Kmat2 + Kmat3 + Kmat4

        self.Kmatrix = np.array(Kmat)
        


        
        
        

