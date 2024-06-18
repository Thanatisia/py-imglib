"""
Functions to obtain metadata and information from images
"""
import os
import sys

def get_image_size(input_image):
    """
    Extract the width and height of the image
    """
    # Initialize Variables
    width = 0
    height = 0

    # Try to get the width and height from the image's resolution
    width, height = input_image.size

    return [width, height]

def get_image_color_mode(input_image):
    """
    Get the color mode of the image (i.e. RGB/RGBA)
    """
    # Obtain the image mode
    image_mode = input_image.mode
    return image_mode

