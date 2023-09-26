import getopt
import os

import constants
import sys
from PIL import Image


def parse_arguments():
    # Print Banner
    print(constants.PROGRAM_CONFIGURATION_BANNER)

    # Initialization
    cover_img_dir = ""
    number_of_bits_per_pixel = constants.ZERO

    # GetOpt Arguments
    arguments = sys.argv[1:]
    opts, _ = getopt.getopt(arguments, 'c:l:')

    if len(opts) == constants.ZERO:
        sys.exit(constants.NO_ARG_ERROR)

    for opt, argument in opts:
        if opt == '-c':  # For Cover Image
            if os.path.exists(argument):
                cover_img_dir = argument
            else:
                sys.exit(constants.C_OPTION_INVALID_PATH_ERROR)
        if opt == '-l':  # For Number of LSBs per pixel
            try:
                number_of_bits_per_pixel = int(argument)
                if number_of_bits_per_pixel > constants.MAX_LSB_LIMIT_PER_PIXEL:
                    sys.exit(constants.BITS_PER_PIXEL_UPPER_BOUND_ERROR)
                if number_of_bits_per_pixel <= constants.ZERO:
                    sys.exit(constants.BITS_PER_PIXEL_LOWER_BOUND_ERROR)
            except ValueError:
                sys.exit(constants.L_OPTION_INVALID_ARGUMENT_MSG)

    # Check to force user to provide a cover image to perform LSB on
    if len(cover_img_dir) == constants.ZERO:
        sys.exit(constants.C_OPTION_INVALID_ARGUMENT_MSG)

    # Set default LSB bits per pixel == 3 if no args provided
    if number_of_bits_per_pixel == constants.ZERO:
        print(constants.L_OPTION_NO_ARG_WARNING_MSG)
        print(constants.L_OPTION_DEFAULT_SETTING_MSG)
        number_of_bits_per_pixel = constants.LSB_MINIMUM

    # Print Information
    print(constants.CONFIG_COVER_IMG.format(cover_img_dir))
    print(constants.CONFIG_BITS_PER_PIXEL.format(number_of_bits_per_pixel))
    print(constants.PROGRAM_CONFIG_ENDING_BANNER)

    return cover_img_dir, number_of_bits_per_pixel


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
