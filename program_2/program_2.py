import constants
import sys
from os import path
from program2_utils import encode, encrypt, payload_to_binary
from PIL import Image


def do_program_2(img_dir: str,
                 number_of_lsb_to_replace_per_pixel: int = 0,
                 payload: str = ""):
    try:
        img = Image.open(img_dir)
        max_bits_supported_by_lsb = img.height * img.width * constants.LSB_MINIMUM

        # Perform Encryption of Payload
        encrypted_key, encrypted_payload = encrypt(payload)

        # Convert Encrypted Payload to Binary
        encrypted_payload_in_binary = payload_to_binary(encrypted_payload, max_bits_supported_by_lsb)

        # Perform LSB Encoding
        encode(img, encrypted_payload_in_binary)

        # Save the new image
        filename, _ = path.splitext(img_dir)
        filename += '_lsb' + constants.PNG_EXTENSION
        img.save(filename, constants.PNG_FORMAT)

        return encrypted_key
    except OSError:
        sys.exit(constants.OS_ERROR_MSG)


if __name__ == '__main__':
    do_program_2("../Pictures/24_bit.png", 1, "I am Vladimir the hacker")
