import numpy as np
import cv2
import math
def hex_corners(center, radius):
    hex_points = []
    for angle in range(0,360,60):
        angle_rad = math.radians(angle)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        hex_points.append((int(x), int(y)))
        
    return hex_points

# Intensity computation
def intensity_value(hexagon,image):
    # Découper l'hexagone
    hex_cut = image[int(y_offset):int(y_offset + h), int(x_offset):int(x_offset + l)]
    mask = np.zeros((hex_cut.shape), dtype=np.uint8)
    hex_mask = cv2.fillConvexPoly(mask, hexagon, 255)
    print(hex_cut.shape)
    print(hex_mask.shape)

    
    # Appliquer le masque pour obtenir uniquement les pixels dans l'hexagone
    masked_hex = cv2.bitwise_and(hex_cut, hex_cut, mask=hex_mask)
    
    return cv2.mean(masked_hex,mask=hex_mask)[0]
    
#Initilization
point=255
long_radius = 20
h = long_radius*math.sqrt(3)
l = long_radius*2


# Image reading
filename = "cameraman.jpg" # Path and filename of the image file
image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE) # Read and Convert the image in Grayscale

# Get image size
im_size = image.shape
print(im_size)

num_cols = int(im_size[0]// (l*0.75)) +1
num_rows = int(im_size[1]//h) +1
for row in range(num_rows):
    for col in range(num_cols):
        even = col %2
        x_offset = int(col*l*0.75)
        y_offset = int(row*h + even*(h/2))
        hex_points = hex_corners((5+x_offset,5+y_offset), long_radius)
        hex_points = np.array(hex_points, dtype=np.int32)
        hex_intensity = intensity_value(hex_points,image)
        cv2.fillConvexPoly(image, hex_points, hex_intensity)
        if x_offset + l > im_size[0] or y_offset + h > im_size[1]:
            continue
        
        
    
cv2.imshow("modified image", image)

cv2.waitKey(0)
