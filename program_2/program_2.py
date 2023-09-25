import constants
import sys
from program2_utils import (image_to_binary, parse_arguments, file_to_binary, save_image,
                            do_work_strings, do_work_image_or_file, save_metadata)
from PIL import Image


def do_program_2():
    """
    Performs embedding and optional encryption of payload into a cover image using Least
    Significant Bit (LSB) technique

    @return: None
    """
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
            metadata_list = do_work_strings(cover_img, isEncrypt, max_bits_supported,
                                            number_of_lsb_to_replace_per_pixel, string_payload)
            save_image(cover_img, cover_image_dir)
            save_metadata(metadata_list)
            return None

        if len(image_payload_dir) is not constants.ZERO:  # Image Payload
            print(constants.OPERATION_IMAGE_MSG)
            (image_binary, extension_type, file_name, payload_length_bits,
             [image_mode, image_width, image_height]) = image_to_binary(image_payload_dir, cover_img, max_bits_supported)

            metadata_list = do_work_image_or_file(cover_img, image_binary,
                                                  isEncrypt, number_of_lsb_to_replace_per_pixel,
                                                  constants.TYPE_IMAGE, extension_type, file_name, payload_length_bits,
                                                  [image_mode, image_width, image_height])

            save_image(cover_img, cover_image_dir)
            save_metadata(metadata_list)
            return None

        if len(file_payload_dir) is not constants.ZERO:  # File Payload
            print(constants.OPERATION_FILE_MSG)
            file_in_binary, file_name, file_extension, payload_length_bits = file_to_binary(file_payload_dir,
                                                                                            max_bits_supported)
            metadata_list = do_work_image_or_file(cover_img, file_in_binary,
                                                  isEncrypt, number_of_lsb_to_replace_per_pixel,
                                                  constants.TYPE_FILE, file_extension, file_name, payload_length_bits,
                                                  [])
            save_image(cover_img, cover_image_dir)
            save_metadata(metadata_list)
            return None

    except IOError as e:
        sys.exit(constants.FILE_OPEN_ERROR.format(e))


if __name__ == '__main__':
    do_program_2()
