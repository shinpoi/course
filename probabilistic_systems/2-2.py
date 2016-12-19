# python3
# homework 2-2 of probabilistic systems

import numpy as np

# add y(1-2) = y(-1), k(1-1) = k(0)
y = [1,1]
a1 = -1
a2 = -1
n = 5
for k in range(5): # N=1~5 ( k=0~5 )
    #print(k)
    y.append(-a1*y[k]-a2*y[k+1])
    #print(y)
print("y:\n",y,"\n")

# hn
phi_num = np.array([0, 0])
for k in range(2, n+2):
    phi = np.array([-y[k-1]*y[k], -y[k-2]*y[k]])
    phi_num += phi
hn = phi_num/float(n)
print("hn:\n", hn, "\n")

# Gn
pxp_num = np.array([[0, 0], [0, 0]])
for k in range(2, n+2):
    pxp_t = np.array([[y[k-1]**2, y[k-1]*y[k-2]], [y[k-1]*y[k-2], y[k-2]**2]])
    pxp_num += pxp_t

gn = pxp_num/float(n)
print("gn:\n", gn, "\n")

gn_inv = np.linalg.inv(gn)
print("gn_inv:\n", gn_inv, "\n")

# suppose theta
theta_hat = np.dot(gn_inv, hn)
print("theta_hat:\n", theta_hat, "\n")
