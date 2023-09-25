ZERO = 0
POWER_SEVEN = 7
EIGHT_BIT_BINARY = 8
FILE_READ = "r"
FILE_OPEN_ERROR = "[+] ERROR: An error has occurred while opening the file provided: {}"
NO_ARG_ERROR = "[+] NO_ARG_ERROR: No arguments were passed in!"
C_OPTION_INVALID_ARGUMENT_MSG = "[+] ERROR: No argument was provided for -c (Cover Image) option!"
F_OPTION_INVALID_ARGUMENT_MSG = "[+] ERROR: No argument was provided for -f (Metadata File) option!"

RGB_MODE = "RGB"
PNG_FORMAT = "PNG"
IMG_PAYLOAD_NOT_RGB_ERROR = "[+] ERROR: The image payload is not of RGB color mode!"
TYPE_STRING = "string"
TYPE_IMAGE = "image"
TYPE_FILE = "file"
UNICODE_FORMAT = "utf-8"
MODE_WRITE_BINARY = "wb"
MODE_WRITE = "w"

PROGRAM_CONFIGURATION_BANNER = "====================== // PROGRAM CONFIGURATIONS // ======================"
PROGRAM_CONFIG_ENDING_BANNER = "=========================================================================="
PROGRAM_CONFIG_STEG_IMG_MSG = "[+] Steganographed Image: {}"
PROGRAM_CONFIG_METADATA_MSG = "[+] Metadata File: {}"
OPERATION_STRING_MSG = "[+] Now recovering string payload from cover image..."
OPERATION_IMAGE_MSG = "[+] Now recovering image payload from cover image..."
OPERATION_FILE_MSG = "[+] Now recovering file payload from cover image..."

METADATA_FILE_VALIDATE_FIRST_LINE = "number_of_bits_per_pixel"
NOT_METADATA_FILE_ERROR = "[+] ERROR: File is not a metadata file from program 2!"
METADATA_PAYLOAD_LENGTH = "payload_length_bits"
METADATA_ITEM_ONE = "Number of bits per pixel"
METADATA_ITEM_TWO = "Is Payload Encrypted"
METADATA_ITEM_THREE = "Encryption Key"
METADATA_ITEM_FOUR = "Original Payload Type"
METADATA_ITEM_FIVE = "Original Payload Extension Type"
METADATA_ITEM_SIX = "Original Payload File Name"
METADATA_ITEM_SEVEN = "Original Payload Length Bit"

RECOVERY_DIRECTORY_NAME = "recovered_payload"
RECOVERY_DIRECTORY_CREATED = "[+] A recovered_payload directory has been created (in current directory)!"
DIRECTORY_EXISTS_WARNING_MSG = "[+] WARNING: A recovered_payload directory already exists within current directory!"
RECOVERED_TAG_FILE_NAME = '_recovered'

FILE_IO_ERROR = "[+] ERROR: An error has occurred while writing to file: {}"
FILE_RECOVERY_SUCCESS_MSG = "[+] OPERATION SUCCESS: File has been saved to '{}' as '{}'"
IMAGE_RECOVERY_SUCCESS_MSG = "[+] OPERATION SUCCESS: Image saved in '{}' as {}"