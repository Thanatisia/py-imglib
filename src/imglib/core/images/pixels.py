"""
Pixel/Cells-related Image Manipulation functions and handling
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops

def get_image_pixels(input_image, pixel_map, width, height):
    """
    Iterate through the image and return a dictionary (key-value) mapping all the points and cell/pixels values making up the image
    """
    # Initialize Variables
    image_map = {
        # (x,y) : [r,g,b]
    }

    # Iterate through the image pixel by pixel across the row and down the columns and map the color density of that pixel (black/white) to the current X value (row number)
    for i in range(width): 
        for j in range(height): 
            # getting the RGB pixel value. 
            r, g, b = input_image.getpixel((i, j)) 
                  
            # Map the current pixel's RGB value to the current row x column
            image_map[i,j] = [r,g,b]

    # Output/Return
    return image_map

def get_black_pixels(image_map):
    """ 
    Iterate through the image mappings and Check for cells with black pixels (r=0,g=0,b=0)
    """
    # Initialize Variables
    found_rows = {}

    # Iterate through the image mappings
    for coordinates, img_pixels in image_map.items():
        # Get coordinates row and column
        curr_row = coordinates[0]
        curr_col = coordinates[1]

        # Check for cells with black pixels (r=0,g=0,b=0)
        if image_map[coordinates] == [0,0,0]:
            # print("{} = {}".format(coord, img_pixels))
            found_rows[curr_row, curr_col] = img_pixels

    # Return/Output
    return found_rows

def get_colored_pixels(image_map):
    """ 
    Iterate through the image mappings and Check for cells with colored pixels (r>0,g>0,b>0)
    """
    # Initialize Variables
    found_rows = {}

    # Iterate through the image mappings
    for coordinates, img_pixels in image_map.items():
        # Get coordinates row and column
        curr_row = coordinates[0]
        curr_col = coordinates[1]

        # Get color values
        R = img_pixels[0]
        G = img_pixels[1]
        B = img_pixels[2]

        # Check for cells with colored pixels (r>0,g>0,b>0)
        if not (img_pixels == [0,0,0]):
            # print("{} = {}".format(coord, img_pixels))
            found_rows[curr_row, curr_col] = img_pixels

    # Return/Output
    return found_rows


