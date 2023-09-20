import constants
import sys
from os import path
from program2_utils import (encode, encrypt_string, string_to_binary, image_to_binary,
                            parse_arguments, encrypt, file_to_binary)
from PIL import Image


def do_program_2():
    try:
        # GetOpts
        (cover_image_dir, image_payload_dir, file_payload_dir,
         string_payload, number_of_lsb_to_replace_per_pixel) = parse_arguments()

        # Open Cover Image
        cover_img = Image.open(cover_image_dir)
        max_bits_supported = cover_img.height * cover_img.width * number_of_lsb_to_replace_per_pixel

        # Declaring Variables
        encrypted_key = ""
        payload_type = ""

        # Payload Type Check
        if len(string_payload) is not constants.ZERO:  # String Payload
            print(constants.OPERATION_STRING_MSG)
            encrypted_key, encrypted_payload, payload_type = encrypt_string(string_payload)
            encrypted_payload_in_binary = string_to_binary(encrypted_payload, max_bits_supported)
            encode(cover_img, encrypted_payload_in_binary)

            # RETURN: Encryption Key, Payload type (string for recovery)

        if len(image_payload_dir) is not constants.ZERO:  # Image Payload
            print(constants.OPERATION_IMAGE_MSG)
            image_binary = image_to_binary(image_payload_dir, cover_img, max_bits_supported)
            encrypted_key, encrypted_payload = encrypt(image_binary)
            encode(cover_img, encrypted_payload)

            # RETURN: Encrypt Key, Payload type (Image Mode or format), Original file name

        if len(file_payload_dir) is not constants.ZERO:  # File Payload
            print(constants.OPERATION_FILE_MSG)
            file_in_binary, file_name, file_extension = file_to_binary(file_payload_dir, max_bits_supported)
            encrypted_key, encrypted_payload = encrypt(file_in_binary)
            encode(cover_img, encrypted_payload)

            # RETURN: Encrypt key, Payload (File) Type (zip, rar, txt, etc.), Original File Name

        # Save the new image
        filename, _ = path.splitext(cover_image_dir)
        filename += '_lsb' + constants.PNG_EXTENSION
        cover_img.save(filename, constants.PNG_FORMAT)
        print(constants.OPERATION_SUCCESSFUL_MSG)

        return encrypted_key
    except OSError:
        sys.exit(constants.OS_ERROR_MSG)


if __name__ == '__main__':
    do_program_2()
