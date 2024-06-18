"""
Image Translation/Transformation/Conversion functions
"""
import os
import sys
from imglib.core.images.pixels import get_colored_pixels
from PIL import Image, ImageDraw, ImageFilter, ImageChops

def color_transform(r, g, b, r_Factor=1, g_Factor=1, b_Factor=1, preset=""):
    """
    Tranform the colors based on the pro
    """
    # Initialize Variables
    presets = {
        "grayscale" : (0.299*r + 0.587*g + 0.114*b)
    }

    # Check if preset is provided
    if preset != "":
        # Not empty - provided
        # Transform the colorset according to the presets
        transformed_color = presets[preset]
    else:
        # Transform the colorset by multiplying the color factors and adding them together
        transformed_color = (r_Factor*r + g_Factor*g + b_Factor*b)

    # Return/Output
    return transformed_color

def convert_black_cells_to_transparent(input_image):
    """
    Convert the image to an RGBA value and convert all black areas into a transparent mask layer and return the RGBA object to the caller
    """
    # Obtain the image mode
    image_mode = input_image.mode

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

    return rgba

def img_grayscale(input_image, pixel_map, width, height, factor=0, orientation="x"):
    """
    Convert and Map the image with a gray tint (grayscaling) based on the factor, as well as the target orientation to apply the grayscale to (only applicable if the grayscale fraction is more than 0)

    :: Params
    
    """
    # Obtain the image mode
    image_mode = input_image.mode

    # Check factor (What fraction of the image to grayscale)
    # 2 = 1/2
    if factor > 0:
        # Check the orientation to apple the grayscale to (Only applicable if the grayscale factor > 0)
        match orientation:
            case "x":
                for i in range(width//factor): 
                    for j in range(height): 
                        # Check if input image contains an alpha
                        if image_mode != "RGBA":
                            # getting the RGB pixel value. 
                            r, g, b = input_image.getpixel((i, j)) 
                      
                            # Apply formula of grayscale: 
                            grayscale = (0.299*r + 0.587*g + 0.114*b) 
              
                            # setting the pixel value. 
                            pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale)) 
                        else:
                            # getting the RGB pixel value. 
                            r, g, b, a = input_image.getpixel((i, j)) 
                      
                            # Apply formula of grayscale: 
                            grayscale = (0.299*r + 0.587*g + 0.114*b) 
              
                            # setting the pixel value. 
                            pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale), int(a))
            case "y":
                for i in range(width): 
                    for j in range(height//factor): 
                        # Check if input image contains an alpha
                        if image_mode != "RGBA":
                            # getting the RGB pixel value. 
                            r, g, b = input_image.getpixel((i, j)) 
                      
                            # Apply formula of grayscale: 
                            grayscale = (0.299*r + 0.587*g + 0.114*b) 
              
                            # setting the pixel value. 
                            pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale)) 
                        else:
                            # getting the RGB pixel value. 
                            r, g, b, a = input_image.getpixel((i, j)) 
                      
                            # Apply formula of grayscale: 
                            grayscale = (0.299*r + 0.587*g + 0.114*b) 
              
                            # setting the pixel value. 
                            pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale), int(a)) 
    else:
        for i in range(width): 
            for j in range(height): 
                # Check if input image contains an alpha
                if image_mode != "RGBA":
                    # getting the RGB pixel value. 
                    r, g, b = input_image.getpixel((i, j)) 
                      
                    # Apply formula of grayscale: 
                    grayscale = (0.299*r + 0.587*g + 0.114*b) 
              
                    # setting the pixel value. 
                    pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale))
                else:
                    # getting the RGB pixel value. 
                    r, g, b, a = input_image.getpixel((i, j)) 
                      
                    # Apply formula of grayscale: 
                    grayscale = (0.299*r + 0.587*g + 0.114*b) 
              
                    # setting the pixel value. 
                    pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale), int(a))

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



 
