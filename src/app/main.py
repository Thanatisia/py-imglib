"""
Image Specification Identifier
- Iterate through every pixel in the imported image and reports the image specifications
"""
import os
import sys
from PIL import Image

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

def img_grayscale(input_image, pixel_map, width, height, factor=0, orientation="x"):
    """
    Convert and Map the image with a gray tint (grayscaling) based on the factor, as well as the target orientation to apply the grayscale to (only applicable if the grayscale fraction is more than 0)

    :: Params
    
    """
    # Check factor (What fraction of the image to grayscale)
    # 2 = 1/2
    if factor > 0:
        # Check the orientation to apple the grayscale to (Only applicable if the grayscale factor > 0)
        match orientation:
            case "x":
                for i in range(width//factor): 
                    for j in range(height): 
                        # getting the RGB pixel value. 
                        r, g, b = input_image.getpixel((i, j)) 
                  
                        # Apply formula of grayscale: 
                        grayscale = (0.299*r + 0.587*g + 0.114*b) 
          
                        # setting the pixel value. 
                        pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale)) 
            case "y":
                for i in range(width): 
                    for j in range(height//factor): 
                        # getting the RGB pixel value. 
                        r, g, b = input_image.getpixel((i, j)) 
                  
                        # Apply formula of grayscale: 
                        grayscale = (0.299*r + 0.587*g + 0.114*b) 
          
                        # setting the pixel value. 
                        pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale)) 
    else:
        for i in range(width): 
            for j in range(height): 
                # getting the RGB pixel value. 
                r, g, b = input_image.getpixel((i, j)) 
                  
                # Apply formula of grayscale: 
                grayscale = (0.299*r + 0.587*g + 0.114*b) 
          
                # setting the pixel value. 
                pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale)) 

def main():
    # Initialize Variables
    action = ["metadata", "image-pixels", "check-black-cells", "check-colored-cells", "grayscale"]
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
    input_image = Image.open(img_fname) 
  
    # Extracting pixel map: 
    pixel_map = input_image.load() 
  
    # Extracting the width and height
    # of the image: 
    width, height = input_image.size 

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
  
            # Saving the final output 
            # as "grayscale.png": 
            input_image.save("grayscale.png", format="png") 
  
            # use input_image.show() to see the image on the 
            # output screen.     
        case _:
            # Default Value
            print("Invalid action: {}".format(action))

if __name__ == "__main__":
    main()
