import numpy as np
import cv2

def rle_decode(rle, shape):
    """Decodes an RLE encoded list of space separated
    numbers and returns a binary mask."""
    rle = list(map(int, rle.split()))
    rle = np.array(rle, dtype=np.int32).reshape([-1, 2])
    rle[:, 1] += rle[:, 0]
    rle -= 1
    mask = np.zeros([shape[0] * shape[1]], np.bool)
    for s, e in rle:
        assert 0 <= s < mask.shape[0]
        assert 1 <= e <= mask.shape[0], "shape: {}  s {}  e {}".format(shape, s, e)
        mask[s:e] = 1
    # Reshape and transpose
    mask = mask.reshape([shape[1], shape[0]]).T
    return mask
if __name__ == "__main__":
    result = rle_decode("137692 7 138203 9 138714 12 139226 13 139737 15 140249 18 140761 21 141272 23 141784 23 142296 23 142808 23 143320 23 143832 23 144344 23 144856 23 145368 23 145880 22 146392 21 146904 20 147416 20 147929 18 148441 17 148954 15 149467 13 149980 11 150493 8 151007 1",(512,512))
    image = np.array(result).reshape(512,512,1).astype(np.uint8)
    cv2.imshow('image', image*255)
    cv2.waitKey(0)
    # grayimg = cv2.cvtColor(image.reshape(512,512,1), cv2.COLOR_BGR2HSV)
    contours, hierarchy = cv2.findContours(image,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
