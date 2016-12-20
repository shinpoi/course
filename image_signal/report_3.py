# -*- coding: utf-8 -*-
# Python 2.7
# OpenCV 3.1

import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread('photo_kyutech.jpg', 0)  # read as gray-scale image

high = img.shape[0]
width = img.shape[1]

###################
# histogram
a = plt.hist(img.reshape(-1), bins=51)
mu = a[1][25]  # threshold value =  mid-value of histogram

# Binarization
img_bin = np.array(img)
for i in range(high):
    for j in range(width):
        if img[i][j] > mu:
            img_bin[i][j] = 255
        else:
            img_bin[i][j] = 0

###################
# Edge
prewitt = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
sobel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
laplacian = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])

img_p = cv2.filter2D(img, -1, prewitt)
img_s = cv2.filter2D(img, -1, sobel)
img_l = cv2.filter2D(img, -1, laplacian)

###################
# Write in files
cv2.imwrite('image_gray.png', img)
cv2.imwrite('image_binarization.png', img_bin)
cv2.imwrite('image_prewitt.png', img_p)
cv2.imwrite('image_sobel.png', img_s)
cv2.imwrite('image_laplacian.png', img_l)

# Show
cv2.imshow('image_original', img)
cv2.imshow('image_binarization', img_bin)
cv2.imshow('image_prewitt', img_p)
cv2.imshow('image_sobel', img_s)
cv2.imshow('image_laplacian', img_l)
cv2.waitKey(0)
