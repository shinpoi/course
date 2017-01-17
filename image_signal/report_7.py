import cv2
import numpy as np
import time
from sklearn.preprocessing import normalize

"""
img = cv2.imread('git.png', 0)
img2 = np.zeros((img.shape[0]*2, img.shape[1]*2), dtype='uint8')
tr = np.matrix([[2, 0], [0, 2]])


def trans(img, img2, tr_in):
    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            co = np.dot(tr_in, np.array([[i+0.5], [j+0.5]]))
            img2[i][j] = img[np.int(co[0][0])][np.int(co[1][0])]

start = time.clock()
trans(img, img2, np.array(tr**-1))
print('time = %f s' % (time.clock() - start))

cv2.imshow('or', img)
cv2.imshow('x2', img2)
cv2.waitKey(0)
"""

img = cv2.imread('git.png', 0)
"""
img_c = np.zeros((img.shape[0], img.shape[1], 2))
for i in range(img.shape[0]):
    for j in range(img.shape[0]):
        img_c[i][j][0] = img[i][j]
img_dft = cv2.dft(img_c)
img_norm = np.zeros((img.shape[0], img.shape[1]))
for i in range(img.shape[0]):
    for j in range(img.shape[0]):
        img_norm[i][j] = np.linalg.norm(img_dft[i][j])

img_log = np.log(img_norm)
img_log = np.array(img_log, dtype='uint8')
img_log = cv2.equalizeHist(img_log)
"""
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
s1 = np.log(np.abs(f))
s2 = np.log(np.abs(fshift))


# cv2.imshow('or', img)
# cv2.imshow('dft', img_log)
cv2.imshow('or', np.array(s1, dtype='uint8'))
cv2.imshow('dft', np.array(s2, dtype='uint8'))
cv2.waitKey(0)


