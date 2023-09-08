import constants
import sys


def determine_payload_size(total_pixels: int,
                           number_of_lsb_to_replace_per_pixel: int):

    return total_pixels * number_of_lsb_to_replace_per_pixel


def param_check(number_of_lsb_to_replace_per_pixel: int):
    if number_of_lsb_to_replace_per_pixel > constants.MAX_BIT_DEPTH:
        sys.exit(constants.NUM_BITS_TO_REPLACE_EXCEEDED_ERROR)

    if number_of_lsb_to_replace_per_pixel < constants.ZERO:
        sys.exit(constants.NUM_BITS_ERROR_NEGATIVE)
