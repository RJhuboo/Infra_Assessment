import numpy as np
import cv2
import math
import pandas as pd

def Mask_hexagon(radius,height,width):
    # This function creates a mask of an hexagon within a height*width image dimension, where height
    # is the height of the hexagon, and width is the horizontal length of the hexagon.
    # The mask is filled with 255, representing the hexagon, and 0, representing the rest of the image.
    # The mask is then used to calculate the mean of the masked hexagon pixels.
    mask = np.zeros((int(height),int(width)), dtype=np.uint8)
    hex_points = []
    for angle in range(0,360,60):
        angle_rad = math.radians(angle)
        x = radius + radius * math.cos(angle_rad)
        y = (int(height)//2) + radius * math.sin(angle_rad)
        hex_points.append((int(x), int(y)))
    points = np.array(hex_points)
    cv2.fillConvexPoly(mask, points, 255)
    return mask

    
# Scaling parameter
long_radius = 10 # Scaling factor: Choose the radius of the circle encompassing the hexagon.

# Hexagon dimensions
h = int(long_radius*math.sqrt(3)) # The height of an hexagon
l = int(long_radius*2) # the width of an hexagon


# Image reading
filename = "image test.jpg" # Path and filename of the image file
image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE) # Read and Convert the image in Grayscale

# Get image size
im_size = image.shape

# Initilization
num_cols = int(im_size[1]// (l*0.75)) # define the number of hexagons in height
num_rows = int(im_size[0]//h) # define the number of hexagons in width
result = np.zeros_like(image) # Initilization of the result image
hex_mask =  Mask_hexagon(long_radius,h,l) # Initilization of the hexagon mask
hex_means = [] # Initialization of the mean intensity values list

# Main 
for row in range(num_rows):
    for col in range(num_cols):
        even = col %2 # Define if the column is even or odd
        x_offset = int(col*l*0.75) # x position
        y_offset = int(row*h + even*(h//2)) # y position with an offset depending in the column parity
        
        # Make sure to not getting out of the image 
        if x_offset + l >= im_size[1] or y_offset + h >= im_size[0]:
            continue
        
        # Crop the image 
        hex_cut = image[y_offset:y_offset + int(h),x_offset:x_offset + int(l)]

        # Apply the hexagon mask to the cropped image to keep only the hexagon's pixels values
        masked_hex = cv2.bitwise_and(hex_cut, hex_cut, mask=hex_mask)
        
        # Compute the mean intensity value.
        mean_value = cv2.mean(masked_hex, mask=hex_mask)[0]
        
        center_x = x_offset + l//2
        center_y = y_offset + h//2
        hex_means.append({'X_position': center_x, "Y_position": center_y, "Intensity value": mean_value})
        
        # Fill the hexagon with the mean intensity value
        filled_hex = np.full_like(masked_hex, int(mean_value))
        hex_with_intensity = cv2.bitwise_and(filled_hex, filled_hex, mask=hex_mask)
        
        # Paste the final hexagon within the result image.
        non_zero_mask = hex_with_intensity > 0
        result[y_offset:y_offset + int(h),x_offset:x_offset + int(l)][non_zero_mask] = hex_with_intensity[non_zero_mask]
        
df = pd.DataFrame(hex_means)     
print(df)

df.to_csv('Intensities.csv')    

cv2.imshow("modified image", result)
cv2.waitKey(0)
