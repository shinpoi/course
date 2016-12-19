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
sigmaw2 = 2

# number of sample
n = 300
N = np.linspace(0, n-1, n)

y = []
x = []
x_chi = []
x_chi_next = 0
x_k = 0

# Kalman Filter
for n in range(n):
    # create y(k)
    y_k = A * x_k + np.random.normal(0, sigmaw2)
    # record x(k) and y(k)
    y.append(y_k)
    x.append(x_k)
    # Kalman Filter
    x_pri = A * x_chi_next
    p_pri = A * p + sigmav2 * b * b
    g = (p_pri * c) / (c * p_pri * c + sigmaw2)
    x_chi_next = x_pri + g * (y_k - c * x_pri)
    p = (1 - g * c) * p_pri
    x_chi.append(x_chi_next)
    # create x(k+1) as sum of x(k) plus Normalize(0,sigmaw) (same as homework.6)
    x_k += np.random.normal(0, sigmav2)

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
