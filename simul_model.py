## Code to compute the equilibrium of a basic closed-city
## version of Ahlfeldt Redding Sturm Wolf
## Model inputs in a city of J neighborhoods:
##  . Jx1 total factor productivities
##  . Jx1 residential amenities
##  . Jx1 land areas
##  . Jx1 workplace attractiveness
##  . JxJ matrix of distances
## Model parameters (in order):
##  0 = a  = share of floor space in production
##  1 = b  = share of floor space in consumption
##  2 = e  = location choice elasticity
##  3 = t  = distance disutility
##  4 = m  = floor space supply elasticity
##  5 = lr = residential amenities agglo effects
##  6 = dr = residential amenities decay
##  7 = lm = productivity agglo effects
##  8 = dm = productivty spillovers decay
##  9 = HT = total population

import time
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from computeA import compute_A
from computeB import compute_B
from computeh import compute_H
from computeprice import compute_prices


## Function to simulate the model.
## Takes parameters, exogenous variables and an initial matrix of
## bilateral flows as inputs
## J localisations
## entrées :
##      par = dico de paramètres
##      inputs = matrice (J x 4) des carac exogènes des localisations
##              . Jx1 total factor productivities (a_j)
##              . Jx1 residential amenities (b_i)
##              . Jx1 land areas (L_i)
##              . Jx1 workplace attractiveness (T_j)
##      d = matrice de distance entre toutes les localisations (J x J)
## Pour toutes les matrices JxJ, lignes = résidence et col = travail

@st.cache_data

def simsim(par, inputs, d, H_0):
    t0 = time.time()
    # Compute specific travel costs
    dhh = np.exp(np.log(d+1) * (-par['t']))
    ddr = np.exp(np.log(d+1) * (-par['dr']))
    ddm = np.exp(np.log(d+1) * (-par['dm']))
    J = inputs.shape[0]

    # Initialize endogenous variables
    H_t = H_0
    H_t = H_t * par['HT'] / H_t.sum()  ## (J x J) H_ij = population on each commute
    A_t = compute_A(H_t, par, inputs, ddm) ## Total factor productivity
    B_t = compute_B(H_t, par, inputs, ddr)
    Q_t = np.ones((J, 1))  ## Q = loyers du bâti (J x 1)
    Q_t, w_t, ein = compute_prices(Q_t, H_t, A_t, par, inputs)
    
    # Fixed point iterations
    ll = 1/(par['e'])
    nn = 0
    er = 1
    lr = []
    while er>1e-3:
        # Update prices from previous period population
        Q_t, w_t, ein = compute_prices(Q_t, H_t, A_t, par, inputs)
    
        # Update agglo effects
        A_t = compute_A(H_t, par, inputs, ddm)
        B_t = compute_B(H_t, par, inputs, ddr)
    
        # Update populations
        H_tm1 = H_t.copy()
        H_t = compute_H(Q_t, w_t, B_t, dhh, par, inputs)
    
        er = np.max(np.abs( (H_t - H_tm1) / (H_tm1) )) + ein

        lr.append(er)
        nn = nn+1
        print('iter ' + str(nn) + ', err = ' + str(er))
    
        H_t = H_tm1 * np.power(H_t/H_tm1, ll)
            
    t1 = time.time()
    print('Converged in ' + str(nn) + ' iterations and ' +  str(t1-t0) + ' seconds ')
    print('Criterion = ' + str(er))

    return H_t, Q_t, w_t, A_t, B_t, lr





