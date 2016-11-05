import sys
import logging

from framework.common import *
from from_neo.config import *
from framework.licensee import *
from shuka_lib.utils import get_os
from shuka_lib.mocks import not_implemented_log


def sys_get_path(type):
    """
    :return: None if not found
    """

    if type == 'PATH_BASE':
        if os.path.exists(BUILD_DATADIR):
            return BUILD_DATADIR
        logging.warning('base path ' + BUILD_DATADIR + ' does not exist')
        # id: try next to the executable..
        exe_path = sys_get_path('PATH_EXE')
        if exe_path:
            path = os.path.join(exe_path, BASE_GAMEDIR)
            if os.path.exists(path):
                logging.warning('using path of executable: ' + exe_path)
                return path
        # id: allback to vanilla doom3 install
        if get_os() == 'linux':
            os_path = LINUX_DEFAULT_PATH
        else:
            not_implemented_log('default path for win')
        if os.path.exists(os_path):
            logging.warning('using hardcoded path:' + os_path)
            return os_path
        return None

    elif type == 'PATH_CONFIG':
        if get_os() == 'linux':

            s = os.getenv('XDG_CONFIG_HOME', None)
            if s:
                return s + '/shuka'
            else:
                return os.getenv('HOME') + '/.config/shuka'
        else:
            not_implemented_log('default path for win')
    elif type == 'PATH_SAVE':
        if get_os() == 'linux':
            s = os.getenv('XDG_DATA_HOME', None)
            if s:
                return s + '/shuka'
            else:
                return os.getenv('HOME') + '/.local/share/shuka'
        else:
            not_implemented_log('default path for win')
    elif type == 'PATH_EXE':
        if get_os() == 'linux':
            buf = '/proc/' + str(os.getpid()) + '/exe'
            buf2 = os.readlink(buf)
            if buf2:
                return buf2
            return os.path.dirname(sys.argv[0])
        else:
            not_implemented_log('default path for win')
    return None

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
    main(sys.argv)
