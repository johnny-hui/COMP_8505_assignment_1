import constants
import sys
from program2_utils import (encode, encrypt_string, string_to_binary, image_to_binary,
                            parse_arguments, encrypt, file_to_binary, save_image, do_work_strings,
                            do_work_image_or_file)
from PIL import Image


def do_program_2():
    try:
        # GetOpts
        (isEncrypt, cover_image_dir, image_payload_dir, file_payload_dir,
         string_payload, number_of_lsb_to_replace_per_pixel) = parse_arguments()

        # Open Cover Image
        cover_img = Image.open(cover_image_dir)
        max_bits_supported = cover_img.height * cover_img.width * number_of_lsb_to_replace_per_pixel

        # Payload Type Check
        if len(string_payload) is not constants.ZERO:  # String Payload
            print(constants.OPERATION_STRING_MSG)
            do_work_strings(cover_img, isEncrypt, max_bits_supported,
                            number_of_lsb_to_replace_per_pixel, string_payload)
            save_image(cover_img, cover_image_dir)
            return None

        if len(image_payload_dir) is not constants.ZERO:  # Image Payload
            print(constants.OPERATION_IMAGE_MSG)
            image_binary = image_to_binary(image_payload_dir, cover_img, max_bits_supported)

            do_work_image_or_file(cover_img, image_binary, isEncrypt, number_of_lsb_to_replace_per_pixel)

            save_image(cover_img, cover_image_dir)
            return None
            # RETURN: Encrypt_key, Payload type == Image, Original file name, Extension Type(png, jpg), No. bits/pixel,
            #         isEncrypt == False

        if len(file_payload_dir) is not constants.ZERO:  # File Payload
            print(constants.OPERATION_FILE_MSG)
            file_in_binary, file_name, file_extension = file_to_binary(file_payload_dir, max_bits_supported)

            do_work_image_or_file(cover_img, file_in_binary, isEncrypt, number_of_lsb_to_replace_per_pixel)

            save_image(cover_img, cover_image_dir)
            return None
            # RETURN: Encrypt_key == None, Payload Type == File, Extension Type (zip, rar, txt, etc.),
            #         Original File Name, No. Bits per pixel, isEncrypt == False
    except OSError:
        sys.exit(constants.OS_ERROR_MSG)


if __name__ == '__main__':
    do_program_2()
