# -*- coding: utf-8 -*-
# python3.5

import numpy as np
import matplotlib.pyplot as plt


# parameter
A = 1
b = 1
c = 1

p = 0

sigmav2 = 1
sigmaw2 = 2z

# number of sample
n = 50
N = np.linspace(0, n-1, n)

# noise
v = np.random.normal(0, sigmav2, n)
w = np.random.normal(0, sigmaw2, n)

# create dataset
x = []
sum_v = 0
for v_k in v:
    sum_v += v_k
    x.append(sum_v)
np.array([x])

y = x + w

x_chi = []
x_chi_next = 0

# Kalman Filter
for y_k in y:
    x_pri = A * x_chi_next
    p_pri = A * p + sigmav2 * b * b
    g = (p_pri * c) / (c * p_pri * c + sigmaw2)
    x_chi_next = x_pri + g * (y_k - c * x_pri)
    p = (1 - g * c) * p_pri
    x_chi.append(x_chi_next)

np.array([x_chi])

# plot
plt.figure(figsize=(8, 4))
plt.plot(N, x, label="true value", color="blue", linewidth=1)
plt.plot(N, y, label="observe value", color="red", linewidth=1)
plt.plot(N, x_chi, label="guess value", color="green", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("Kalman Filter")
plt.legend()
plt.show()
