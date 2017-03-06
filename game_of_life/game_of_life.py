import sys
import argparse
import numpy as np
import cv2 as cv


def neighbours(array, row, col):
    k1 = array.shape[0]-1 if row == 0 else row-1
    k2 = array.shape[1]-1 if col == 0 else col-1
    k3 = 0 if col+1 == array.shape[1] else col+1
    k4 = 0 if row+1 == array.shape[0] else row+1
    return np.count_nonzero(np.array((array[k1, k2], array[k1, col],
                                      array[k1, k3], array[row, k2],
                                      array[row, k3], array[k4, k2],
                                      array[k4, col], array[k4, k3])))


def get_next_step(array):
    _array = np.copy(array)
    for row in range(array.shape[0]):
        for col in range(array.shape[1]):
            if array[row][col] == 0:
                if neighbours(array, row, col) == 3:
                    _array[row][col] = 1
            else:
                if not(1 < neighbours(array, row, col) < 4):
                    _array[row][col] = 0
    return _array


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help='path to file with beginning')
    args = parser.parse_args()
    try:
        array = np.loadtxt(args.path, dtype=int)
    except IOError:
        if not(args.path):
            sys.exit()
        print("No such file or directory: "+args.path)
    a = np.array([[np.array([250, 200, 0], dtype=np.uint8)
                   for j in range(array.shape[1])]
                  for i in range(array.shape[0])])
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.resizeWindow('image', 500, 500)
    while True:
        array = get_next_step(array)
        cv.imshow("image", np.array([[a[i, j]*array[i, j]
                                      for j in range(a.shape[1])]
                                     for i in range(a.shape[0])]))
        if cv.waitKey(150) > 0:
            break
