OS_ERROR_MSG = "[+] ERROR: Cannot open file at specified directory!"
PAYLOAD_SIZE_TOO_LARGE_ERROR = ("[+] ERROR: Payload (in binary) is greater than the bit capacity supported to "
                                "perform LSB steganography for the current image: {} bits")
PROGRAM_CONFIGURATION_BANNER = "====================== // PROGRAM CONFIGURATIONS // ======================"
PROGRAM_CONFIG_ENDING_BANNER = "========================================================================"

PNG_FORMAT = "PNG"
PNG_EXTENSION = ".png"
STRING_EXTENSION = "str"
TRUE = "true"

EIGHT_BIT_BINARY = "08b"
ZERO = 0
LSB_MINIMUM = 3
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
IMG_PAYLOAD_TOO_LARGE_IN_BITS_ERROR = ("[+] ERROR: The image payload is too large to support LSB steganography"
                                       " for the current cover image!")
STRING_PAYLOAD_EMPTY_ERROR = "[+] ERROR: The string payload (-s) provided cannot be empty!"

MAX_LSB_LIMIT_PER_PIXEL = 24
BITS_PER_PIXEL_UPPER_BOUND_ERROR = "[+] ERROR: The number of LSBs per pixel (-l) provided cannot exceed 24 bits!"
BITS_PER_PIXEL_LOWER_BOUND_ERROR = "[+] ERROR: The number of LSBs per pixel (-l) provided cannot be negative or zero!"
FILE_OPEN_ERROR = "[+] ERROR: An error has occurred while opening the file provided: {}"
READ_BYTE_MODE = "rb"
OPERATION_SUCCESSFUL_MSG = "[+] OPERATION COMPLETE: Now terminating program 2..."

OPERATION_STRING_MSG = "[+] Now encrypting and encoding string payload into cover image..."
OPERATION_IMAGE_MSG = "[+] Now encrypting and encoding image payload into cover image..."
OPERATION_FILE_MSG = "[+] Now encrypting and encoding file payload into cover image..."
