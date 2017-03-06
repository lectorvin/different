import numpy as np
import cv2 as cv


def get_random_image(height, width):
    im = np.ndarray(shape=(height, width, 3), dtype=np.uint8)
    for row in range(height):
        for col in range(width):
            im[row][col] = np.array([np.random.randint(1, 255),
                                     np.random.randint(1, 255),
                                     np.random.randint(1, 255)],
                                    dtype=np.uint8)
    return im


if __name__ == "__main__":
    height, width = 250, 250
    while True:
        cv.imshow("image", get_random_image(height, width))
        if cv.waitKey(30) > 0:
            break
