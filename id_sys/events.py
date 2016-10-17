import ctypes
import logging
from functools import partial

from sdl2 import *

from framework.common import *
from framework.key_input import *
from framework.cvar_system import IdCVar, CVAR_FLAGS
from sys_public import *

_KBD_NAMES = ["english", "french", "german", "italian", "spanish", "turkish", "norwegian", "brazilian", None]
_in_kbd = IdCVar("in_kbd", "english",
                 CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_ARCHIVE'] | CVAR_FLAGS['CVAR_NOCHEAT'],
                 "keyboard layout",
                 value_strings=_KBD_NAMES,
                 value_completion=partial(IdCmdSystem.arg_completion_string, args=_KBD_NAMES))


class _KbdPoll:
    def __init__(self, key=0, state=False):
        self.key = key
        self.state = state


class _MousePoll:
    def __init__(self, a='', v=0):
        self.a = a
        self.v = v


_kbd_polls = []
_mouse_polls = []


def map_key(key):
    if key == SDLK_BACKSPACE:
        return KEY_NUMS['K_BACKSPACE']
    if key == SDLK_PAUSE:
        return KEY_NUMS['K_PAUSE']
    if key <= SDLK_z:
        return KEY_NUMS['key&0xff']
    if key == SDLK_APPLICATION:
        return KEY_NUMS['K_COMMAND']
    if key == SDLK_CAPSLOCK:
        return KEY_NUMS['K_CAPSLOCK']
    if key == SDLK_SCROLLLOCK:
        return KEY_NUMS['K_SCROLL']
    if key == SDLK_POWER:
        return KEY_NUMS['K_POWER']

    if key == SDLK_UP:
        return KEY_NUMS['K_UPARROW']
    if key == SDLK_DOWN:
        return KEY_NUMS['K_DOWNARROW']
    if key == SDLK_LEFT:
        return KEY_NUMS['K_LEFTARROW']
    if key == SDLK_RIGHT:
        return KEY_NUMS['K_RIGHTARROW']

    if key == SDLK_LGUI:
        return KEY_NUMS['K_LWIN']
    if key == SDLK_RGUI:
        return KEY_NUMS['K_RWIN']
    if key == SDLK_MENU:
        return KEY_NUMS['K_MENU']

    if key == SDLK_LALT or key == SDLK_RALT:
        return KEY_NUMS['K_ALT']
    if key == SDLK_RCTRL or key == SDLK_LCTRL:
        return KEY_NUMS['K_CTRL']
    if key == SDLK_RSHIFT or key == SDLK_LSHIFT:
        return KEY_NUMS['K_SHIFT']
    if key == SDLK_INSERT:
        return KEY_NUMS['K_INS']
    if key == SDLK_DELETE:
        return KEY_NUMS['K_DEL']
    if key == SDLK_PAGEDOWN:
        return KEY_NUMS['K_PGDN']
    if key == SDLK_PAGEUP:
        return KEY_NUMS['K_PGUP']
    if key == SDLK_HOME:
        return KEY_NUMS['K_HOME']
    if key == SDLK_END:
        return KEY_NUMS['K_END']

    if key == SDLK_F1:
        return KEY_NUMS['K_F1']
    if key == SDLK_F2:
        return KEY_NUMS['K_F2']
    if key == SDLK_F3:
        return KEY_NUMS['K_F3']
    if key == SDLK_F4:
        return KEY_NUMS['K_F4']
    if key == SDLK_F5:
        return KEY_NUMS['K_F5']
    if key == SDLK_F6:
        return KEY_NUMS['K_F6']
    if key == SDLK_F7:
        return KEY_NUMS['K_F7']
    if key == SDLK_F8:
        return KEY_NUMS['K_F8']
    if key == SDLK_F9:
        return KEY_NUMS['K_F9']
    if key == SDLK_F10:
        return KEY_NUMS['K_F10']
    if key == SDLK_F11:
        return KEY_NUMS['K_F11']
    if key == SDLK_F12:
        return KEY_NUMS['K_F12']

    if key == SDLK_F13:
        return KEY_NUMS['K_F13']
    if key == SDLK_F14:
        return KEY_NUMS['K_F14']
    if key == SDLK_F15:
        return KEY_NUMS['K_F15']

    if key == SDLK_KP_7:
        return KEY_NUMS['K_KP_HOME']
    if key == SDLK_KP_8:
        return KEY_NUMS['K_KP_UPARROW']
    if key == SDLK_KP_9:
        return KEY_NUMS['K_KP_PGUP']
    if key == SDLK_KP_4:
        return KEY_NUMS['K_KP_LEFTARROW']
    if key == SDLK_KP_5:
        return KEY_NUMS['K_KP_5']
    if key == SDLK_KP_6:
        return KEY_NUMS['K_KP_RIGHTARROW']
    if key == SDLK_KP_1:
        return KEY_NUMS['K_KP_END']
    if key == SDLK_KP_2:
        return KEY_NUMS['K_KP_DOWNARROW']
    if key == SDLK_KP_3:
        return KEY_NUMS['K_KP_PGDN']
    if key == SDLK_KP_ENTER:
        return KEY_NUMS['K_KP_ENTER']
    if key == SDLK_KP_0:
        return KEY_NUMS['K_KP_INS']
    if key == SDLK_KP_PERIOD:
        return KEY_NUMS['K_KP_DEL']
    if key == SDLK_KP_DIVIDE:
        return KEY_NUMS['K_KP_SLASH']

    if key == SDLK_KP_MINUS:
        return KEY_NUMS['K_KP_MINUS']

    if key == SDLK_KP_PLUS:
        return KEY_NUMS['K_KP_PLUS']
    if key == SDLK_NUMLOCKCLEAR:
        return KEY_NUMS['K_KP_NUMLOCK']
    if key == SDLK_KP_MULTIPLY:
        return KEY_NUMS['K_KP_STAR']
    if key == SDLK_KP_EQUALS:
        return KEY_NUMS['K_KP_EQUALS']

    if key == SDLK_PRINTSCREEN:
        return KEY_NUMS['K_PRINT_SCR']
    if key == SDLK_MODE:
        return KEY_NUMS['K_RIGHT_ALT']

    return 0


def push_console_event(s):
    b = s[:]
    event = SDL_Event()

    event.type = SDL_USEREVENT
    event.user.code = SYS_EVENT_TYPES['SE_CONSOLE']
    event.user.data1 = len(s)
    event.user.data2 = b
    SDL_PushEvent(event)


def sys_init_input():
    global _in_kbd
    _in_kbd.set_modified()


def sys_shutdown_input():
    global _kbd_polls, _mouse_polls
    _kbd_polls.clear()
    _mouse_polls.clear()


def sys_get_console_key(shifted):
    keys = ['`', '~']
    global _in_kbd
    if _in_kbd.modified():
        lang = in_kbd.string
        if lang and len(lang) != 0:
            if lang == 'french':
                keys[0] = '<'
                keys[1] = '>'
            elif lang == 'german':
                keys[0] = '^'
                keys[1] = 127
            elif lang == 'italian':
                keys[0] = '\\'
                keys[1] = '|'
            elif lang == 'spanish':
                keys[0] = 186
                keys[1] = 187
            elif lang == 'turkish':
                keys[0] = '"'
                keys[1] = 233
            elif lang == 'norwegian':
                keys[0] = 124
                keys[1] = 167
            elif lang == 'brazilian':
                keys[0] = "'"
                keys[1] = '"'
            _in_kbd.clear_modified()
    if shifted:
        return keys[1]
    return keys[0]


def sys_map_char_for_key(key):
    return key & 0xff


def sys_grab_mouse_cursor(grab_it):
    raise NotImplementedError()


"""
void Sys_GrabMouseCursor(bool grabIt) {
    int flags;

    if (grabIt)
        flags = GRAB_ENABLE | GRAB_HIDECURSOR | GRAB_SETSTATE;
    else
        flags = GRAB_SETSTATE;

    GLimp_GrabInput(flags);
}
"""


def sys_get_event():
    global _kdb_polls
    global _mouse_polls
    res_none = SysEvent()
    res_none.event_type = 'SE_NONE'
    s = [0]
    s_pos = 0
    ev = SDL_Event()
    while SDL_PollEvent(ctypes.byref(ev)) != 0:
        if ev.type == SDL_WINDOWEVENT:
            if ev.window.event == SDL_WINDOWEVENT_FOCUS_GAINED:
                # id: unset modifier, in case alt-tab was used to leave window and ALT is still set
                # id: as that can cause fullscreen-toggling when pressing enter...
                currentmod = SDL_GetModState()
                newmod = KEY_NUMS['KMOD_NONE']
                if (currentmod & KMOD_CAPS):  # id: preserve capslock
                    newmod |= KMOD_CAPS
                SDL_SetModState(newmod)
            if ev.window.event == SDL_WINDOWEVENT_FOCUS_LOST:
                """
                GLimp_GrabInput(0);
                    break;
                """
                raise NotImplementedError()

            continue
        if ev.type == SDL_KEYDOWN:
            flags = 0
            if ev.key.keysym.sym == SDLK_RETURN and (ev.key.keysym.mod & KEY_NUMS['KMOD_ALT']) > 0:
                cvarSystem.set_cvar_bool("r_fullscreen", not renderSystem->IsFullScreen())
                push_console_event("vid_restart")
                return res_none
        if ev.type == SDL_KEYUP:
            key = map_key(ev.key.keysym.sym)
            if not key:
                # id: check if its an unmapped console key
                c = sys_get_console_key(False)
                if (ev.key.keysym.unicode == c):
                    key = c
                else:
                    c = sys_get_console_key(True)
                    if (ev.key.keysym.unicode == c):
                        key = c
                    else:
                        logging.error('unmapped key:' + str(ev.key.keysym.sym))
                        continue
            res = SysEvent()
            res.event_type = 'SE_KEY'
            res.event_value = key
            res.event_value2 = 1
            if ev.key.state != SDL_PRESSED:
                res.event_value2 = 0
            _kbd_polls.append(_KbdPoll(key, ev.key.state == SDL_PRESSED))
            return res
        if ev.type == SDL_TEXTINPUT:
            if ev.text.text[0]:
                res = SysEvent()
                res.event_type = 'SE_CHAR'
                res.event_value = ev.text.text[0]
                if ev.text.text[1] != '\0':
                    s = ev.text.text[:]
                    raise NotImplementedError()
        if ev.type == SDL_TEXTEDITING:
            # id:  on windows we get this event whenever the window gains focus.. just ignore it.
            continue
        if ev.type == SDL_MOUSEMOTION:
            res = SysEvent()
            res.event_type = 'SE_MOUSE'
            res.event_value = ev.motion.xrel
            res.event_value2 = ev.motion.yrel
            _mouse_polls.append(_MousePoll('M_DELTAX', ev.motion.xrel))
            _mouse_polls.append(_MousePoll('M_DELTAY', ev.motion.yrel))
            return res
        if ev.type == SDL_MOUSEWHEEL:
            res = SysEvent()
            res.event_type = 'SE_KEY'
            if ev.wheel.y > 0:
                res.event_value = KEY_NUMS['K_MWHEELUP']
                _mouse_polls.append(_MousePoll('M_DELTAZ', 1))
            else:
                res.event_value = KEY_NUMS['K_MWHEELDOWN']
                _mouse_polls.append(_MousePoll('M_DELTAZ', -1))
            res.event_value2 = 1
            return res
        if ev.type in [SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP]:
            res = SysEvent()
            res.event_type = 'SE_KEY'
            pressed = ev.button.state == SDL_PRESSED
            if pressed:
                pressed = 1
            else:
                pressed = 0
            if ev.button.button == SDL_BUTTON_LEFT:
                res.event_value = KEY_NUMS['K_MOUSE1']
                _mouse_polls.append(_MousePoll('M_ACTION1', pressed))
            if ev.button.button == SDL_BUTTON_MIDDLE:
                res.event_value = KEY_NUMS['K_MOUSE3']
                _mouse_polls.append(_MousePoll('M_ACTION1', pressed))
            if ev.button.button == SDL_BUTTON_RIGHT:
                res.event_value = KEY_NUMS['K_MOUSE2']
                _mouse_polls.append(_MousePoll('M_ACTION1', pressed))
            return res

        # TODO: forgot one section
        if ev.type == SDL_QUIT:
            push_console_event("quit")
            return res_none
        if ev.type == SDL_USEREVENT:
            if ev.user.code == 'SE_CONSOLE':
                res = SysEvent()
                res.event_type = 'SE_CONSOLE'
                res.event_ptr_len = len(ev.user.data1)
                res.event_pointer = ev.user.data2
                return res
            else:
                logging.warning("unknown user event {0}".format(str(ev.user.code)))
                continue
        else:
            # debug
            # id: ok, I don't /really/ care about unknown SDL events. only uncomment this for debugging.
            # id: common->Warning("unknown SDL event 0x%x", ev.type);
            continue  # id: handle next event
    return res_none


def sys_clear_events():
    ev = SDL_Event()

    while SDL_PollEvent(ctypes.byref(ev)) != 0:
        pass
    global _kbd_polls, _mouse_polls
    _kbd_polls.clear()
    _mouse_polls.clear()


def sys_generate_events():
    s = sys_console_input()
    if s:
        push_console_event(s)
    SDL_PumpEvents()


def sys_poll_keyboard_input_events():
    # return kbd_polls.Num();???
    raise NotImplementedError()


# NB: semantic is changed!
def sys_return_keyboard_input_event(n):
    global _kbd_polls
    if n >= len(_kbd_polls):
        return 0
    key = _kbd_polls[n].key
    state = _kbd_polls[n].state
    return key, state


def sys_end_keyboard_input_events():
    # kbd_polls.SetNum(0, false); ???
    raise NotImplementedError()


def sys_poll_mouse_input_events():
    # return mouse_polls.Num();???
    raise NotImplementedError()


# NB: semantic is changed!
def sys_return_mouse_input_event(n):
    global _mouse_polls
    if n >= len(_mouse_polls):
        return 0
    action = _mouse_polls[n].action
    value = _kbd_polls[n].value
    return action, value


def sys_end_mouse_input_events():
    # mouse_polls.SetNum(0, false); ???
    raise NotImplementedError()
