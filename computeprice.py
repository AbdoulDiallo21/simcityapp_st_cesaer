import numpy as np

def compute_w(Q, A, par):
    a = par['a']
    return (1-a) * np.power(A[:,None], 1/(1-a)) * np.power((1/a)*Q, a/(a-1))

def compute_prices(Q, H, A, par, inputs):
    # New equilibrium Q and W given pop
    a = par['a']
    b = par['b']
    m = par['m']
    L = inputs[:,2][:,None]

    er = 1
    nn = 0
    ll = a / (1 + a*(1+m))
    #ll = 1
    while er>1e-5 and nn<1 :
        w = compute_w(Q, A, par)
        Fd = b*(H @ w) + (a/(1-a))*H.sum(0)[:,None]*w
        Fs = L * np.power(Q, m+1)
        Q  = Q * np.power(Fd/Fs, ll)
        er = np.max(np.abs((Fd - Fs)/Fs))
        nn = nn+1

    #print("Er = " + str(er))
    if nn>1:
        print("Warning, potential failed convergence of inner loop")

    w = compute_w(Q, A, par)
    return Q, w, er