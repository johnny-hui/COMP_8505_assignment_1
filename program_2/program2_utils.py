import constants
from PIL import Image


def encrypt(payload: str):
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


def encode(img: Image.Image, payload_in_binary: str):
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

            # SUGGESTION: Darcy wants user to be able to declare how many LSBs per pixels to replace
            # (Use While Loop + Counter??)

            # Update the pixel in the cover image
            img.putpixel((x, y), tuple(pixel))


def payload_to_binary(payload: str, max_bits_supported_by_lsb: int):
    # Convert the encrypted payload to binary (Char -> ASCII Integer -> 8-bit binary conversion per character)
    encrypted_payload_in_binary = ''.join(format(ord(char), constants.EIGHT_BIT_BINARY) for char in payload)
    print(f"Number of Bits: {len(encrypted_payload_in_binary)}")

    # CHECK: on payload size and max amount of bits supported using LSB
    assert (max_bits_supported_by_lsb >= len(encrypted_payload_in_binary)), \
        (constants.PAYLOAD_SIZE_TOO_LARGE_ERROR.format(max_bits_supported_by_lsb))

    return encrypted_payload_in_binary
