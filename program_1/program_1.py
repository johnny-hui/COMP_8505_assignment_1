import constants
import sys
from program1_utils import determine_payload_size, param_check, png_check
from PIL import Image


def do_program_1(img_dir: str,
                 number_of_lsb_to_replace_per_pixel: int = 0):
    """
    Reads cover image and determines how large a payload can be hidden, given the number of LSBs
    (The Least Significant Bits) per pixel to replace per user choice.

    @param img_dir:
        A string representing the image path to be analyzed

    @param number_of_lsb_to_replace_per_pixel:
        An int representing number of LSBs to replace (default 0)

    @return: None

    """
    try:
        img = Image.open(img_dir)

        # Check if PNG format
        png_check(img)

        # Param Check
        param_check(number_of_lsb_to_replace_per_pixel)

        # Get Dimensions
        width, height = img.size
        total_pixels = width * height
        print(f"Total Number of Pixels: {total_pixels}")

        # Determine payload size possible to be hidden (given user number of bits/pixel)
        print(f"Payload Size (Chosen {number_of_lsb_to_replace_per_pixel} bits per pixel to replace)"
              f": {determine_payload_size(total_pixels, number_of_lsb_to_replace_per_pixel)} bits")

        # Determine payload size required for LSB (minimal change to image quality)
        print(f"Minimal Payload Size Requirement for LSB (3 bits per pixel): "
              f"{total_pixels * constants.LSB_MINIMUM} bits")

        # Max Payload Size of Image (If chosen to Replace All 8 bits per channel)
        print(f"Maximum Payload Size for Image (24 bits per pixel): {(total_pixels * constants.MAX_BIT_DEPTH)} bits")

        return None

    except OSError:
        sys.exit(constants.OS_ERROR_MSG)


# MAIN (for testing)
if __name__ == '__main__':
    do_program_1("../Pictures/24_bit.png", 22)
