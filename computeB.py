import numpy as np
def compute_B(H, par, inputs, ddr):
    return inputs[:,1] * np.power( ddr @ H.sum(1) , par['lr'])