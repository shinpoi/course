# -*- coding: utf-8 -*-
# python3.5

import numpy as np
import math
import matplotlib.pyplot as plt

# parameter
b = 1
sigma_v = 1
sigma_w = 100
N = 50   # samples's number


# function
def x_next(x):
    return x + 3 * math.cos(x/10.0) + np.random.normal(0, sigma_v)


def y(x):
    return x**3 + np.random.normal(0, sigma_w)


# Filter update
def x_guess_prior_next(x_guess):
    return x_guess + 3 * math.cos(x_guess/10.0)


def a(x_guess_prior):
    return 1 - 3/10.0 * math.sin(x_guess_prior/10.0)


def c(x_guess_prior):
    return 3 * x_guess_prior**2


def p_prior_next(p_prior, a_k, sig_v=sigma_v, b1=b):
    return a_k**2 * p_prior + sig_v**2 * b1**2


def g(p_prior, c_k, sig_w=sigma_w):
    return (p_prior * c_k) / (c_k**2 * p_prior + sig_w**2)


def x_guess_next(x_guess_prior, g_k, y_k_):
    return x_guess_prior + g_k * (y_k_ - x_guess_prior**3)


def p(g_k, p_prior, c_k):
    return (1 - g_k * c_k) * p_prior


# Extended Kalman Filter
def EKF(ylist):
    x_guess_list = []
    x_guess_prior_k = 10
    pk = 1

    for yk in ylist:
        x_guess_prior_k = x_guess_prior_next(x_guess_prior_k)
        ak = a(x_guess_prior_k)
        ck = c(x_guess_prior_k)
        p_prior_k = p_prior_next(pk, ak)
        gk = g(p_prior_k, ck)
        x_guess_k = x_guess_next(x_guess_prior_k, gk, yk)
        pk = p(gk, p_prior_k, ck)
        x_guess_list.append(x_guess_k)

    return x_guess_list


# Create data_set
x_list = [10]
x_k = x_list[0]

y_list = [y(x_k)]
y_k = y_list[0]

for n in range(1, N+1):
    x_k = x_next(x_k)
    x_list.append(x_k)
    y_k = y(x_k)
    y_list.append(y_k)

# Run EKF
xguess_list = EKF(y_list)

# plot
# plt.plot(range(N+1), y_list, label="observe value", color="red", linewidth=1)
plt.plot(range(N+1), x_list, label="true value", color="green", linewidth=1)
plt.plot(range(N+1), xguess_list, label="guess value", color="blue", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("Kalman Filter")
plt.legend()
plt.show()
