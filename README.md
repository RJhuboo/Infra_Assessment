# Infra_assessment

This project is part of the INFRA assessment. It aims to transform a grayscale image into a set of hexagons, where each hexagon is colored with the mean intensity value of the image within that hexagon (see the picture below). In other words, we create an image where the pixels are hexagons. The code takes an image and a scaling factor as input, and outputs an image and the mean intensity values for each hexagon.

<img src="image_test.jpg" width="400" />
Figure 1: Input image that is converted afterward in grayscale.


<img src="Output/result.jpg" width="400" />
Figure 2: Output image

## Requirements

This code uses opencv, numpy, pandas, math, argparse. All the required packages are presented in the requirement.txt that you can download using the following line in your terminal
```
pip install requirements.txt
```

## How to use

The code is called main.py. Just run main.py to use the code. Two parameters can be tuned : filename and long_radius. The first one represents the path and name of the image and the second is the radius of the circle that encompass the hexagon.
The higher is the long_radius value and the bigger will be the hexagons.
To run the code, you can use the following line: 

```
py main.py --filename image_test.jpg --long_radius 10
```
Please change the ```py``` depending on your configuration (e.g. ```py3```,```python```, ...)
Two images are available for testing the code : "image_test.jpg" and "cameraman.jpg".

## What is the output ? 

The code outputs an image that is saved in the Output directory. It also save the file intensities.csv, inside the Output folder, that contains the mean intensity values of each hexagons as well as the coordinates of their center (X_position,Y_position).
