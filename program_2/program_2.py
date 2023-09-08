import sys
import constants
from PIL import Image


def do_program_2(img_dir: str,
                 number_of_lsb_to_replace_per_pixel: int = 0,
                 payload_size: int = 0):
    try:
        img = Image.open(img_dir)
        width, height = img.size

        # Create new image map of original image
        new_image = Image.new("RGB", (width, height), "white")
        pixels = new_image.load()

        # Transform to grayscale (Starting at (0,0))
        for x in range(width):
            for y in range(height):
                # Get Pixel
                pixel = img.getpixel((x, y))

                # Get R, G, B values (These are int from 0 to 255)
                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                # Transform to grayscale
                gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)

                # Set Pixel in new image
                pixels[x, y] = (int(gray), int(gray), int(gray))

        new_image.save("ass.png", "png")
    except OSError:
        sys.exit(constants.OS_ERROR_MSG)
