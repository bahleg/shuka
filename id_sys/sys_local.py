from functools import partial

from framework.key_input import *
from threads import *
from cpu import *
from framework.cvar_system import IdCVar, CVAR_FLAGS
from framework.cmd_system import IdCmdSystem

_SYS_LANGUAGE_NAMES = [
    "english", "spanish", "italian", "german", "french", "russian",
    "polish", "korean", "japanese", "chinese", None]

IdCVar("sys_lang", "english", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_ARCHIVE'], "",
       value_strings=_SYS_LANGUAGE_NAMES,
       value_completion=partial(IdCmdSystem.arg_completion_string, args=_SYS_LANGUAGE_NAMES))


class IdSysLocal(IdSys):
    def debug_print(self, string):
        logging.debug(string)

    def get_milliseconds(self):
        return sys_milliseconds()

    def get_processor_id(self):
        return sys_get_processor_id()

    def generate_mouse_button_event(self, button, down):
        event = SysEvent()
        event.event_type = 'SE_KEY'
        event.event_value = KEY_NUMS['K_MOUSE1'] + button - 1
        event.event_value2 = down
        return event

    def generate_mouse_move_event(self, delta_x, delta_y):
        event = SysEvent()
        event.event_type = 'SE_MOUSE'
        event.event_value = delta_x
        event.event_value2 = delta_y
        return event
