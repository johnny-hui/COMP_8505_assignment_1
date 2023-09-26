PROGRAM_CONFIGURATION_BANNER = "====================== // PROGRAM CONFIGURATIONS // ======================"
PROGRAM_CONFIG_ENDING_BANNER = "=========================================================================="

OS_ERROR_MSG = "[+] ERROR: Cannot open file at specified directory!"
MAX_NUM_BITS_EXCEEDED_ERROR = "[+] ERROR: Number of bits per pixel chosen to be replaced exceeds 24!"
NUM_BITS_ERROR_NEGATIVE = "[+] ERROR: Number of LSBs per pixel chosen to be replaced cannot be a negative integer!"
NUM_BITS_TO_REPLACE_EXCEEDED_ERROR = "[+] ERROR: Number of LSBs per pixel chosen to be replaced cannot exceed 24 bits!"
PAYLOAD_SIZE_NEGATIVE_ERROR = "[+] ERROR: Payload size cannot be a negative integer!"
PAYLOAD_SIZE_EXCEEDED_ERROR = "[+] ERROR: Payload size exceeds maximum possible threshold for current image!"
MAX_BIT_DEPTH = 24
LSB_MINIMUM = 3
ZERO = 0
PNG_FORMAT = "PNG"
PNG_FORMAT_RGB = "RGB"
NOT_PNG_ERROR = "[+] ERROR: This program only supports images with PNG format!"
NOT_PNG_24_BIT_ERROR = "[+] ERROR: This program only supports 24 bit (RGB) PNG images!"
NO_ARG_ERROR = "[+] NO_ARG_ERROR: No arguments were passed in!"
MAX_LSB_LIMIT_PER_PIXEL = 24
BITS_PER_PIXEL_UPPER_BOUND_ERROR = "[+] ERROR: The number of LSBs per pixel (-l) provided cannot exceed 24 bits!"
BITS_PER_PIXEL_LOWER_BOUND_ERROR = "[+] ERROR: The number of LSBs per pixel (-l) provided cannot be negative or zero!"
L_OPTION_INVALID_ARGUMENT_MSG = "[+] ERROR: Invalid Argument for -l option!"
C_OPTION_INVALID_ARGUMENT_MSG = "[+] ERROR: No argument was provided for -c (Cover Image) option!"
C_OPTION_INVALID_PATH_ERROR = "[+] ERROR: File does not exist or invalid path!"
L_OPTION_DEFAULT_SETTING_MSG = "[+] WARNING: Now setting -l option to a default value of 3 bits/pixel...\n"
L_OPTION_NO_ARG_WARNING_MSG = "[+] The -l option (number of bits/pixel) was not provided!"

CONFIG_COVER_IMG = "[+] Cover Image: {}"
CONFIG_BITS_PER_PIXEL = "[+] Number of Bits Per Pixel: {}"
