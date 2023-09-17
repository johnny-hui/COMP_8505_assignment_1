import constants
import sys
from os import path
from program2_utils import encode, encrypt_string, payload_to_binary, image_to_binary, parse_arguments, encrypt_image
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

        # Payload Type Check
        if len(string_payload) is not constants.ZERO:  # String Payload
            # Perform Encryption of Payload
            encrypted_key, encrypted_payload = encrypt_string(string_payload)

            # Convert Encrypted Payload to Binary
            encrypted_payload_in_binary = payload_to_binary(encrypted_payload, max_bits_supported)

            # Perform LSB Encoding
            encode(cover_img, encrypted_payload_in_binary)

            # RETURN: Encryption Key

        if len(image_payload_dir) is not constants.ZERO:  # Image Payload
            image_binary = image_to_binary(image_payload_dir, cover_img, max_bits_supported)
            encrypted_key, encrypted_payload = encrypt_image(image_binary)
            encode(cover_img, encrypted_payload)

            # RETURN: Encrypt Key, Image Payload format for program 3 (recovery, decrypting, converting to orig. file)

        # Save the new image
        filename, _ = path.splitext(cover_image_dir)
        filename += '_lsb' + constants.PNG_EXTENSION
        cover_img.save(filename, constants.PNG_FORMAT)

        return encrypted_key
    except OSError:
        sys.exit(constants.OS_ERROR_MSG)


if __name__ == '__main__':
    do_program_2()
