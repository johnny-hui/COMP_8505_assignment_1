import constants
import sys
from program1_utils import determine_payload_size, param_check, png_check, parse_arguments
from PIL import Image


def do_program_1():
    """
    Reads cover image and determines how large a payload can be hidden, given the number of LSBs
    (The Least Significant Bits) per pixel to replace per user choice.

    @return: None
    """
    # Parse Arguments (via. GetOps)
    cover_img_dir, number_of_lsb_to_replace_per_pixel = parse_arguments()

    try:
        img = Image.open(cover_img_dir)

        # Check if PNG format
        png_check(img)

        # Param Check
        param_check(number_of_lsb_to_replace_per_pixel)

        # Get Dimensions
        width, height = img.size
        total_pixels = width * height
        print(f"[+] Total Number of Pixels: {total_pixels}")

        # Determine payload size possible to be hidden (given user number of bits/pixel)
        print(f"[+] Required Payload Size must be less than or equal to"
              f": {determine_payload_size(total_pixels, number_of_lsb_to_replace_per_pixel)} bits")

        # Determine payload size required for LSB (minimal change to image quality)
        print(f"[+] Minimal Payload Size Requirement for LSB (3 bits per pixel): "
              f"{total_pixels * constants.LSB_MINIMUM} bits")

        # Max Payload Size of Image (If chosen to Replace All 8 bits per channel)
        print(f"[+] Maximum Payload Size for Image (24 bits per pixel): {(total_pixels * constants.MAX_BIT_DEPTH)} bits")

        return None
    except OSError:
        sys.exit(constants.OS_ERROR_MSG)


# MAIN (for testing)
if __name__ == '__main__':
    do_program_1()
