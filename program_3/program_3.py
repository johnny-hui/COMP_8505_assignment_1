import constants
from program_3_utils import parse_arguments, get_metadata_info


def do_program_3():
    # GetOpts
    cover_img_dir, metadata_file_dir = parse_arguments()

    # Get Metadata Info
    metadata_info = get_metadata_info(metadata_file_dir)

    # Decode



if __name__ == '__main__':
    do_program_3()
