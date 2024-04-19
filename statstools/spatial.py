import numpy as np
import pandas as pd
from scipy.linalg import cho_solve, cho_factor, eigh

def moranBasis(X, A, tol = 0.95, as_df = True):
    X = np.array(X)
    XtX = X.T @ X
    Ip = np.eye(X.shape[1])
    In = np.eye(X.shape[0])
    po = (In - X @ cho_solve(cho_factor(X.T@X, lower=True), Ip) @ X.T)
    mat = po@A@po
    e_vals, e_vecs = eigh(mat)
    sorted_indices = np.argsort(e_vals)[::-1]
    e_vals = e_vals[sorted_indices]
    e_vecs = e_vecs[:, sorted_indices]
    pos = np.where(e_vals > 0)[0]
    sel = np.where(np.cumsum(e_vals[pos]) / np.sum(e_vals[pos]) < tol)[0]
    M = e_vecs[:,pos[sel]]
    if as_df == True:
        col_names = ['b' + str(i) for i in range(M.shape[1])]
        M = pd.DataFrame(M, columns=col_names)
    return M