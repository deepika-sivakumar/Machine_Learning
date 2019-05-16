
import numpy as np

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    # X Columns = 2 to 10; Y columns = 1
    # Rows = 10 to 1000
    rows = 30
    Xcolumns = 3
    X = np.random.random(size = (rows,Xcolumns))
    Y = np.array([])
    m = np.random.random(size = (Xcolumns,))
    b = np.random.random_sample()
    for i in range(0,rows):
        # Y = b + m0*X0 + m1*X1 +.....+ mk*Xk, where k = no of X columns
        Y = np.append(Y, b + np.sum(m * X[i, :]))
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)
    rows = 30
    Xcolumns = 3
    X = np.random.random(size = (rows,Xcolumns))
    Y = np.zeros((rows,))
    for i in range(0, rows):
        median = np.median(X[i,:])
        if median <= 10:
            Y[i] = 1
        elif median <= 20:
            Y[i] = 2
        elif median <= 30:
            Y[i] = 3
    return X, Y

if __name__=="__main__":
    print "they call me Tim."
