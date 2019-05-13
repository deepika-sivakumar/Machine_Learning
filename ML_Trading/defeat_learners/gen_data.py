"""
template for generating data to fool learners (c) 2016 Tucker Balch
Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Deepika Sivakumar
GT User ID: dsivakumar6
GT ID: 903450354
"""

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

def author():
    return 'dsivakumar6'

if __name__=="__main__":
    print "they call me Tim."
