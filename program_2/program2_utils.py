import getopt
import math
import random
import sys
import constants
from os import path
from PIL import Image


def encrypt_string(payload: str):
    """
    Encrypts a string payload using XOR encryption

    [SOURCE: Modified code from ChatGPT]

    @param payload:
            A string representing the payload.

    @return encryption_key_binary, encrypted_payload:
            A tuple that includes the encryption key and encrypted payload
    """
    # Declarations
    encrypted_payload = ""
    payload_type = constants.STRING_EXTENSION

    # Predefined XOR key (in binary) for ASCII letter 172
    encryption_key = 0b10101010

    # Convert encrypted key to binary
    encryption_key_binary = format(encryption_key, constants.EIGHT_BIT_BINARY)

    # Encrypt the payload using XOR encryption
    for i in range(len(payload)):
        encrypted_payload += chr(ord(payload[i]) ^ ord(encryption_key_binary[i % len(encryption_key_binary)]))

    # print(encrypted_payload)
    # 
    # # Decrypt test
    # decrypt_test = ""
    # for i in range(len(encrypted_payload)):
    #     decrypt_test += chr(ord(encrypted_payload[i]) ^ ord(encryption_key_binary[i % len(encryption_key_binary)]))
    # 
    # print(decrypt_test)

    return encryption_key_binary, encrypted_payload, payload_type


def encrypt(payload_in_binary: str):
    """
    Encrypts any payload that is already in binary using XOR encryption
    (currently used for images and file payload)

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


def encode(img: Image.Image,
           payload_in_binary: str,
           number_of_lsb_to_replace_per_pixel: int):
    """
    Encodes (embeds) the payload in the pixels of the image using bitwise operators and shifting

    @param img:
            An image object

    @param payload_in_binary:
            A string representing the payload (in binary)

    @param number_of_lsb_to_replace_per_pixel:
            An integer representing number of LSBs per pixel to replace

    @return: None
    """
    payload_index = constants.ZERO

    # Loop through each pixel of the image (top down)
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img.getpixel((x, y)))

            # Reset Critical Variables
            bit_position = constants.ZERO
            num_bits_replaced = constants.ZERO

            # Embed payload bits into the least significant bits of RGB channels (using bitwise operators)
            while num_bits_replaced < number_of_lsb_to_replace_per_pixel:

                for i in range(3):  # <== 0 for Red, 1 for Green, 2 for Blue
                    if num_bits_replaced >= number_of_lsb_to_replace_per_pixel:
                        break

                    if payload_index < len(payload_in_binary):
                        pixel[i] = pixel[i] & ~int(math.pow(2,  bit_position)) | int(payload_in_binary[payload_index])
                        payload_index += 1

                    num_bits_replaced += 1

                bit_position += 1

            # Update the pixel in the cover image
            img.putpixel((x, y), tuple(pixel))


def image_to_binary(img_path: str,
                    cover_img: Image.Image,
                    max_bits_supported: int):
    """
    Converts an image to binary

    [SOURCE: Modified code from ChatGPT]

    @param img_path:
            A string representing the image path

    @param cover_img:
            The Image object of the cover image

    @param max_bits_supported:
            An integer representing the max number of bits supported for LSB for steganography

    @return: binary_data_to_string
            A string containing the binary representation of the image
    """

    # Open the image and get mode
    image = Image.open(img_path)
    image_mode = image.mode

    # Check if image is RGB
    if image_mode is not constants.RGB_MODE:
        sys.exit(constants.IMG_PAYLOAD_NOT_RGB_ERROR)

    # Check if Image payload meets requirements (Must be smaller or equal)
    if (image.width > cover_img.width) or (image.height > cover_img.height):
        sys.exit(constants.IMG_PAYLOAD_TOO_LARGE_ERROR)

    # Convert each RGB pixel to binary and store in a list
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

    # Check if image bits supported for cover image
    if len(binary_data_to_string) > max_bits_supported:
        sys.exit(constants.IMG_PAYLOAD_TOO_LARGE_IN_BITS_ERROR)

    return binary_data_to_string


def string_to_binary(payload: str, max_bits_supported_by_lsb: int):
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

    # CHECK: if payload size is less than max amount of bits supported for LSB
    assert (max_bits_supported_by_lsb >= len(payload_in_binary)), \
        (constants.PAYLOAD_SIZE_TOO_LARGE_ERROR.format(max_bits_supported_by_lsb))

    return payload_in_binary


def file_to_binary(file_path: str, max_bits_supported: int):
    """
    Converts any file to binary bits and performs check for eligibility to perform steganography.

    @param file_path:
            A string representing the file path

    @param max_bits_supported:
            An integer representing the max bits supported for current cover image

    @return file_in_binary, file_name, file_extension:
            The file in binary and metadata for program 3 (recovery and decrypting)

    """
    try:
        with open(file_path, constants.READ_BYTE_MODE) as file:
            binary_data = file.read()

            # Get file metadata for program 3 (recovery)
            file_name = file.name.split('/')[-1]
            file_extension = file_name.split('.')[-1]

            # Read each byte and covert into binary
            file_in_binary = ''.join(format(byte, constants.EIGHT_BIT_BINARY) for byte in binary_data)
            print(f"[+] Number of bits for {file_name}: {len(file_in_binary)}")

            # CHECK: if payload size is less than max amount of bits supported for LSB
            assert (max_bits_supported >= len(file_in_binary)), \
                (constants.PAYLOAD_SIZE_TOO_LARGE_ERROR.format(max_bits_supported))

            return file_in_binary, file_name, file_extension
    except IOError as e:
        sys.exit(constants.FILE_OPEN_ERROR.format(e))


def parse_arguments():
    """
    Parses arguments from command line

    @return is_encrypt, cover_image, extra_image, file_directory, string_payload, number_of_bits_per_pixel:
            The arguments for sufficient for proper functioning of program_2
    """
    # Initialization
    is_encrypt, cover_image, extra_image, file_directory, string_payload = False, "", "", "", ""
    number_of_bits_per_pixel = constants.ZERO

    # GetOpt Arguments
    arguments = sys.argv[1:]
    opts, user_list_args = getopt.getopt(arguments, 'e:c:i:f:s:l:')

    if len(opts) == constants.ZERO:
        sys.exit(constants.NO_ARG_ERROR)

    for opt, argument in opts:
        if opt == '-e':
            if str(argument).lower() == constants.TRUE:
                is_encrypt = True
        if opt == '-c':  # For Cover Image
            cover_image = argument
        if opt == '-i':  # For Image Payload
            extra_image = argument
        if opt == '-f':  # For File Payload
            file_directory = argument
        if opt == '-s':  # For String Payload
            string_payload = argument
            if len(string_payload) is constants.ZERO:
                sys.exit(constants.STRING_PAYLOAD_EMPTY_ERROR)
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
    if len(cover_image) == constants.ZERO:
        sys.exit(constants.C_OPTION_INVALID_ARGUMENT_MSG)

    # Set default LSB bits per pixel == 3 if no args provided
    if number_of_bits_per_pixel == constants.ZERO:
        number_of_bits_per_pixel = constants.LSB_MINIMUM

    # Print Configurations
    __print_config(is_encrypt, number_of_bits_per_pixel)

    return is_encrypt, cover_image, extra_image, file_directory, string_payload, number_of_bits_per_pixel


def save_image(cover_img: Image.Image, cover_img_dir: str):
    filename, _ = path.splitext(cover_img_dir)
    filename += '_lsb' + constants.PNG_EXTENSION
    cover_img.save(filename, constants.PNG_FORMAT)
    print(constants.OPERATION_SUCCESSFUL_MSG)


def do_work_strings(cover_img, is_encrypt, max_bits_supported, number_of_lsb_to_replace_per_pixel, string_payload):
    if is_encrypt:
        encrypted_key, encrypted_payload, payload_type = encrypt_string(string_payload)
        encrypted_payload_in_binary = string_to_binary(encrypted_payload, max_bits_supported)
        encode(cover_img, encrypted_payload_in_binary, number_of_lsb_to_replace_per_pixel)
        # RETURN: Encrypt Key, Payload Type (string), no. bits/pixel, isEncrypt = True, Original File Name == None
    else:
        payload_in_binary = string_to_binary(string_payload, max_bits_supported)
        encode(cover_img, payload_in_binary, number_of_lsb_to_replace_per_pixel)
        # RETURN: Encryption Key=None, Payload type (string), no. bits/pixel, isEncrypt = False,
        #         Original File Name == None


def do_work_image_or_file(cover_img, payload_binary, is_encrypted, number_of_lsb_to_replace_per_pixel):
    if is_encrypted:
        encrypted_key, encrypted_payload = encrypt(payload_binary)
        encode(cover_img, encrypted_payload, number_of_lsb_to_replace_per_pixel)
        # RETURN: Encrypt Key and everything below, isEncrypt == True
    else:
        encode(cover_img, payload_binary, number_of_lsb_to_replace_per_pixel)


def __print_config(is_encrypt, number_of_bits_per_pixel):
    print(constants.PROGRAM_CONFIGURATION_BANNER)
    if is_encrypt is False:
        print(constants.ENCRYPTION_DISABLED_MSG)
    else:
        print(constants.ENCRYPTION_ENABLED_MSG)

    print(f"[+] Number of LSBs per pixel to replace: {number_of_bits_per_pixel}")
    print(constants.PROGRAM_CONFIG_ENDING_BANNER)
