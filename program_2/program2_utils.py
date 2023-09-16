import getopt
import random
import sys
import constants
from PIL import Image


def encrypt_string(payload: str):
    """
    Encrypts a string payload using XOR encryption

    @param payload:
            A string representing the payload.

    @return encryption_key_binary, encrypted_payload:
            A tuple that includes the encryption key and encrypted payload
    """
    # Declarations
    encrypted_payload = ""

    # Randomly Generate XOR key (in binary)
    encryption_key = 0b10101010

    # Convert encrypted key to binary
    encryption_key_binary = format(encryption_key, constants.EIGHT_BIT_BINARY)

    # Encrypt the payload using XOR encryption
    for i in range(len(payload)):
        encrypted_payload += chr(ord(payload[i]) ^ ord(encryption_key_binary[i % len(encryption_key_binary)]))

    return encryption_key_binary, encrypted_payload


def encrypt_image(payload_in_binary: str):
    """
    Encrypts an image payload (already in binary) using XOR encryption
    [SOURCE: Modified code from ChatGPT]

    @param payload_in_binary:
            A string representing the image payload in binary

    @return encryption_key, encrypted_payload
            A randomly generated encryption key and the encrypted payload
    """
    # Generate random encryption key (has to be same length as payload)
    encryption_key = ''.join([str(random.randint(0, 1)) for _ in range(len(payload_in_binary))])

    # Perform XOR Encryption on image payload with generated key (operation in parallel using zip())
    encrypted_payload_list = []
    for binary_bit in payload_in_binary:
        encrypted_bit = "".join(str(int(bit) ^ int(encrypted_bit)) for bit, encrypted_bit in zip(binary_bit,
                                                                                                 encryption_key))
        encrypted_payload_list.append(encrypted_bit)

    # Convert Encrypted Payload from List to String
    encrypted_payload = ""
    for bit in encrypted_payload_list:
        encrypted_payload += bit

    return encryption_key, encrypted_payload


def encode(img: Image.Image, payload_in_binary: str):
    """
    Encodes (embeds) the payload in the pixels of the image using bitwise operators

    @param img:
            An image object

    @param payload_in_binary:
            A string representing the payload (in binary)

    @return: None
    """
    payload_index = constants.ZERO

    # Loop through each pixel of the image (top down)
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img.getpixel((x, y)))

            # Embed payload bits into the least significant bits of RGB channels (using bitwise operators)
            for i in range(3):  # <== 0 for Red, 1 for Green, 2 for Blue
                if payload_index < len(payload_in_binary):
                    pixel[i] = pixel[i] & ~1 | int(payload_in_binary[payload_index])
                    payload_index += 1

            # IMPLEMENT 2: Darcy wants user to be able to declare how many LSBs per pixels to replace
            #              (Use While Loop + Counter??)

            # Update the pixel in the cover image
            img.putpixel((x, y), tuple(pixel))


def image_to_binary(img_path: str, cover_img: Image.Image):
    """
    Converts an image to binary
    [SOURCE: Modified code from ChatGPT]

    @param img_path:
            A string representing the image path

    @param cover_img:
            The Image object of the cover image

    @return: binary_data_to_string
            A string containing the binary representation of the image
    """

    # Open the image
    image = Image.open(img_path)

    # Check if Image payload meets requirements (Must be smaller or equal)
    if (image.width > cover_img.width) or (image.height > cover_img.height):
        sys.exit(constants.IMG_PAYLOAD_TOO_LARGE_ERROR)

    # Convert each pixel to binary and store in a list
    binary_data = []

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            binary_value = "".join(format(channel, constants.EIGHT_BIT_BINARY) for channel in pixel)
            binary_data.append(binary_value)

    # Convert binary_data (array) to string
    binary_data_to_string = ""
    for pixel_in_binary in binary_data:
        binary_data_to_string += pixel_in_binary

    return binary_data_to_string


def payload_to_binary(payload: str, max_bits_supported_by_lsb: int):
    """
    Converts any payload to binary and provides a check for suitable conditions to perform LSB

    @note: Use Case
        Image payloads does not require the use of this function!

    @param payload:
            A string representing the payload

    @param max_bits_supported_by_lsb:
            An integer representing the maximum bits supported to perform LSB

    @return payload_in_binary:
            A string representing the payload in binary.
    """

    # Convert the encrypted payload to binary (Char -> ASCII Integer -> 8-bit binary conversion per character)
    payload_in_binary = ''.join(format(ord(char), constants.EIGHT_BIT_BINARY) for char in payload)
    print(f"Number of Bits: {len(payload_in_binary)}")

    # CHECK: if payload size is less than max amount of bits supported for LSB
    assert (max_bits_supported_by_lsb >= len(payload_in_binary)), \
        (constants.PAYLOAD_SIZE_TOO_LARGE_ERROR.format(max_bits_supported_by_lsb))

    return payload_in_binary


def parse_arguments():
    """
    Parses arguments from command line

    @return cover_image, extra_image, file_directory, string_payload, number_of_bits_per_pixel:
            The arguments for sufficient for proper functioning of program_2
    """
    # Initialization
    cover_image, extra_image, file_directory, string_payload = "", "", "", ""
    number_of_bits_per_pixel = constants.ZERO

    # GetOpt Arguments
    arguments = sys.argv[1:]
    opts, user_list_args = getopt.getopt(arguments, 'c:i:f:s:l')

    if len(opts) == constants.ZERO:
        sys.exit(constants.NO_ARG_ERROR)

    for opt, argument in opts:
        if opt == '-c':  # For Cover Image
            cover_image = argument
        if opt == '-i':  # For Image Payload
            extra_image = argument
        if opt == '-f':  # For File Payload
            file_directory = argument
        if opt == '-s':  # For String Payload
            string_payload = argument
        if opt == '-l':  # For Number of LSBs per pixel
            try:
                number_of_bits_per_pixel = int(argument)
            except ValueError:
                sys.exit(constants.L_OPTION_INVALID_ARGUMENT_MSG)

    # Check to force user to provide a cover image to perform LSB on
    if len(cover_image) == constants.ZERO:
        sys.exit(constants.C_OPTION_INVALID_ARGUMENT_MSG)

    # Check to force user to have at least one other argument
    if len(extra_image) or len(file_directory) or len(string_payload) == constants.ZERO:
        sys.exit(constants.INSUFFICIENT_ARGS_MSG)

    # Set default LSB bits per pixel == 3 if no args provided
    if number_of_bits_per_pixel == constants.ZERO:
        number_of_bits_per_pixel = constants.LSB_MINIMUM

    return cover_image, extra_image, file_directory, string_payload, number_of_bits_per_pixel


if __name__ == '__main__':
    img = Image.open("../Pictures/24_bit.png")
    image_binary = image_to_binary("../Pictures/24_bit.png", img)
    encrypt_image(image_binary)
