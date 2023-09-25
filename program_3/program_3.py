import constants
from program_3_utils import (parse_arguments, get_metadata_info, decode,
                             decrypt_string, binary_to_string, decrypt,
                             payload_to_image, payload_to_file)


def do_program_3():
    # GetOpts
    cover_img_dir, metadata_file_dir = parse_arguments()

    # Get Metadata Info
    metadata_info = get_metadata_info(metadata_file_dir)

    # Decode
    recovered_payload_binary = decode(cover_img_dir, metadata_info[6], metadata_info[0])

    # Payload Check
    if metadata_info[3] == constants.TYPE_STRING:  # String Payload
        print(constants.OPERATION_STRING_MSG)

        if eval(metadata_info[1]) is True:  # If Encrypted
            decrypted_payload = decrypt_string(metadata_info[2], recovered_payload_binary)
            print(decrypted_payload)
        else:
            original_payload = binary_to_string(recovered_payload_binary)
            print({original_payload})

        return None

    if metadata_info[3] == constants.TYPE_IMAGE:  # Image Payload
        print(constants.OPERATION_IMAGE_MSG)

        if eval(metadata_info[1]) is True:
            decrypted_payload = decrypt(metadata_info[2], recovered_payload_binary)
            payload_to_image(decrypted_payload, metadata_info[5], metadata_info[4])
        else:
            payload_to_image(recovered_payload_binary, metadata_info[5], metadata_info[4])

        return None

    if metadata_info[3] == constants.TYPE_FILE:  # File Payload
        print(constants.OPERATION_FILE_MSG)

        if eval(metadata_info[1]) is True:
            decrypted_payload = decrypt(metadata_info[2], recovered_payload_binary)
            payload_to_file(decrypted_payload, metadata_info[5], metadata_info[4])
        else:
            payload_to_file(recovered_payload_binary, metadata_info[5], metadata_info[4])

        return None


if __name__ == '__main__':
    do_program_3()
