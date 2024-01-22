import numpy as np
def readDMAT(file):
    h = np.loadtxt(file, max_rows=1, usecols=[0,1], dtype=np.int32)
    A = np.loadtxt(file, skiprows=1, usecols=[0], dtype=np.float32)
    A = np.reshape(A,(h[0],h[1])).T
    return A
