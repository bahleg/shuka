"""
original /sys/platform.h
"""
MAX_STRING_CHARS = 1024  # id: max length of a string

# id: maximum world size
MAX_WORLD_COORD = 128 * 1024
MIN_WORLD_COORD = -128 * 1024
MAX_WORLD_SIZE = MAX_WORLD_COORD - MIN_WORLD_COORD


def bit(num):
    return 2**num