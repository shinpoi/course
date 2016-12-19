# -*- coding: utf-8 -*-
# python2.7

import cv2
import numpy as np

white = 255

img = np.zeros(512*512, dtype="uint8")
img = img.reshape(512, 512)

for n in range(512*512):
    img[np.random.randint(512)][np.random.randint(512)] = white

cv2.imwrite("test.png", img)

###############################################
img2 = np.zeros(512*512, dtype="uint8")
img2 = img2.reshape(512, 512)

for n in range(512*512):
    i = int(np.random.normal(256, 128))
    j = int(np.random.normal(256, 128))
    if i >= 511: i = 511
    if i < 0: i = 0
    if j >= 511: j = 511
    if j < 0: j = 0
    img2[i][j] = white

cv2.imwrite("test2.png", img2)

###############################################
img3 = np.zeros(512*512, dtype="uint8")
img3 = img3.reshape(512, 512)

for i in range(512):
    for j in range(512):
        img3[i][j] = np.random.randint(2)*255
        # np.random.randint(2) ~ {0, 1}

cv2.imwrite("test3.png", img3)

'''
###############################################
f = open("/home/shin-u16/100", "r")
l1 = []
while 1:
    l = f.readline()
    if not l:
        break
    else:
        l1.append([int(x) for x in l.split("\t")])
f.close()

f = open("/home/shin-u16/100_2", "r")
l2 = []
while 1:
    l = f.readline()
    if not l:
        break
    else:
        l2.append([int(x) for x in l.split("\t")])
f.close()

list1 = []
for line in l1:
    list1 += line
list1 = np.array(list1)

list2 = []
for line in l2:
    list2 += line
list2 = np.array(list2)

img3 = np.zeros(100*100*3, dtype=int)
img3 = img3.reshape(100, 100, 3)

for n in range(len(l1)):
    img3[list1[n]][list2[n]] = white

cv2.imwrite("/home/shin-u16/test3.png", img3)
'''