# -*- coding: utf-8 -*-
# python3.5
# complementary filter in Kalman Filter

import numpy as np
import matplotlib.pyplot as plt
import math

# parameter
n = 200

sigma_v1 = 60
sigma_v2 = 60
a = 0.75
mu0 = 0
beta0 = 20
e2_0 = 0
z_0 = 10

x_0 = np.matrix([[mu0], [beta0], [e2_0]])
A = np.matrix([[a, 0, 0], [0, 1, 0], [0, 0, 0]])
B = np.matrix([[1-a, 0], [0, 0], [0, 1]])
cT = np.matrix([[1, 1, -1]]).transpose()

p = 0


def z_next(n, z0):
    z_list = [z0]
    z = z0
    for i in range(1,n):
        z = z + 2*math.cos(0.05*i) + np.random.normal(0, 5)
        z_list.append(z)
    return z_list


def y1(z_list, mu0, a, sigma_v1, beta):
    y1_list = []
    mu_list = []
    mu = mu0
    for z in z_list:
        mu = a*mu + (1-a)*np.random.normal(0, sigma_v1)
        y1 = z + mu + beta
        y1_list.append(y1)
        mu_list.append(mu)
    return np.array(y1_list), np.array(mu_list)


def y2(z_list, sigma_v2):
    y2_list = []
    e2_list = []
    for z in z_list:
        e2 = np.random.normal(0, sigma_v2)
        y2 = z + e2
        y2_list.append(y2)
        e2_list.append(e2)
    return np.array(y2_list), np.array(e2_list)

# Kalman Filter
class KalmanFilter(object):
    def __init__(self, A, B, Q, cT, R):
        self.A = A
        self.B = B
        self.Q = Q
        self.cT = cT
        self.R = R

    def guess(self, y_list, x0, p0):
        x_guess = x0
        p_k = p0
        x_guess_list = []
        for y_k in y_list:
            x_guess_pri = self.A * x_guess
            p_pri = self.A * p_k + self.A.transpose() + self.B * self.Q * self.B.transpose()
            g = (p_pri * self.cT) * ((self.cT.transpose() * p_pri * self.cT + self.R)**-1)
            x_guess = x_guess_pri + g * (y_k - self.cT.transpose() * x_guess_pri)
            p_k = (np.identity(len(x0)) - g * self.cT.transpose()) * p_pri
            x_guess_list.append(x_guess)
        return x_guess_list

#########################################
# create dataset
z_list = z_next(n=n, z0=z_0)
y1_list, mu_list = y1(z_list=z_list, mu0=mu0, a=a, sigma_v1=sigma_v1, beta=beta0)
y2_list, e2_list = y2(z_list=z_list, sigma_v2=sigma_v2)

y_list = y1_list - y2_list

# Run Kalman Filter
Q = np.diag([60, 60])
R = 0.0001
x00 = np.matrix([[10], [30], [20]])
p00 = np.matrix([[1000, 0, 0], [0, 1000, 0], [0, 0, 1000]])

kf = KalmanFilter(A, B, Q, cT, R)
x_guess_list = kf.guess(y_list, x00, p00)

mu_list_guess = [mu.tolist()[0][0] for mu in x_guess_list]
e2_list_guess = [mu.tolist()[2][0] for mu in x_guess_list]

z_list_guess = y2_list - np.array(e2_list_guess)


###########################################
# plot
# y1 - y2 - true
plt.figure(1, figsize=(16, 9))
plt.plot(range(n), y1_list, label="value of sensor1", color="purple", linewidth=1)
plt.plot(range(n), y2_list, label="value of sensor2", color="orange", linewidth=1)
plt.plot(range(n), z_list, label="true value ", color="red", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("Kalman Filter (sensor - true)")
plt.legend()

# e2 - e2_hat
plt.figure(2, figsize=(16, 9))
plt.plot(range(n), e2_list, label="$e_2$(true value)", color="black", linewidth=1)
plt.plot(range(n), e2_list_guess, label="$e_2$(guess value)", color="green", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("Kalman Filter ($e_2$ - $\hat{e_2}$)")
plt.legend()

plt.figure(3, figsize=(16, 9))
plt.plot(range(n), z_list, label="z(true value)", color="black", linewidth=1)
plt.plot(range(n), z_list_guess, label="z(guess value)", color="red", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("$z$ - $\hat{z}$")
plt.legend()

plt.show()
