# -*- coding: utf-8 -*-
# Python 2.7
# OpenCV 3.1

import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('lowcontrast.jpg')
img = cv2.resize(img, (1200, 900))

img_r = img[:, :, 0].reshape((-1,))
img_g = img[:, :, 1].reshape((-1,))
img_b = img[:, :, 2].reshape((-1,))

# img = img.reshape((-1,))


# average hist function
def average_hist(img):
    # sort
    img_list = [[j, i] for i, j in enumerate(img)]
    img_list.sort()

    # average_hist
    bins_number = int(img.shape[0]/256.0) + 1
    img_new = np.array(img)

    n = 0
    for color in range(256):
        for i in range(bins_number):
            try:
                j = img_list[n][1]
            except IndexError as e:
                break
            img_new[j] = color
            n += 1
    return img_new


img_r_new = average_hist(img_r)
img_g_new = average_hist(img_g)
img_b_new = average_hist(img_b)


img_new = np.array(img)
img_new[:, :, 0] = img_r_new.reshape((900, 1200))
img_new[:, :, 1] = img_g_new.reshape((900, 1200))
img_new[:, :, 2] = img_b_new.reshape((900, 1200))


# show hist
hist_r = plt.hist(img_r, 256, range=(0, 256))
hist_g = plt.hist(img_g, 256, range=(0, 256))
hist_b = plt.hist(img_b, 256, range=(0, 256))
plt.close('all')

n = 256
plt.figure(1, figsize=(16, 9))
plt.axis([0, 255, 0, 25000])
plt.plot(range(n), hist_r[0], label="hist of red", color="red", linewidth=1)
plt.plot(range(n), hist_g[0], label="hist of green", color="green", linewidth=1)
plt.plot(range(n), hist_b[0], label="hist of blue", color="blue", linewidth=1)
plt.xlabel("color")
plt.ylabel("num")
plt.title("hist of color")
plt.legend()
plt.show()


# show image
cv2.imshow('image_original', img)
cv2.imshow('image_average_hist', img_new)
cv2.waitKey(0)
