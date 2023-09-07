from PIL import Image
import constants
import sys


def do_program_1(img_dir):
    try:
        img = Image.open(img_dir)
        width, height = img.size

        print(f"Image Properties: {img.format}, {img.mode}")
        print(f"Number of Pixels: {width * height}")
        print(f"Starting Pixel Position (0,0): {list(img.getpixel((0,0)))}")
    except OSError:
        sys.exit(constants.OS_ERROR_MSG)


if __name__ == '__main__':
    do_program_1("/home/johnny/PycharmProjects/COMP_8505_assignment_1/24_bit.png")
