"""
Image Specification Identifier
- Iterate through every pixel in the imported image and reports the image specifications
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

def convert_black_cells_to_transparent(input_image):
    """
    Convert the image to an RGBA value and convert all black areas into a transparent mask layer and return the RGBA object to the caller
    """
    # Convert image to RGBA
    rgba = input_image.convert("RGBA")

    # Create a mask to make the background transparent
    mask = Image.new('L', input_image.size, 0)
    draw = ImageDraw.Draw(mask)
    
    # Define the bounding box for the circle
    width, height = input_image.size
    bbox = [0, 0, width, height]
    
    # Draw a filled white circle in the mask
    draw.ellipse(bbox, fill=255)

    # Smooth the mask to reduce artifacts
    mask = mask.filter(ImageFilter.GaussianBlur(2))

    # Create a mask for black pixels
    r,g,b,a = rgba.split()

    # Composite the new alpha channel with the existing alpha channel
    new_alpha = ImageChops.multiply(a, mask)

    # Create a new image with the updated alpha channel
    input_image.putalpha(new_alpha)

    # Get the image data
    rgba_data = rgba.getdata()

    # Iterate through the image mappings
    transparency_list = []
    black_threshold = 5 # Define the threshold for near-black pixels
    for pixel_values in rgba_data:
        # Get RGB value of the current pixel
        R = pixel_values[0]
        G = pixel_values[1]
        B = pixel_values[2]

        # Check if the pixel is near black (Adjust threshold as necessary)
        if R <= black_threshold and G <= black_threshold and B <= black_threshold:
            # Near-black colour found (RGB values are almost zero)
            # Make pixel transparent (set alpha to 0)
            transparency_list.append((R,G,B,0))
        else:
            # Not black - store the original pixel as per normal
            transparency_list.append(pixel_values)  # other colours remain unchanged

    # Update image with new pixel data
    rgba.putdata(transparency_list)

    """
    # Create a transparency mask to apply to all black areas in the image
    mask = Image.new("L", input_image.size, color=255)

    # Draw a new transparency mask image using the mask object to attach to all black areas
    transparency_mask = ImageDraw.Draw(mask)

    # Iterate through the black cells
    transparent_area = [(0,0), (width, height)]

    for coordinates, pixel_values in black_cells.items():
        # Obtain transparency area (transparency area is a list containing of the following format [x1,y1,x2,y2,...] where X = row and Y = column)
        row = coordinates[0]
        col = coordinates[1]

    # Draw a rectangle on the black cells to be converted to transparent
    transparency_mask.rectangle(transparent_area, fill=0)

    # Put the transparency mask as an alpha to the image
    input_image.putalpha(mask)
    """
    return rgba

def extract_populated_areas(input_image, pixel_map, image_map, out_fname="out", format="png"):
    """
    Remove all black areas (Unpopulated) of the image
    """
    # Obtain colored points
    colored_cells = get_colored_pixels(image_map)

    # Iterate through the colored cells
    for coordinates, pixel_values in colored_cells.items():
        # Obtaining the X (row) and Y (column) values
        row = coordinates[0]
        col = coordinates[1]

        # Obtaining the color values
        R = pixel_values[0]
        G = pixel_values[1]
        B = pixel_values[2]

        # setting the pixel value. 
        pixel_map[row, col] = (int(R), int(G), int(B)) 

    # Saving the final output 
    # as the specified filename
    input_image.save("{}.{}".format(out_fname, format), format)

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
        case "extract-colored":
            # Extract only the colored/populated areas
            ## Get all pixel coordinates and their RGB values
            img_map = get_image_pixels(input_image, pixel_map, width, height)
            ## Extract colored/populated areas
            extract_populated_areas(input_image, pixel_map, img_map)
        case "transparency":
            # Add a transparency mask layer to the black areas of the image
            rgba = convert_black_cells_to_transparent(input_image)

            # Saving the final output 
            # as the output file 'transparency.png'
            rgba.save("transparency.png", format="PNG") 
        case _:
            # Default Value
            print("Invalid action: {}".format(action))

if __name__ == "__main__":
    main()
