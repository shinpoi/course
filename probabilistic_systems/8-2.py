# -*- coding: utf-8 -*-
# python3.5

import numpy as np
import math
import matplotlib.pyplot as plt

###################################
# model's parameter 7.1
b = 1
sigma_v = 1
sigma_w = 100
x0_71 = 10
N = 300   # samples's number


def f_71(x):
    return x + 3 * math.cos(x/10.0)


def h_71(x):
    return x**3


def a_71(x_guess_prior):
    return 1 - (3 / 10.0) * math.sin(x_guess_prior / 10.0)


def c_71(x_guess_prior):
    return 3 * (x_guess_prior ** 2)


###################################
# x(k+1) = f(x(x)) + bv(k)
# y(k) = h(x(k)) + w(k)
# ( f(x), b, h(x), A = df(x)/dx, cT = dh(x)/dx, sigma_v, sigma_w
class EKF(object):
    def __init__(self, f, b, h, A, cT, sigv, sigw, x0=0):
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
    def run(self, n, x_g_0, p0):
        # create dataset
        x_list = self.x_list
        x_k = x_list[0]
        x_guess_list = [0]

        for i in range(1, n+1):
            self.x_list.append(self.x_next(x_k))
        y_list = [self.y(x) for x in self.x_list]

        # Filter
        x_guess_k = x_g_0
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

        print(len(range(N+1)), len(y_list), len(x_list), len(x_guess_list))

        # plot
        plt.figure(1)
        plt.plot(range(N+1), x_list, label="true value", color="purple", linewidth=1)
        plt.plot(range(N+1), x_guess_list[1:], label="guess value", color="blue", linewidth=1)
        plt.xlabel("k")
        plt.ylabel("value")
        plt.title("Kalman Filter")
        plt.legend()

        plt.figure(2)
        plt.plot(range(N + 1), y_list, label="observe value", color="black", linewidth=1)
        plt.xlabel("k")
        plt.ylabel("value")
        plt.title("Kalman Filter")
        plt.legend()

        plt.show()


###################################
# Run
ekf71 = EKF(f=f_71, b=b, h=h_71, A=a_71, cT=c_71, sigv=sigma_v, sigw=sigma_w, x0=x0_71)
ekf71.run(n=N, x_g_0=11, p0=1)