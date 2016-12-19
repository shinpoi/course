# -*- coding: utf-8 -*-
# python 2.7
# OpenCV 3.1

import cv2
import numpy as np
import matplotlib.pyplot as plt


##################################
# Kalman Filter
class KF:
    def __init__(self, y_list, a, b, c, sig_v, sig_w):
        self.y_list = y_list
        self.a = a
        self.b = b
        self.c = c
        self.sig_v = sig_v
        self.sig_w = sig_w

    def run(self, x0, p0):
        x_g = np.zeros(len(self.y_list))
        x_g[0] = x0
        x_gue = x0
        p = p0
        for i in range(len(self.y_list))[:-1]:
            x_p_g = self.a * x_gue
            p_p = self.a**2 * p + self.b**2 * self.sig_v**2
            g = (p_p * self.c) / (self.c**2 * p_p + self.sig_w**2)
            x_gue = x_p_g + g * (self.y_list[i+1] - self.c * x_p_g)
            p = (1 - g * self.c) * p_p
            x_g[i+1] = x_gue
        return x_g

# END Kalman Filter
##################################

# image
a = 1
b = 1
c = 10

sigma_v = 3
sigma_w = 30

rank = 768
length = rank * rank

img_true = np.zeros(length, dtype="uint8")
img_noise = np.zeros(length)
img_filter = np.zeros(length, dtype="uint8")

# img_true
for i in range(length):
    img_true[i] = 128

for i in range(length)[1:]:
    n = a * img_true[i-1] + b * np.random.normal(0, sigma_v)
    if n > 255:
            n = 255
    if n < 0:
        n = 0
    n = int(n)
    img_true[i] = n


# img_noise
for i in range(length):
    n = c * img_true[i] + np.random.normal(0, sigma_w)
    img_noise[i] = n
    n = int(n / c)
    if n > 255:
        n = 255
    if n < 0:
        n = 0


# img filter
img_kf = KF(y_list=img_noise, a=a, b=b, c=c, sig_v=sigma_v, sig_w=sigma_w)
img_value = img_kf.run(x0=float(img_true[0]), p0=1000.0)

for i in range(length):
    n = img_value[i]
    if n > 255:
        n = 255
    if n < 0:
        n = 0
    n = int(n)
    img_filter[i] = n


# write to files
n = 600
img_true_line = img_true[:n]
img_filter_line = img_filter[:n]
img_deviation = img_true - img_filter

for i in range(length):
    img_true[i] = 255 - img_true[i]
    img_filter[i] = 255 - img_filter[i]
    img_deviation[i] = 160 + 5 * img_deviation[i]

img_true = img_true.reshape([rank, rank])
img_filter = img_filter.reshape([rank, rank])
img_deviation = img_deviation.reshape([rank, rank])

cv2.imwrite("f_true.png", img_true)
cv2.imwrite("f_filter.png", img_filter)
cv2.imwrite("f__deviation.png", img_deviation)

# plot
N = range(n)

plt.figure(figsize=(16, 9))
plt.plot(N, img_true_line, label="true value", color="blue", linewidth=1)
plt.plot(N, img_filter_line, label="guess value", color="red", linewidth=1)
plt.xlabel("k")
plt.ylabel("value")
plt.title("Kalman Filter")
plt.legend()
plt.show()
