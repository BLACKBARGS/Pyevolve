import numpy as np
import cv2
from pyflow import pyflow

# Read two images
image1 = cv2.imread('path/to/your/image1.png', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('path/to/your/image2.png', cv2.IMREAD_GRAYSCALE)

# Normalize the images to the range [0, 1]
image1 = image1.astype(float) / 255.
image2 = image2.astype(float) / 255.

# Set Pyflow parameters
alpha = 0.012
ratio = 0.75
minWidth = 20
nOuterFPIterations = 7
nInnerFPIterations = 1
nSORIterations = 30
colType = 0  # 0:RGB, 1:GRAY (but pass gray image with shape (h,w,1))

# Compute the optical flow
u, v, _ = pyflow.coarse2fine_flow(image1, image2, alpha, ratio, minWidth, nOuterFPIterations, nInnerFPIterations, nSORIterations, colType)

# Compute the flow magnitude
flow_magnitude = np.sqrt(u ** 2 + v ** 2)

# Display the flow magnitude
cv2.imshow('Flow Magnitude', flow_magnitude)
cv2.waitKey(0)
cv2.destroyAllWindows()
