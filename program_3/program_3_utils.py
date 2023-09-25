import getopt
import sys
from io import TextIOWrapper
from PIL import Image
import constants


def parse_arguments():
    # Initialization
    cover_image_dir, metadata_file_dir = "", ""

    # GetOpt Arguments
    arguments = sys.argv[1:]
    opts, user_list_args = getopt.getopt(arguments, 'c:f:')

    if len(opts) == constants.ZERO:
        sys.exit(constants.NO_ARG_ERROR)

    for opt, argument in opts:
        if opt == '-c':
            try:
                Image.open(argument)
                cover_image_dir = argument
            except IOError as e:
                sys.exit(constants.FILE_OPEN_ERROR.format(e))

        if opt == '-f':
            try:
                open(argument, mode=constants.FILE_READ)
                metadata_file_dir = argument
            except IOError as e:
                sys.exit(constants.FILE_OPEN_ERROR.format(e))

    # Check to force user to provide a cover image
    if len(cover_image_dir) == constants.ZERO:
        sys.exit(constants.C_OPTION_INVALID_ARGUMENT_MSG)

    # Check to ensure user provides a metadata file
    if len(metadata_file_dir) == constants.ZERO:
        sys.exit(constants.F_OPTION_INVALID_ARGUMENT_MSG)

    # Print Configurations
    __print_config(cover_image_dir, metadata_file_dir)

    return cover_image_dir, metadata_file_dir


def get_metadata_info(metadata_file_dir: str):
    metadata_info = []
    metadata_item_headers = [constants.METADATA_ITEM_ONE, constants.METADATA_ITEM_TWO, constants.METADATA_ITEM_THREE,
                             constants.METADATA_ITEM_FOUR, constants.METADATA_ITEM_FIVE, constants.METADATA_ITEM_SIX,
                             constants.METADATA_ITEM_SEVEN]

    with open(metadata_file_dir, mode=constants.FILE_READ) as file:
        first_line = file.readline().strip()

        if first_line.split("=")[0] == constants.METADATA_FILE_VALIDATE_FIRST_LINE:
            metadata_info.append(int(first_line.split("=")[-1]))
            for line in file:
                if line.split("=")[0] == constants.METADATA_PAYLOAD_LENGTH:
                    metadata_info.append(int(line.split("=")[-1]))
                    continue
                metadata_info.append(line.strip().split("=")[-1])
        else:
            sys.exit(constants.NOT_METADATA_FILE_ERROR)

    __print_metadata_info(metadata_info, metadata_item_headers)

    return metadata_info


def decode(cover_img_dir: str, payload_length: int, number_of_lsb_per_pixel: int):
    image = Image.open(cover_img_dir)

    # Check if image is RGB
    if image.mode is not constants.RGB_MODE:
        sys.exit(constants.IMG_PAYLOAD_NOT_RGB_ERROR)

    # Extract each LSB from each pixel and store in list
    extracted_binary_data = []

    # Loop through each pixel of the image (top down)
    for x in range(image.width):
        for y in range(image.height):
            pixel = list(image.getpixel((x, y)))

            # Reset Critical Variables
            bit_position = constants.ZERO
            num_bits_recovered = constants.ZERO




    # RETURN: binary_data_bits (from list -> string)


def __print_config(cover_image_dir: str, metadata_file_dir: str):
    print(constants.PROGRAM_CONFIGURATION_BANNER)
    print(constants.PROGRAM_CONFIG_STEG_IMG_MSG.format(cover_image_dir))
    print(constants.PROGRAM_CONFIG_METADATA_MSG.format(metadata_file_dir))


def __print_metadata_info(metadata_info, metadata_item_headers):
    index = constants.ZERO

    for item in metadata_info:
        if index == len(metadata_item_headers):
            break
        if index == 2:
            index += 1
            continue
        print(f"[+] {metadata_item_headers[index]}: {item}")
        index += 1

    print(constants.PROGRAM_CONFIG_ENDING_BANNER)


if __name__ == '__main__':
    print("BINARY BIT SHIFTING TEST")
