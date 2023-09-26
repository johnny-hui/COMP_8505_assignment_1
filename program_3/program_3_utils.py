import getopt
import os
import sys
from PIL import Image
import constants


def parse_arguments():
    """
    Parses arguments from command line

    @return cover_image_dir, metadata_file_dir:
            Strings containing the paths for steganographed image and metadata file
    """
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
    """
    Parses information from metadata file saved from program 2

    @param metadata_file_dir:
            A string representing the path of the metadata file

    @return metadata_info
            A list of properties from program 2
    """
    metadata_info = []
    metadata_item_headers = [constants.METADATA_ITEM_ONE, constants.METADATA_ITEM_TWO, constants.METADATA_ITEM_THREE,
                             constants.METADATA_ITEM_FOUR, constants.METADATA_ITEM_FIVE, constants.METADATA_ITEM_SIX,
                             constants.METADATA_ITEM_SEVEN, constants.METADATA_ITEM_EIGHT]

    with open(metadata_file_dir, mode=constants.FILE_READ) as file:
        first_line = file.readline().strip()

        if first_line.split("=")[0] == constants.METADATA_FILE_VALIDATE_FIRST_LINE:
            metadata_info.append(int(first_line.split("=")[-1]))
            for line in file:  # Read 2nd line onwards
                if line.split("=")[0] == constants.METADATA_PAYLOAD_LENGTH:
                    metadata_info.append(int(line.split("=")[-1]))
                    continue
                if line.split("=")[0] == constants.METADATA_IMG_PROPERTIES:
                    metadata_info.append(eval(line.strip().split("=")[-1]))
                    continue
                metadata_info.append(line.strip().split("=")[-1])
        else:
            sys.exit(constants.NOT_METADATA_FILE_ERROR)

    __print_metadata_info(metadata_info, metadata_item_headers)

    return metadata_info


def decode(cover_img_dir: str, payload_length: int, number_of_lsb_per_pixel: int):
    """
    Decodes the binary payload from an LSB steganographed image

    @param cover_img_dir:
            A string representing the path of steganographed image

    @param payload_length:
            An integer representing the original payload (bit) length

    @param number_of_lsb_per_pixel:
            An integer representing the number of LSBs per pixel

    @return extracted_binary_data_str:
            A string containing the binary bits of the original payload (maybe encrypted)
    """
    image = Image.open(cover_img_dir)
    total_num_bits_recovered = constants.ZERO

    # Check if image is RGB
    if image.mode is not constants.RGB_MODE:
        sys.exit(constants.IMG_PAYLOAD_NOT_RGB_ERROR)

    # Extract each LSB from each pixel and store in list
    extracted_binary_data = []
    extracted_binary_data_str = ""

    # Loop through each pixel of the image (top down)
    for x in range(image.width):
        for y in range(image.height):
            pixel = list(image.getpixel((x, y)))

            # Reset Critical Variables
            bit_position = constants.POWER_SEVEN
            num_bits_recovered_per_pixel = constants.ZERO

            while num_bits_recovered_per_pixel < number_of_lsb_per_pixel:

                for i in range(3):  # <== 0 for Red, 1 for Green, 2 for Blue
                    if num_bits_recovered_per_pixel >= number_of_lsb_per_pixel:
                        break

                    # If total number of bits recovered reaches max, stop iterating pixels (break 1)
                    if total_num_bits_recovered >= payload_length:
                        break

                    recovered_lsb = "{0:b}".format(pixel[i]).zfill(8)[bit_position]  # Convert channel value + get LSB
                    extracted_binary_data.append(recovered_lsb)

                    num_bits_recovered_per_pixel += 1
                    total_num_bits_recovered += 1

                # If total number of bits recovered reaches max, stop iterating pixels (break 2)
                if total_num_bits_recovered >= payload_length:
                    break
                else:
                    bit_position -= 1

            # If total number of bits recovered reaches max, stop iterating pixels (break 3)
            if total_num_bits_recovered >= payload_length:
                break

        # If total number of bits recovered reaches max, stop iterating pixels (break 4)
        if total_num_bits_recovered >= payload_length:
            break

    # Convert List to String
    for bit in extracted_binary_data:
        extracted_binary_data_str += bit

    return extracted_binary_data_str


def decrypt_string(encrypt_key: str, encrypted_payload: str):
    """
    Takes an encrypted binary payload, converts it into UTF-8 encoding, then decrypts the string using
    an encryption key and reverse XOR encryption for recovery of the original string payload

    @param encrypt_key:
            A string representing the encryption key

    @param encrypted_payload:
            A string containing binary data recovered from steganographed image

    @return decrypted_payload:
            A string containing the decrypted payload
    """

    # Convert 8-bit binary chunks into bytes back into a string of characters
    decoded_string = binary_to_string(encrypted_payload)

    decrypted_payload = ""
    for i in range(len(decoded_string)):
        decrypted_payload += chr(ord(decoded_string[i]) ^ ord(encrypt_key[i % len(encrypt_key)]))

    return decrypted_payload


def decrypt(encrypt_key: str, encrypted_payload: str):
    """
    Decrypts the original payload by using reverse XOR encryption and a XOR encryption key

    @param encrypt_key:
            A string representing the XOR key

    @param encrypted_payload:
            A string containing the original payload in binary bits

    @return decrypted_payload:
            A string containing the decrypted payload in binary bits
    """
    print(constants.DECRYPTION_START_MSG)
    decrypted_payload_list = []

    # Perform Reverse XOR Encryption on encrypted payload with key (operation in parallel using zip())
    for binary_bit in encrypted_payload:
        encrypted_bit = "".join(str(int(bit) ^ int(encrypted_bit)) for bit, encrypted_bit in zip(binary_bit,
                                                                                                 encrypt_key))
        decrypted_payload_list.append(encrypted_bit)

    # Convert Decrypted Payload from List to String
    decrypted_payload = ""
    for bit in decrypted_payload_list:
        decrypted_payload += bit

    print(constants.DECRYPTION_SUCCESS_MSG)
    return decrypted_payload


def payload_to_image(decrypted_payload: str,
                     file_name: str,
                     file_extension: str,
                     img_properties: list):
    """
    Converts the binary representation of the original payload into bytes and
    encodes them into an image file

    [SOURCES USED: Code from ChatGPT]

    @param decrypted_payload:
            A string containing the original payload (in binary)

    @param file_name:
            A string containing the original file name (from metadata)

    @param file_extension:
            A string containing the file extension (such as .png, .tiff, etc.)

    @param img_properties:
            A list containing the properties of the original image (Mode, Width, Height)

    @return: None
    """
    # Split binary bits into 8-bit chunks -> convert each 8-bit chunk back into decimal
    byte_data = bytes(int(decrypted_payload[i:i + 8], 2) for i in range(constants.ZERO,
                                                                        len(decrypted_payload),
                                                                        constants.EIGHT_BIT_BINARY))

    # Make directory to store recovered payload
    current_path = os.getcwd()
    __make_recovered_payload_directory()

    # Change Directory
    os.chdir(f"{current_path}/{constants.RECOVERY_DIRECTORY_NAME}")

    # String concatenate new file name
    new_file_name = file_name.split(".")[0]
    new_file_name += constants.RECOVERED_TAG_FILE_NAME + '.' + file_extension

    # Save bytes into image file and save
    image = Image.frombytes(img_properties[0], (img_properties[1], img_properties[2]), byte_data)  # Mode, Width, Height
    image.save(new_file_name)
    image.close()

    print(constants.IMAGE_RECOVERY_SUCCESS_MSG.format(os.getcwd(), new_file_name))


def payload_to_file(decrypted_payload: str, file_name: str, file_extension: str):
    """
    Converts the binary representation of the original payload into bytes and
    encodes them into any file

    @param decrypted_payload:
            A string containing the original payload (in binary)

    @param file_name:
            A string containing the original file name (from metadata)

    @param file_extension:
            A string containing the file extension (such as .txt, .zip, .rar)

    @return: None
    """

    # Convert binary bits (from string) into bytes
    if file_extension == constants.ZIP_EXTENSION:  # For Zip files
        byte_data = bytes(int(decrypted_payload[i:i + 8], 2) for i in range(constants.ZERO,
                                                                            len(decrypted_payload),
                                                                            constants.EIGHT_BIT_BINARY))

    if file_extension == constants.TXT_EXTENSION:  # For Txt files
        byte_data = bytes(int(decrypted_payload[i:i + 8], 2) for i in range(constants.ZERO,
                                                                            len(decrypted_payload),
                                                                            constants.EIGHT_BIT_BINARY))

    # Make directory to store recovered payload
    current_path = os.getcwd()
    __make_recovered_payload_directory()

    # Change Directory
    os.chdir(f"{current_path}/{constants.RECOVERY_DIRECTORY_NAME}")

    # Parse New Name
    new_file_name = file_name.split(".")[0]
    new_file_name += constants.RECOVERED_TAG_FILE_NAME + '.' + file_extension

    # Create new file and write
    try:
        if file_extension == constants.ZIP_EXTENSION:  # For Zip files
            with open(new_file_name, constants.MODE_WRITE_BINARY) as zip_file:
                zip_file.write(byte_data)

        if file_extension == constants.TXT_EXTENSION:  # For Txt files
            with open(new_file_name, constants.MODE_WRITE_BINARY) as text_file:
                text_file.write(byte_data)

        print(constants.FILE_RECOVERY_SUCCESS_MSG.format(os.getcwd(), new_file_name))
    except IOError as e:
        print(constants.FILE_IO_ERROR.format(e))


def binary_to_string(encrypted_payload: str):
    """
    Converts 8-bit binary chunks into bytes, then back into a string of characters

    [SOURCES USED: Code from ChatGPT]

    @param encrypted_payload:
            A string containing decoded binary bits recovered from steganographed image

    @return decoded_string:
            A string containing the original string payload of characters
    """
    byte_data = bytes(int(encrypted_payload[i:i + 8], 2) for i in range(constants.ZERO,
                                                                        len(encrypted_payload),
                                                                        constants.EIGHT_BIT_BINARY))
    decoded_string = byte_data.decode(constants.UNICODE_FORMAT)
    return decoded_string


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


def __make_recovered_payload_directory():
    try:
        os.mkdir(constants.RECOVERY_DIRECTORY_NAME)
        print(constants.RECOVERY_DIRECTORY_CREATED)
    except FileExistsError:
        print(constants.DIRECTORY_EXISTS_WARNING_MSG)
