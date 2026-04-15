# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:24:27 2026

@author: AWOUNANG
"""

import math
import numpy as np

nom="optim"

# Définition des voisinages
#
#             0     1
#
#    2     3     4     5   
#
#       6     7     8     9
#
#          10    11    12    13
#
#             14    15
#

M=16
Vx = 1.0
Vy = math.sqrt(3.0) * Vx

# Constellation 16 symboles avec indices correspondant au schéma

constellation=np.array([
               [  -Vx,  2*Vy],
               [   Vx,  2*Vy],
#
               [-4*Vx,    Vy],
               [-2*Vx,    Vy],
               [    0,    Vy],
               [ 2*Vx,    Vy],
#
               [-3*Vx,     0],
               [  -Vx,     0],
               [   Vx,     0],
               [ 3*Vx,     0],
#              
               [-2*Vx,   -Vy],
               [    0,   -Vy],
               [ 2*Vx,   -Vy], 
               [ 4*Vx,   -Vy],
#               
               [  -Vx, -2*Vy],
               [   Vx, -2*Vy]
])

symboles = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]
