OS_ERROR_MSG = "[+] ERROR: Cannot open file at specified directory!"
PAYLOAD_SIZE_TOO_LARGE_ERROR = ("[+] ERROR: Payload (in binary) is greater than the bit capacity supported to "
                                "perform LSB steganography for the current image: {} bits")
PROGRAM_CONFIGURATION_BANNER = "====================== // PROGRAM CONFIGURATIONS // ======================"
PROGRAM_CONFIG_ENDING_BANNER = "=========================================================================="

PNG_FORMAT = "PNG"
PNG_EXTENSION = ".png"
PNG_EXTENSION_TWO = "png"
JPG_EXTENSION = "jpg"
GIF_EXTENSION = "gif"
TIFF_EXTENSION = "tif"

TYPE_STRING = "string"
TYPE_IMAGE = "image"
TYPE_FILE = "file"
TRUE = "true"
FILE_WRITE = 'w'

EIGHT_BIT_BINARY = "08b"
ZERO = 0
LSB_MINIMUM = 3
BASE_TWO = 2
ENCRYPTED_KEY_LENGTH = 1
ENCRYPTION_ENABLED_MSG = "[+] Encryption has been enabled!"
ENCRYPTION_DISABLED_MSG = "[+] Encryption has been disabled!"

NO_ARG_ERROR = "[+] NO_ARG_ERROR: No arguments were passed in!"
L_OPTION_INVALID_ARGUMENT_MSG = "[+] ERROR: Invalid Argument for -l option!"
C_OPTION_INVALID_ARGUMENT_MSG = "[+] ERROR: No argument was provided for -c (Cover Image) option!"
INSUFFICIENT_ARGS_MSG = ("[+] ERROR: Please provide at least one argument for payload "
                         "using either the '-i', '-f', '-s' options!")

IMG_PAYLOAD_TOO_LARGE_ERROR = ("[+] ERROR: The image payload (dimension-wise) must be smaller than or equal "
                               "to the cover image!")
RGB_MODE = "RGB"
IMG_PAYLOAD_NOT_RGB_ERROR = "[+] ERROR: The image payload is not of RGB color mode!"
IMG_PAYLOAD_TOO_LARGE_IN_BITS_ERROR = ("[+] ERROR: The image payload (in bits) is too large to support LSB "
                                       "steganography for the current cover image! Consider increasing the "
                                       "bits per pixel (-l option).")
STRING_PAYLOAD_EMPTY_ERROR = "[+] ERROR: The string payload (-s) provided cannot be empty!"

MAX_LSB_LIMIT_PER_PIXEL = 24
BITS_PER_PIXEL_UPPER_BOUND_ERROR = "[+] ERROR: The number of LSBs per pixel (-l) provided cannot exceed 24 bits!"
BITS_PER_PIXEL_LOWER_BOUND_ERROR = "[+] ERROR: The number of LSBs per pixel (-l) provided cannot be negative or zero!"
FILE_OPEN_ERROR = "[+] ERROR: An error has occurred while opening the file provided: {}"
READ_BYTE_MODE = "rb"
OPERATION_SUCCESSFUL_MSG = "[+] OPERATION COMPLETE: Now terminating program 2..."
FILE_INVALID_ERROR_MSG = "[+] ERROR: Invalid file format provided for the -f option!"

OPERATION_STRING_MSG = "[+] Now encrypting and encoding string payload into cover image..."
OPERATION_IMAGE_MSG = "[+] Now encrypting and encoding image payload into cover image..."
OPERATION_FILE_MSG = "[+] Now encrypting and encoding file payload into cover image..."
DIRECTORY_CREATION_WARNING_MSG = "[+] WARNING: A metadata directory already exists within current directory!"

METADATA_DIRECTORY_NAME = "metadata"
METADATA_DIRECTORY_CREATED = "[+] A /metadata directory has been created (in current directory)!"
METADATA_TEXT_FILE_NAME = "metadata.txt"
METADATA_ITEM_ONE = "number_of_bits_per_pixel="
METADATA_ITEM_TWO = "is_encrypted="
METADATA_ITEM_THREE = "encryption_key="
METADATA_ITEM_FOUR = "payload_type="
METADATA_ITEM_FIVE = "payload_extension_type="
METADATA_ITEM_SIX = "payload_file_name="
