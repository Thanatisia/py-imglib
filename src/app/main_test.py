"""
Image Specification Identifier
- Iterate through every pixel in the imported image and reports the image specifications
"""
import os
import sys
from imglib.core.images.io import open as import_file, load_image, save as output_file
from imglib.core.images.pixels import get_image_pixels, get_black_pixels, get_colored_pixels
from imglib.core.images.translation import img_grayscale, extract_populated_areas, convert_black_cells_to_transparent
from imglib.core.images.information import get_image_size

def main():
    # Initialize Variables
    action = ["metadata", "image-pixels", "check-black-cells", "check-colored-cells", "grayscale", "extract-colored", "transparency"]
    img_fname = "src.jpg"
    action_id = 3

    # Get CLI arguments
    exec = sys.argv[0]
    argv = sys.argv[1:]
    argc = len(argv)

    # Get file information
    if argc >= 1:
        img_fname = argv[0]

    # Get target action ID
    if argc >= 2:
        action_id = int(argv[1])

    # Import an image from directory: 
    input_image, token, err_msg = import_file(img_fname)
  
    # Extracting pixel map: 
    pixel_map, token, err_msg = load_image(input_image)
  
    # Extracting the width and height
    # of the image: 
    width, height = get_image_size(input_image)

    match action[action_id]:
        case "metadata":
            print("Width: {}, Height: {}, Pixel Map: {}".format(width, height, pixel_map))
        case "image-pixels":
            print(get_image_pixels(input_image, pixel_map, width, height))
        case "check-black-cells":
            # Check for black pixels in the entire image
            ## Get all pixel coordinates and their RGB values
            img_map = get_image_pixels(input_image, pixel_map, width, height)
            ## Get all coordinates with black (0,0,0) pixels
            black_pixel_cells = get_black_pixels(img_map)
            print(black_pixel_cells)
        case "check-colored-cells":
            # Check for non-black pixels in the entire image
            ## Get all pixel coordinates and their RGB values
            img_map = get_image_pixels(input_image, pixel_map, width, height)
            ## Get all coordinates with colors (R,G,B) pixels
            colored_pixel_cells = get_colored_pixels(img_map)
            print(colored_pixel_cells)
        case "grayscale":
            # Grayscale half of the image  
            img_grayscale(input_image, pixel_map, width, height)
  
            # Saving the final output as "grayscale.png"
            output_file(input_image, "grayscale", format="png")
  
            # use input_image.show() to see the image on the 
            # output screen.
        case "extract-colored":
            # Extract only the colored/populated areas
            ## Get all pixel coordinates and their RGB values
            img_map = get_image_pixels(input_image, pixel_map, width, height)
            ## Extract colored/populated areas
            extract_populated_areas(input_image, pixel_map, img_map)
            ## Saving the image as color extracted
            output_file(input_image, "color-extracted", format="png")
        case "transparency":
            # Add a transparency mask layer to the black areas of the image
            rgba = convert_black_cells_to_transparent(input_image)

            # Saving the final output as the output file 'transparency.png'
            output_file(rgba, "transparency", format="png")
        case _:
            # Default Value
            print("Invalid action: {}".format(action))

if __name__ == "__main__":
    main()
