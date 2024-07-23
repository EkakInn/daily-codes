import cv2
import numpy as np

# Example points defined by their x1, y1 and x2, y2 coordinates
points = np.array([
    [1, 2],
    [2, 4],
    [3, 1],
    [5, 3],
    [4, 5]
], dtype=np.float32)

# Find the minimum area bounding rectangle
rect = cv2.minAreaRect(points)
print(rect)

# Get the box points and convert them to integer
box = cv2.boxPoints(rect)
box = np.int0(box)

# The rect variable contains:
# - center (x, y) of the rectangle
# - (width, height) of the rectangle
# - angle of rotation

# Minimum area
width, height = rect[1]
min_area = width * height

print(f"Minimum area: {min_area}")
print("Rectangle corners:")
for corner in box:
    print(corner)
