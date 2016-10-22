import logging
import traceback
import sys
from shuka_lib.mocks import *
from psutil import virtual_memory



def sys_error(error=''):
    logging.error(error)
    _, _, error_tb = sys.exc_info()
    error_tb = '\n'.join(traceback.format_tb(error_tb))
    logging.error(error_tb)
    print 'error:', error
    print error_tb
    sys.exit(1)

def sys_init():
    not_implemented_log('posix console init')
    not_implemented_log('com_pid')
    mem = virtual_memory()
    logging.debug('memory: {0} Mb'.format(str(mem.total/1024/1024)))