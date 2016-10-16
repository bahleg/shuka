CPU_IDS = {'CPUID_NONE': 0x00000,
           'CPUID_UNSUPPORTED': 0x00001,  # unsupported (386/486)
           'CPUID_GENERIC': 0x00002,  # unrecognized processor
           'CPUID_MMX': 0x00010,  # Multi Media Extensions
           'CPUID_3DNOW': 0x00020,  # 3DNow!
           'CPUID_SSE': 0x00040,  # Streaming SIMD Extensions
           'CPUID_SSE2': 0x00080,  # Streaming SIMD Extensions 2
           'CPUID_SSE3': 0x00100,  # Streaming SIMD Extentions 3 aka Prescott's New Instructions
           'CPUID_ALTIVEC': 0x00200,  # AltiVec
           }

JOYSTIC_AXES = {'AXIS_SIDE', 'AXIS_FORWARD', 'AXIS_UP', 'AXIS_ROLL', 'AXIS_YAW', 'AXIS_PITCH', 'MAX_JOYSTICK_AXIS'
                }

SYS_EVENT_TYPES = {'SE_NONE',  # evTime is still valid
                   'SE_KEY',  # evValue is a key code, evValue2 is the down flag
                   'SE_CHAR',  # evValue is an ascii char
                   'SE_MOUSE',  # evValue and evValue2 are reletive signed x / y moves
                   'SE_JOYSTICK_AXIS',  # evValue is an axis number and evValue2 is the current state (-127 to 127)
                   'SE_CONSOLE'  # evPtr is a char*, from typing something at a non-game console
                   }

SYS_M_EVENTS = {
    'M_ACTION1',
    'M_ACTION2',
    'M_ACTION3',
    'M_ACTION4',
    'M_ACTION5',
    'M_ACTION6',
    'M_ACTION7',
    'M_ACTION8',
    'M_DELTAX',
    'M_DELTAY',
    'M_DELTAZ'
}


class SysEvent:
    def __init__(self):
        self.event_type = None
        self.event_value = 0
        self.event_value2 = 0
        self.event_ptr_len = 0  # id: bytes of data pointed to by evPtr, for journaling
        self.event_pointer = None  # id: this must be manually freed if not NULL


SYS_PATH = {
    'PATH_BASE', 'PATH_CONFIG', 'PATH_SAVE', 'PATH_EXE'
}

"""
==============================================================

	Networking

==============================================================
"""

NET_ADDR_TYPE = {
    'NA_BAD',  # id: an address lookup failed
    'NA_LOOPBACK', 'NA_BROADCAST', 'NA_IP'
}

PORT_ANY = -1


class NetAddr:
    def __init__(self):
        self.net_addr_type = None
        self.ip = [127, 0, 0, 1]
        self.port = 666


"""
==============================================================

	Multi-threading

==============================================================
"""
MAX_CRITICAL_SECTIONS = 5

CRITICAL_SECTIONS = {
    'CRITICAL_SECTION_ZERO': 0,
    'CRITICAL_SECTION_ONE': 1,
    'CRITICAL_SECTION_TWO': 2,
    'CRITICAL_SECTION_THREE': 3,
    'CRITICAL_SECTION_SYS': 4
}

MAX_TRIGGER_EVENTS = 4

TRIGGER_EVENTS = {
    'TRIGGER_EVENT_ZERO': 0,
    'TRIGGER_EVENT_ONE': 1,
    'TRIGGER_EVENT_TWO': 2,
    'TRIGGER_EVENT_THREE': 3
}

"""
==============================================================

	idSys

==============================================================
"""


class IdSys:
    def debug_print(self, string):
        raise NotImplementedError()

    def get_milliseconds(self):
        raise NotImplementedError()

    def get_processor_id(self):
        raise NotImplementedError()

    def FPU_set_FTZ(self, enable):
        raise NotImplementedError()

    def FPU_set_DAZ(self, enable):
        raise NotImplementedError()

    def lock_memory(self, ptr, bytes):
        raise NotImplementedError()

    def unlock_memory(self, ptr, bytes):
        raise NotImplementedError()

    def dll_load(self, dll_name):
        raise NotImplementedError()

    def dll_get_proc_address(self, dll_handle, proc_name):
        raise NotImplementedError()

    def DLL_Unload(self, dll_handle):
        raise NotImplementedError()

    def dll_get_filename(self, basename, dll_name, max_length):
        raise NotImplementedError()

    def generate_mouse_button_event(self, button, down):
        raise NotImplementedError()

    def generate_mouse_move_event(self, delta_x, delta_y):
        raise NotImplementedError()

    def open_url(self, url, quit):
        raise NotImplementedError()

    def start_process(self, exe_path, quit):
        raise NotImplementedError()
