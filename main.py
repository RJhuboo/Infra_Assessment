import numpy as np
import cv2
import math
def hex_corners(radius):
    mask = np.zeros((int(h),int(l)), dtype=np.uint8)
    hex_points = []
    for angle in range(0,360,60):
        angle_rad = math.radians(angle)
        x = radius + radius * math.cos(angle_rad)
        y = (int(h)//2) + radius * math.sin(angle_rad)
        hex_points.append((int(x), int(y)))
    points = np.array(hex_points)
    cv2.fillConvexPoly(mask, points, 255)
    return mask

    
#Initilization
point=255
long_radius = 10
h = int(long_radius*math.sqrt(3))
l = int(long_radius*2)


# Image reading
filename = "image test.jpg" # Path and filename of the image file
image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE) # Read and Convert the image in Grayscale

# Get image size
im_size = image.shape
print(im_size)

num_cols = int(im_size[1]// (l*0.75)) 
num_rows = int(im_size[0]//h) 
result = np.zeros_like(image)
hex_mask =  hex_corners(long_radius)
hex_means = []
for row in range(num_rows):
    for col in range(num_cols):
        even = col %2
        x_offset = int(col*l*0.75)
        y_offset = int(row*h + even*(h//2))
        hex_cut = image[int(y_offset):int(y_offset + h), int(x_offset):int(x_offset + l)]
        if x_offset + l >= im_size[1] or y_offset + h >= im_size[0]:
            continue
        # Découper l'hexagone
        hex_cut = image[y_offset:y_offset + int(h),x_offset:x_offset + int(l)]
        if hex_cut.shape[0] == 7:
            print("error")
        #print("cut:",hex_cut.shape)
        #print("mask",hex_mask.shape)
        # Appliquer le masque pour obtenir uniquement les pixels dans l'hexagone
        masked_hex = cv2.bitwise_and(hex_cut, hex_cut, mask=hex_mask)
        # Calculer la valeur moyenne des pixels dans l'hexagone
        mean_value = cv2.mean(masked_hex, mask=hex_mask)[0]
        hex_means.append(mean_value)
        
        # Remplir l'hexagone dans l'image finale avec la valeur moyenne
        filled_hex = np.full_like(masked_hex, int(mean_value))
        hex_with_intensity = cv2.bitwise_and(filled_hex, filled_hex, mask=hex_mask)
        non_zero_mask = hex_with_intensity > 0
        result[y_offset:y_offset + int(h),x_offset:x_offset + int(l)][non_zero_mask] = hex_with_intensity[non_zero_mask]
        
        
    
cv2.imshow("modified image", result)
cv2.waitKey(0)
