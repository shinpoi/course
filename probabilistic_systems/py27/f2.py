# -*- coding: utf-8 -*-
# python 2.7
# OpenCV 3.1

import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


#################################
# Parameter
particle_number = 500
sigma_v = 5
sigma_w = 50


#################################
# State equation
# x(t+1) = f(x(t)) + N(0, sigma_v)
# y(t) = g(x(t)) + N(0, sigma_w)
def f(x):
    return x + 3 * math.cos(x/10.0)


def a(x):
    return 1 - (3.0/10) * math.sin(x / 10.0)


def g(x):
    return x**3


def c(x):
    return 3 * x**2


def x_next(x, sig_v):
    return x + 3 * math.cos(x/10.0) + np.random.normal(0, sig_v)


def y(x, sig_w):
    return g(x) + np.random.normal(0, sig_w)


##################################################################
# EKF
# from 8.py (確率システム制御特論 第8回演習のプログラムそのまま使いました)
# x(k+1) = f(x(x)) + bv(k)
# y(k) = h(x(k)) + w(k)
# ( f(x), b, h(x), A = df(x)/dx, cT = dh(x)/dx, sigma_v, sigma_w
class EKF(object):
    def __init__(self, y_list, f, b, h, A, cT, sigv, sigw, x0=0):
        self.y_list = y_list
        self.f = f
        self.b = b
        self.h = h
        self.A = A
        self.cT = cT
        self.sigma_v = sigv
        self.sigma_w = sigw
        self.x0 = x0

        self.x_guess_prior_next = f
        self.x_list = [x0]

    # function
    def x_next(self, x):
        return self.f(x) + self.b * np.random.normal(0, self.sigma_v)

    def y(self, x):
        return self.h(x) + np.random.normal(0, self.sigma_w)

    # Filter update
    def p_prior_next(self, p_prior, a_k):
        return a_k**2 * p_prior + self.sigma_v**2 * self.b**2

    def g(self, p_prior, cT_k):
        return (p_prior * cT_k) / (cT_k**2 * p_prior + self.sigma_w**2)

    def x_guess_next(self, x_guess_prior, g_k, y_k):
        return x_guess_prior + g_k * (y_k - self.h(x_guess_prior))

    @staticmethod
    def p(g_k, p_prior, cT_k):
        return (1 - g_k * cT_k) * p_prior

    # Extended Kalman Filter
    def run(self, p0):
        # create dataset
        x_guess_list = [0]
        y_list = self.y_list

        # Filter
        x_guess_k = self.x0
        p_k = p0
        for y_k in y_list:
            x_gp_k = self.x_guess_prior_next(x_guess_k)
            a_k = self.A(x_gp_k)
            cT_k = self.cT(x_gp_k)
            p_prior_k = self.p_prior_next(p_k, a_k)
            g_k = self.g(p_prior_k, cT_k)
            x_guess_k = self.x_guess_next(x_gp_k, g_k, y_k)
            p_k = self.p(g_k, p_prior_k, cT_k)
            x_guess_list.append(x_guess_k)
        return x_guess_list[1:]
# END EKF
##################################################################

# image
rank = 512
length = rank * rank

img_true = np.zeros(rank*rank, dtype="uint8")
img_noise = np.zeros(rank*rank)
img_ekf = np.zeros(rank*rank, dtype="uint8")
img_pf = np.zeros(rank*rank, dtype="uint8")
img_ekf_deviation = np.zeros(rank*rank, dtype="uint8")


# img_true
for i in range(length):
    img_true[i] = 128

for i in range(length)[1:]:
    n = x_next(img_true[i-1], sigma_v)
    if n > 255:
        n = 255
    if n < 0:
        n = 0
    n = int(n)
    img_true[i] = n


# img_noise
for i in range(length):
    img_noise[i] = y(img_true[i], sigma_w)

# img EKF
ekf = EKF(y_list=img_noise, f=f, b=1, h=g, A=a, cT=c, sigv=sigma_v, sigw=sigma_w, x0=128)
ekf_value = ekf.run(p0=1)

for i in range(length):
    n = ekf_value[i]
    if n > 255:
        n = 255
    if n < 0:
        n = 0
    n = int(n)
    img_ekf[i] = n

# write to files
n = 50
img_true_line = img_true[:n]
img_ekf_line = img_ekf[:n]

for i in range(length):
    img_ekf_deviation[i] = int(255 - 10 * abs(float(img_true[i]) - float(img_ekf[i])))

img_true = img_true.reshape([rank, rank])
img_ekf = img_ekf.reshape([rank, rank])
img_ekf_deviation = img_ekf_deviation.reshape([rank, rank])

cv2.imwrite("f2_true.png", img_true)
cv2.imwrite("f2_ekf.png", img_ekf)
cv2.imwrite("f2__ekf_deviation.png", img_ekf_deviation)

# plot
N = range(n)

plt.figure(1, figsize=(16, 9))
plt.plot(N, img_true_line, label="true value", color="blue", linewidth=1)
plt.plot(N, img_ekf_line, label="ekf value", color="red", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("Filter")
plt.legend()

plt.figure(2, figsize=(16, 9))
plt.plot(N, img_ekf_deviation.reshape(-1)[:n], label="deviation", color="red", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("Filter")
plt.legend()
plt.show()
