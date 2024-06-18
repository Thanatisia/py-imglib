"""
ImgLib core function unit tests
"""
import os
import sys
from imglib.core.images.io import open as import_file, load_image, save as output_file
from imglib.core.images.pixels import get_image_pixels, get_black_pixels, get_colored_pixels
from imglib.core.images.translation import img_grayscale, extract_populated_areas, convert_black_cells_to_transparent

def test_import_file(img_fname="src.png"):
    """
    Unit Test to import the specified file
    """
    # Initialize Variables
    input_image = None
    token = False
    err_msg = ""

    # Check if file is found
    if os.path.isfile(img_fname):
        # Attempt to import file
        input_image, token, err_msg = import_file(img_fname)
    else:
        err_msg = "File '{}' is not found".format(img_fname)

    # Output/Return
    return [input_image, token, err_msg]
  
def test_load_image(input_image):
    """
    Unit Test to extract the image's pixel map
    """
    pixel_map, token, err_msg = load_image(input_image)
    return [pixel_map, token, err_msg]
  
def test_get_image_size(input_image):
    """
    Unit Test to get image resolution
    """
    # Initialize Variables
    width = 0
    height = 0

    if input_image != None:
        # Extracting the width and height of the image
        width, height = input_image.size

    return [width, height]

def test_check_black_cells(input_image, pixel_map, width, height):
    """
    Unit Test to check for black pixels in the entire image
    """
    ## Get all pixel coordinates and their RGB values
    img_map = get_image_pixels(input_image, pixel_map, width, height)

    ## Get all coordinates with black (0,0,0) pixels
    black_pixel_cells = get_black_pixels(img_map)

    # Output/Return
    return black_pixel_cells

def test_check_colored_cells(input_image, pixel_map, width, height):
    """
    Unit Test to check for non-black pixels in the entire image
    """
    ## Get all pixel coordinates and their RGB values
    img_map = get_image_pixels(input_image, pixel_map, width, height)

    ## Get all coordinates with colors (R,G,B) pixels
    colored_pixel_cells = get_colored_pixels(img_map)

    # Output/Return
    return colored_pixel_cells

def test_image_grayscale(input_image, pixel_map, width, height):
    """
    Unit Test for Grayscaling the specified image
    """
    # Initialize Variables
    token = False
    err_msg = ""

    if input_image != None:
        try:
            img_grayscale(input_image, pixel_map, width, height)
            token = True
        except Exception as ex:
            err_msg = ex
    else:
        err_msg = "Input Image is not provided."

    # Output/Return
    return [token, err_msg]

def test_extract_populated_areas(input_image, pixel_map, width, height):
    """
    Unit Test for Extracting only the colored/populated areas
    """
    # Initialize Variables
    token = False
    err_msg = ""

    if input_image != None:
        try:
            ## Get all pixel coordinates and their RGB values
            img_map = get_image_pixels(input_image, pixel_map, width, height)

            ## Extract colored/populated areas
            extract_populated_areas(input_image, pixel_map, img_map)

            token = True
        except Exception as ex:
            err_msg = ex
    else:
        err_msg = "Input Image is not provided."

    # Output/Return
    return [token, err_msg]

def test_transparency(input_image):
    """
    Unit Test for converting black cells to transparent
    """
    # Initialize Variables
    rgba = None
    token = False
    err_msg = ""

    if input_image != None:
        try:
            # Add a transparency mask layer to the black areas of the image
            rgba = convert_black_cells_to_transparent(input_image)

            token = True
        except Exception as ex:
            err_msg = ex
    else:
        err_msg = "Input Image is not provided."

    # Output/Return
    return [rgba, token, err_msg]

def test_save_output(input_image, output_fname="output", output_format="png"):
    """
    Unit Test for saving the specified file
    """
    # Initialize Variables
    input_image = None
    token = False
    err_msg = ""

    if input_image != None:
        token, err_msg = output_file(input_image, output_fname, output_format)
    else:
        err_msg = "Input Image is not provided."

    # Output/Return
    return [token, err_msg]

def unittest():
    # Unit Test 1: Import file
    img_fname = "src.jpg"
    im, token, err_msg = test_import_file(img_fname)
    if im != None:
        print("[+] Image '{}' opened successfully.".format(img_fname))
    else:
        print("[X] Error encountered while opening image '{}' : {}".format(img_fname, err_msg))

    # Unit Test 2: Import Image Pixel Map
    pixel_map, token, err_msg = test_load_image(im)
    if pixel_map != None:
        print("[+] Image '{}' loaded successfully and obtained pixel map : {}".format(img_fname, pixel_map))
    else:
        print("[X] Error encountered while loading image '{}' : {}".format(img_fname, err_msg))

    # Unit Test 3: Get Image Resolution
    width, height = test_get_image_size(im)
    if width >= 0 and height >= 0:
        print("[+] Width: {}, Height: {}".format(width, height))
    else:
        print("[X] Error encountered while obtaining image resolution")

    # Unit Test 4: Check for black cells
    black_pixel_cells = test_check_black_cells(im, pixel_map, width, height)
    if len(black_pixel_cells) != 0:
        print("[+] Black Pixel Cells Found: {}".format(black_pixel_cells))
    else:
        print("[X] Error encountered while checking for the existence of black pixels in image")

    # Unit Test 5: Check for non-black cells
    colored_pixel_cells = test_check_colored_cells(im, pixel_map, width, height)
    if len(colored_pixel_cells) != 0:
        print("[+] Colored Pixel Cells Found: {}".format(colored_pixel_cells))
    else:
        print("[X] Error encountered while checking for the existence of non-black pixels in image")

    # Unit Test 6: Image Grayscaling
    token, err_msg = test_image_grayscale(im, pixel_map, width, height)
    if token == True:
        print("[+] Grayscaling of Image '{}' executed successfully".format(img_fname))
    else:
        print("[X] Error encountered while grayscaling image '{}' : {}".format(img_fname, err_msg))

    # Unit Test 7: Image File Saving/Output
    out_fname = "output-grayscale"
    out_format = "png"
    token, err_msg = test_save_output(im, out_fname, out_format)
    if token == True:
        print("[+] Saving of Image '{}' to '{}.{}' executed successfully".format(img_fname, out_fname, out_format))
    else:
        print("[X] Error encountered while saving image '{}.{}' : {}".format(out_fname, out_format, err_msg))

    # Unit Test 8: Extracting areas that have color
    token, err_msg = test_extract_populated_areas(im, pixel_map, width, height)
    if token == True:
        print("[+] Extraction of populated pixels in Image '{}' executed successfully".format(img_fname))
    else:
        print("[X] Error encountered while extracting populated pixel in image '{}' : {}".format(img_fname, err_msg))

    # Unit Test 9: Image File Saving/Output
    out_fname = "output-extract"
    out_format = "png"
    token, err_msg = test_save_output(im, out_fname, out_format)
    if token == True:
        print("[+] Saving of Image '{}' to '{}.{}' executed successfully".format(img_fname, out_fname, out_format))
    else:
        print("[X] Error encountered while saving image '{}.{}' : {}".format(out_fname, out_format, err_msg))

    # Unit Test 8: Transparency
    rgba, token, err_msg = test_transparency(im)
    if token == True:
        print("[+] Conversion of black background to transparent in Image '{}' executed successfully".format(img_fname))
    else:
        print("[X] Error encountered while converting the black background to transparent in image '{}' : {}".format(img_fname, err_msg))

    # Unit Test 9: Image File Saving/Output
    out_fname = "output-transparency"
    out_format = "png"
    token, err_msg = test_save_output(rgba, out_fname, out_format)
    if token == True:
        print("[+] Saving of Image '{}' to '{}.{}' executed successfully".format(img_fname, out_fname, out_format))
    else:
        print("[X] Error encountered while saving image '{}.{}' : {}".format(out_fname, out_format, err_msg))

if __name__ == "__main__":
    unittest()

