import numpy as np
import matplotlib.pyplot as plt

Q = np.diag([0.0000001, 0.0000001])
F = np.array([[1.,1.], [0.,1.]])
H = np.array([[1.,0.]])

def predict(X0, P0, F, Q):
    Xt = np.dot(F,X0)
    Pt = np.dot(np.dot(F,P0), F.T) + Q
    return Xt, Pt

def update(Xt, Pt, Z, H, R):
    noise = Z - np.dot(H,Xt)
    K = np.dot(np.dot(Pt,H.T),np.linalg.pinv(np.dot(np.dot(H,Pt),H.T) + R))
    Xt2 = Xt + np.dot(K,noise)
    Pt2 = np.dot(np.eye(K.shape[0]) - np.dot(K,H),Pt)
    return Xt2, Pt2, K

def kf( X0, P0, v):
    
    Xt, Pt = predict(X0, P0, F, Q)
    Xt2, Pt2, K = update(Xt, Pt, v, H, 1)

    X0 = Xt2

    return X0