# -*- coding: utf-8 -*-
# Python 2.7
# OpenCV 3.1

import cv2

img = cv2.imread('saltpapernoise.png', 0)

img_mf = cv2.medianBlur(img, 5)
img_bf = cv2.bilateralFilter(img_mf, 7, 10, 10)

cv2.imwrite('img_filter.png', img_mf)

cv2.imshow('img', img)
cv2.imshow('img_mb', img_mf)
cv2.imshow('img_mf', img_bf)
cv2.waitKey(0)
