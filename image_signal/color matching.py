# color matching

import numpy as np
import cv2

def histogram_matching(srcArr, dstArr, srcPNG=False):
    srcHist = cv2.calcHist((srcArr,), (0,), None, (256,), (0, 256)).reshape((-1,))
    if srcPNG:
        srcHist[0] = 0
    srcHist /= sum(srcHist)
    srcHistMap = np.zeros(256, dtype=np.float32)
    for i in range(len(srcHist)):
        srcHistMap[i] = sum(srcHist[:i])

    dstHist = cv2.calcHist((dstArr,), (0,), None, (256,), (0, 256)).reshape((-1,))
    dstHist /= sum(dstHist)
    dstHistMap = np.zeros(256, dtype=np.float32)
    for i in range(len(dstHist)):
        dstHistMap[i] = sum(dstHist[:i])

    HistMap = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        minMap = 1
        minTag = None
        for j in range(256):
            if minMap > abs(srcHistMap[i] - dstHistMap[j]):
                minMap = abs(srcHistMap[i] - dstHistMap[j])
                minTag = j
        HistMap[i] = minTag


    for i in range(srcArr.shape[0]):
        for j in range(srcArr.shape[1]):
            if srcArr[i, j] == 0:
                continue
            else:
                srcArr[i, j] = HistMap[srcArr[i, j]]
    return srcArr

def hm_color(srcArr, dstArr, srcPNG=False):
    srcArr = srcArr.copy()
    for i in range(3):
        srcArr[:,:,i] = histogram_matching(srcArr[:,:,i], dstArr[:,:,i], srcPNG=srcPNG)
    return srcArr


"""
# example
a = cv2.imread("a.png")
b = cv2.imread("b.png")
c = hm_color(a, b)

cv2.imwrite("c.png", c)
"""
