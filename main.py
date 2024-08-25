import numpy as np
import cv2
import math
import pandas as pd
import argparse

# Arguments of the program
parser = argparse.ArgumentParser(
                    prog='Hexagonized image',
                    description='Transform an image into a set of hexagons',
                    epilog='')
parser.add_argument('--filename',default="image_test.jpg",type=str,help="Image filename and path") 
parser.add_argument('--long_radius', default=10,type=int,help="The radius of the hexagon (must be an integer)")      

args = parser.parse_args()

class Hexagon:
    # Hexagon object
    def __init__(self,radius):
        self.radius = radius
        self.h = int(radius*math.sqrt(3)) # The height of an hexagon
        self.l = int(radius*2) # the width of an hexagon
        self.mask = self.Mask_hexagon()
        self.mean_value = None
        
    def Mask_hexagon(self):
        
        # This function creates a mask of an hexagon within a h*l image dimension, where h
        # is the height of the hexagon, and l is the horizontal length of the hexagon.
        # The mask is filled with 255, representing the hexagon, and 0, representing the rest of the image.
        # The mask is then used to calculate the mean of the masked hexagon pixels.
        
        mask = np.zeros((int(self.h),int(self.l)), dtype=np.uint8)
        hex_points = []
        for angle in range(0,360,60):
            angle_rad = math.radians(angle)
            x = self.radius + self.radius * math.cos(angle_rad)
            y = (int(self.h)//2) + self.radius * math.sin(angle_rad)
            hex_points.append((int(x), int(y)))
        points = np.array(hex_points)
        cv2.fillConvexPoly(mask, points, 255)
        return mask

    def apply_mask(self, image,x_offset,y_offset):
        
        # This function apply the mask into the image at the position (x_offset,y_offset).
        
        # Crop the image 
        hex_cut = image[y_offset:y_offset + int(self.h),x_offset:x_offset + int(self.l)]

        # Apply the hexagon mask to the cropped image to keep only the hexagon's pixels values
        masked_hex = cv2.bitwise_and(hex_cut, hex_cut, mask=self.mask)
        
        # Compute the mean intensity value.
        self.mean_value = cv2.mean(masked_hex, mask=self.mask)[0]
        return self.mean_value



if __name__ == '__main__':
     
    # Scaling parameter
    long_radius = args.long_radius # Scaling factor: Choose the radius of the circle encompassing the hexagon.


    # Image reading
    filename = args.filename # Path and filename of the image file
    image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE) # Read and Convert the image in Grayscale

    # Get image size
    im_size = image.shape

    # Initilization of the object "Hexagon"
    hexagon = Hexagon(long_radius)

    # Initilization
    num_cols = int(im_size[1]// (hexagon.l*0.75)) # define the number of hexagons in height
    num_rows = int(im_size[0]//hexagon.h) # define the number of hexagons in width
    result = np.zeros_like(image) # Initilization of the result image
    hex_means = [] # Initialization of the mean intensity values list

    # Main 
    for row in range(num_rows):
        for col in range(num_cols):
            even = col %2 # Define if the column is even or odd
            x_offset = int(col*hexagon.l*0.75) # x position
            y_offset = int(row*hexagon.h + even*(hexagon.h//2)) # y position with an offset depending in the column parity
            
            # Make sure to not getting out of the image 
            if x_offset + hexagon.l >= im_size[1] or y_offset + hexagon.h >= im_size[0]:
                continue
            
            # Compute the mean intensity value
            intensity_value = hexagon.apply_mask(image, x_offset, y_offset)
            
            # Compute the position of the hexagon's center.
            center_x = x_offset + hexagon.l//2
            center_y = y_offset + hexagon.h//2

            # Save the mean intensity value into a list
            hex_means.append({'X_position': center_x, "Y_position": center_y, "Intensity value": intensity_value})
            
            # Fill the hexagon with the mean intensity value
            filled_hex = np.full_like(hexagon.mask, int(intensity_value))
            hex_with_intensity = cv2.bitwise_and(filled_hex, filled_hex, mask=hexagon.mask)
            
            # Paste the final hexagon within the result image.
            non_zero_mask = hex_with_intensity > 0
            result[y_offset:y_offset + int(hexagon.h),x_offset:x_offset + int(hexagon.l)][non_zero_mask] = hex_with_intensity[non_zero_mask]
            
    # Create the dataframe
    df = pd.DataFrame(hex_means)     
    print(df)

    # Save the dataframe into a csv file
    df.to_csv('Intensities.csv')    

    # Dispaly the result
    cv2.imshow("modified image", result)
    cv2.waitKey(0)

    # Save image in the output directory
    cv2.imwrite("Output/result.jpg",result)