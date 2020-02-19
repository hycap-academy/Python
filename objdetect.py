import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
im = cv2.imread('cooking-tips-one-two-668419900.jpg')
bbox, label, conf = cv.detect_common_objects(im)
output_image = draw_bbox(im, bbox, label, conf)
plt.imshow(output_image)
plt.show()

#pip3 install OpenCV-python
#pip3 install matplotlib
#pip3 install cvlib
#pip3 install tensorflow
