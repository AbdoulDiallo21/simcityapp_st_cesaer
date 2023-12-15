import numpy as np
def compute_A(H, par, inputs, ddm):
        return inputs[:,0] * np.power( H.sum(0) @ ddm , par['lm'])