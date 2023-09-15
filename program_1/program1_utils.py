import constants
import sys
from PIL import Image


def determine_payload_size(total_pixels: int,
                           number_of_lsb_to_replace_per_pixel: int):
    """
    A utility function that determines payload size per user argument

    @param total_pixels:
        An integer representing the total number of pixels of the current cover image

    @param number_of_lsb_to_replace_per_pixel:
        An integer representing the number of LSBs to replace per pixel

    @return: None

    """
    return total_pixels * number_of_lsb_to_replace_per_pixel


def param_check(number_of_lsb_to_replace_per_pixel: int):
    """
    A utility function that performs parameter checks for program_1

    @param number_of_lsb_to_replace_per_pixel:
        An integer representing the number of LSBs to replace per pixel

    @return: None

    """
    if number_of_lsb_to_replace_per_pixel > constants.MAX_BIT_DEPTH:
        sys.exit(constants.NUM_BITS_TO_REPLACE_EXCEEDED_ERROR)

    if number_of_lsb_to_replace_per_pixel < constants.ZERO:
        sys.exit(constants.NUM_BITS_ERROR_NEGATIVE)


def png_check(image: Image.Image):
    """
    Checks if image is of PNG format and is 24-bit (RGB) color

    @param image:
        An Image object

    @return: None

    """
    if image.format != constants.PNG_FORMAT:
        sys.exit(constants.NOT_PNG_ERROR)

    # Check if RGB (24-bit format)
    if image.mode != constants.PNG_FORMAT_RGB:
        sys.exit(constants.NOT_PNG_24_BIT_ERROR)
