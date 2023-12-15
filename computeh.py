
import numpy as np
def compute_H(Q, w, B, dhh, par, inputs):
        v_ij = np.outer(B, inputs[:,3]) * dhh
        v_ij = v_ij * np.outer(np.power(Q,-par['b']*par['e']), np.power(w, par['e']))
        return par['HT'] * v_ij / v_ij.sum()