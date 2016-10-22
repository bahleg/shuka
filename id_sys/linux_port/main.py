import os
from framework.common import *

def main(args):
    """
    id:
    some ladspa-plugins (that may be indirectly loaded by doom3 if they're
    used by alsa) call setlocale(LC_ALL, ""); This sets LC_ALL to $LANG or
    $LC_ALL which usually is not "C" and will fuck up scanf, strtod
    etc when using a locale that uses ',' as a float radix.
    so set $LC_ALL to "C".
    """
    os.environ["LC_ALL"] = 'C'
    common = IdCommonLocal()
    common.init(args[1:])

    while (True):
        common.frame()
    return 0


if __name__ == '__main__':
    import sys

    main(sys.argv)
