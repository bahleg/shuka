#from mutex import mutex as mutex_obj
#from threading import Condition, Thread, current_thread
import os
import logging
import multiprocessing
from sdl2 import *

from sys_public import *
from framework.build_defines import MAX_THREADS

_mutex = []
_cond = []
_signaled = []
_waiting = []
_thread = []
_thread_count = 0


def sys_sleep(msec):
    SDL_Delay(msec)


def sys_milliseconds():
    return SDL_GetTicks()


def sys_init_threads():
    global _mutex, _cond, _signaled, _waiting, _thread_count
    # id: critical sections
    for i in xrange(MAX_CRITICAL_SECTIONS):
        _mutex.append(multiprocessing.Lock())
    # id: events
    for i in xrange(MAX_TRIGGER_EVENTS):
        _cond.append(multiprocessing.Condition())
        _signaled.append(False)
        _waiting.append(False)
        for i in xrange(MAX_THREADS):
            _thread.append(None)

    _thread_count = 0


def sys_enter_critical_section(index):
    global _mutex
    assert index >= 0 and index < MAX_CRITICAL_SECTIONS
    _mutex[index].lock()


def sys_leave_critical_section(index):
    global _mutex
    assert index >= 0 and index < MAX_CRITICAL_SECTIONS
    _mutex[index].unlock()


"""
id:
======================================================
wait and trigger events
we use a single lock to manipulate the conditions, CRITICAL_SECTION_SYS

the semantics match the win32 version. signals raised while no one is waiting stay raised until a wait happens
(which then does a simple pass-through)

NOTE: we use the same mutex for all the events. I don't think this would become much of a problem
cond_wait unlocks atomically with setting the wait condition, and locks it back before exiting the function
the potential for time wasting lock waits is very low
======================================================
"""


def sys_wait_for_event(index):
    assert index >= 0 and index < MAX_TRIGGER_EVENTS
    global _waiting, _signaled, _cond
    sys_enter_critical_section(CRITICAL_SECTIONS['CRITICAL_SECTION_SYS'])
    assert not _waiting[index]  # id: WaitForEvent from multiple threads? that wouldn't be good
    if _signaled[index]:
        # id: emulate windows behaviour: signal has been raised already. clear and keep going
        _signaled[index] = False
    else:
        _waiting[index] = True
        _cond[index].wait()
        _waiting[index] = False
    sys_leave_critical_section(index)


def sys_trigger_event(index):
    assert index >= 0 and index < MAX_TRIGGER_EVENTS
    global _waiting, _signaled, _cond
    sys_enter_critical_section(CRITICAL_SECTIONS['CRITICAL_SECTION_SYS'])
    if _waiting[index]:
        _cond[index].notify()
    else:
        _signaled[index] = True
    sys_leave_critical_section(index)


def sys_create_thread(function, params, info, name):
    global _thread_count, threads
    sys_enter_critical_section(CRITICAL_SECTIONS['CRITICAL_SECTION_ZERO'])

    t = multiprocessing.Process(target=function, args=params)
    t.start()#Thread(target=function, args=params)
    info.name = name
    info.thread_handle = t
    info.thread_id = t.ident
    if _thread_count < MAX_THREADS:
        _thread.append(info)
        _thread_count += 1
    else:
        logging.warning('MAX_THREADS reached')
    sys_leave_critical_section(CRITICAL_SECTIONS['CRITICAL_SECTION_ZERO'])


def sys_destroy_thread(info):
    assert info.thread_handle is not None
    global _thread_count, threads
    info.thread_handle.join()
    sys_enter_critical_section(CRITICAL_SECTIONS['CRITICAL_SECTION_ZERO'])
    _thread.remove(info)
    sys_leave_critical_section(CRITICAL_SECTIONS['CRITICAL_SECTION_ZERO'])


def sys_get_thread_name():
    """
    id:
    Sys_GetThreadName
    find the name of the calling thread
    """
    sys_enter_critical_section(CRITICAL_SECTIONS['CRITICAL_SECTION_ZERO'])
    id = os.getpid()# current_thread().ident
    for t in _thread:
        if t.thread_id == id:
            return t.name
    sys_leave_critical_section(CRITICAL_SECTIONS['CRITICAL_SECTION_ZERO'])
    return 'main'
