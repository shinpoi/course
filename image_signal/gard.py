import cv2
import numpy as np

def gard(img):
    # img.shape: (x, y, channel)
    # e.g. 1200x800 pixel RGB Photo -> (800, 1200, 3)
    gar_x = np.zeros(img.shape, dtype="uint8")
    gar_y = np.zeros(img.shape, dtype="uint8")
    size_x = img.shape[0]
    size_y = img.shape[1]

    gar_x[:size_x-1] = img[:size_x-1] - img[1:size_x]
    gar_y[:, :size_y-1] = img[:, :size_y-1] - img[:, 1:size_y]

    cv2.imwrite("test_gar_x.jpg", gar_x)
    cv2.imwrite("test_gar_y.jpg", gar_y)
    cv2.imwrite("test_gar.jpg", gar_x + gar_y)

    return gar_x + gar_y

img = cv2.imread("test.jpg")

img += gard(img)
cv2.imwrite("test_output.jpg", img)
