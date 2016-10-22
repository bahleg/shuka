from shuka_lib.mocks import not_implemented_log
KEY_NUMS = {
    'K_TAB': 9,
    'K_ENTER': 13,
    'K_ESCAPE': 27,
    'K_SPACE': 32,

    'K_BACKSPACE': 127,

    'K_COMMAND': 128,
    'K_CAPSLOCK': 129,
    'K_SCROLL': 130,
    'K_POWER': 131,
    'K_PAUSE': 132,

    'K_UPARROW': 133,
    'K_DOWNARROW': 134,
    'K_LEFTARROW': 135,
    'K_RIGHTARROW': 136,

    # id: The 3 windows keys
    'K_LWIN': 137,
    'K_RWIN': 138,
    'K_MENU': 139,

    'K_ALT': 140,
    'K_CTRL': 141,
    'K_SHIFT': 142,
    'K_INS': 143,
    'K_DEL': 144,
    'K_PGDN': 145,
    'K_PGUP': 146,
    'K_HOME': 147,
    'K_END': 148,

    'K_F1': 149,
    'K_F2': 150,
    'K_F3': 151,
    'K_F4': 152,
    'K_F5': 153,
    'K_F6': 154,
    'K_F7': 155,
    'K_F8': 156,
    'K_F9': 157,
    'K_F10': 158,
    'K_F11': 159,
    'K_F12': 160,
    'K_INVERTED_EXCLAMATION': 161,  # id: upside down !
    'K_F13': 162,
    'K_F14': 163,
    'K_F15': 164,

    'K_KP_HOME': 165,
    'K_KP_UPARROW': 166,
    'K_KP_PGUP': 167,
    'K_KP_LEFTARROW': 168,
    'K_KP_5': 169,
    'K_KP_RIGHTARROW': 170,
    'K_KP_END': 171,
    'K_KP_DOWNARROW': 172,
    'K_KP_PGDN': 173,
    'K_KP_ENTER': 174,
    'K_KP_INS': 175,
    'K_KP_DEL': 176,
    'K_KP_SLASH': 176,
    'K_SUPERSCRIPT_TWO': 178,  # id :superscript 2
    'K_KP_MINUS': 179,
    'K_ACUTE_ACCENT': 180,  # id: accute accent
    'K_KP_PLUS': 181,
    'K_KP_NUMLOCK': 182,
    'K_KP_STAR': 183,
    'K_KP_EQUALS': 184,

    'K_MASCULINE_ORDINATOR': 186,
    # id: 'K_MOUSE enums must be contiguous (no char codes in the middle)
    'K_MOUSE1': 187,
    'K_MOUSE2': 188,
    'K_MOUSE3': 189,
    'K_MOUSE4': 190,
    'K_MOUSE5': 191,
    'K_MOUSE6': 192,
    'K_MOUSE7': 193,
    'K_MOUSE8': 194,

    'K_MWHEELDOWN': 195,
    'K_MWHEELUP': 196,

    'K_JOY1': 197,
    'K_JOY2': 198,
    'K_JOY3': 199,
    'K_JOY4': 199,
    'K_JOY5': 200,
    'K_JOY6': 201,
    'K_JOY7': 202,
    'K_JOY8': 203,
    'K_JOY9': 204,
    'K_JOY10': 205,
    'K_JOY11': 206,
    'K_JOY12': 207,
    'K_JOY13': 208,
    'K_JOY14': 209,
    'K_JOY15': 210,
    'K_JOY16': 211,
    'K_JOY17': 212,
    'K_JOY18': 213,
    'K_JOY19': 214,
    'K_JOY20': 215,
    'K_JOY21': 216,
    'K_JOY22': 217,
    'K_JOY23': 218,
    'K_JOY24': 219,
    'K_JOY25': 220,
    'K_JOY26': 221,
    'K_JOY27': 222,
    'K_GRAVE_A': 224,  # id: lowercase a with grave accent
    'K_JOY28': 225,
    'K_JOY29': 226,
    'K_JOY30': 227,
    'K_JOY31': 228,
    'K_JOY32': 229,

    'K_AUX1': 230,
    'K_CEDILLA_C': 231,  # id : lowercase c with Cedilla
    'K_GRAVE_E': 232,  # id: lowercase e with grave accent
    'K_AUX2': 233,
    'K_AUX3': 234,
    'K_AUX4': 235,
    'K_GRAVE_I': 236,  # id: lowercase i with grave accent
    'K_AUX5': 237,
    'K_AUX6': 238,
    'K_AUX7': 239,
    'K_AUX8': 240,
    'K_TILDE_N': 241,  # id: lowercase n with tilde
    'K_GRAVE_O': 242,  # id lowercase o with grave accent
    'K_AUX9': 243,
    'K_AUX10': 244,
    'K_AUX11': 245,
    'K_AUX12': 246,
    'K_AUX13': 247,
    'K_AUX14': 248,
    'K_GRAVE_U': 249,  # id: lowercase u with grave accent
    'K_AUX15': 250,
    'K_AUX16': 251,

    'K_PRINT_SCR': 252,  # id: SysRq / PrintScr
    'K_RIGHT_ALT': 253,  # id:  used by some languages as "Alt-Gr"
    'K_LAST_KEY ': 254  # id: this better be < 256!
}


class KeyInput:
    def init(self):
        not_implemented_log('key input init')

    _instance = None


    @staticmethod
    def get_instance():
        return KeyInput._instance

    def __init__(self):
        KeyInput._instance = self
