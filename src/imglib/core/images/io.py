"""
Image I/O Handling and Processing functions
"""
import os
import sys
from PIL import Image

def open(img_fname="src.png"):
    """
    Import an image from the specified source file name
    """
    # Initialize Variables
    token = False
    err_msg = ""
    im = None

    try:
        # Try to open the specified file as an image and import into the system buffer
        im = Image.open(img_fname)

        # Set success token
        token = True
    except Exception as ex:
        # Set error message
        err_msg = ex

    # Return/Output
    return [im, token, err_msg]
  
def load_image(input_image):
    """
    Extracting pixel map from the image
    """
    # Initialize Variables
    token = False
    err_msg = ""
    pixel_map = None

    try:
        # Try to load the image and return the image buffer as a pixel map
        pixel_map = input_image.load() 

        # Set success token
        token = True
    except Exception as ex:
        # Set error message
        err_msg = ex

    # Return/Output
    return [pixel_map, token, err_msg]

def save(input_image, out_fname="output", format="PNG"):
    """
    Save the image buffer into the specified output file as the specified image format
    """
    # Initialize Variables
    token = False
    err_msg = ""

    try:
        # Try to save the input image to the output file
        input_image.save("{}.{}".format(out_fname, format.lower()), format)

        # Set success token
        token = True
    except Exception as ex:
        # Set error message
        err_msg = ex

    # Return/Output
    return [token, err_msg]

