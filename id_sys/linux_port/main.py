import os
from framework.common import *
import sys
from from_neo.config import *
from id_sys.sys_public import SYS_PATH
from framework.licensee import *
import logging
from shuka_lib.utils import get_os
from shuka_lib.mocks import not_implemented_log
def sys_get_path(type):
    """
    :return: None if not found
    """
    path = ''
    if type=='PATH_BASE':
        if os.path.exists(BUILD_DATADIR):
            return BUILD_DATADIR
        logging.warning('base path '+BUILD_DATADIR+' does not exist')
        #id: try next to the executable..
        exe_path = sys_get_path('PATH_EXE')
        if exe_path:
            path = os.path.join(exe_path, BASE_GAMEDIR)
            if os.path.exists(path):
                logging.warning('using path of executable: '+exe_path)
                return path
        #id: allback to vanilla doom3 install
        if get_os()=='linux':
            os_path = LINUX_DEFAULT_PATH
        else:
            not_implemented_log('default path for win')
        logging.warning('using hardcoded path:'+os_path)
        return os_path
    else:
       not_implemented_log('not implemented paths')



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
