# noinspection PyUnresolvedReferences
import ctypes
# noinspection PyUnresolvedReferences
from build_version import *
# noinspection PyUnresolvedReferences
from id_sys.threads import *
# noinspection PyUnresolvedReferences
from id_sys.posix_port.posix_main import *
# noinspection PyUnresolvedReferences
from usercmd_gen import *
# noinspection PyUnresolvedReferences
from cmd_system import *
# noinspection PyUnresolvedReferences
from cvar_system import *
# noinspection PyUnresolvedReferences
from key_input import *
# noinspection PyUnresolvedReferences
from id_lib.lib import *
# noinspection PyUnresolvedReferences
from id_sys.sys_public import *
# noinspection PyUnresolvedReferences
from id_sys.events import *

from renderer.render_system import IdRenderSystemLocal

from file_system import IdFileSystemLocal
TOOL_FLAG = {
    'EDITOR_NONE': 0,
    'EDITOR_RADIANT': bit(1),
    'EDITOR_GUI': bit(2),
    'EDITOR_DEBUGGER': bit(3),
    'EDITOR_SCRIPT': bit(4),
    'EDITOR_LIGHT': bit(5),
    'EDITOR_SOUND': bit(6),
    'EDITOR_DECL': bit(7),
    'EDITOR_AF': bit(8),
    'EDITOR_PARTICLE': bit(9),
    'EDITOR_PDA': bit(10),
    'EDITOR_AAS': bit(11),
    'EDITOR_MATERIAL': bit(12)
}

_com_tic_number = 0
_com_frame_time = 0
_com_frame_number = 0
_last_tic_msec = 0


def async_timer_func(interval, ptr):
    IdCommon.get_instance().async()
    sys_trigger_event(TRIGGER_EVENTS['TRIGGER_EVENT_ONE'])
    # id: calculate the next interval to get as close to 60fps as possible
    now = SDL_GetTicks()
    tick = _com_tic_number * USERCMD_MSEC

    if (now >= tick):
        return 1

    return tick - now


class MemInfo:
    def __init__(self):
        self.file_base = ''
        self.total = 0
        self.asset_totals = 0

        # id: memory manager totals
        self.memory_manager_total = 0
        # id: subsystem totals
        self.subsystem_total = 0
        self.render_subsystem_total = 0

        # id: asset totals
        self.image_assets_total = 0
        self.model_assets_total = 0
        self.sound_assets_total = 0


class IdLangDict:
    def __init__(self):
        raise NotImplementedError()


class IdCommon:
    def init(self, args):
        """
        id: Initialize everything.
        """
        raise NotImplementedError()

    def shutdown(self):
        """
        id: Shuts down everything.
        """
        raise NotImplementedError()

    def quit(self):
        """
        id: Shuts down everything.
        """
        raise NotImplementedError()

    def frame(self):
        """
        id: Called repeatedly as the foreground thread for rendering and game logic.
        """
        raise NotImplementedError()

    def gui_frame(self, exec_cmd, network):
        """
        #id:  Called repeatedly by blocking function calls with GUI interactivity.
        """
        raise NotImplementedError()

    def Async(self):
        """
        id:  Called 60 times a second from a background thread for sound mixing,
        id:  and input generation. Not called until idCommon::Init() has completed.
        """
        raise NotImplementedError()

    def startup_variable(self, match, once):
        """
        #id:  Checks for and removes command line "+set var arg" constructs.
        #id:  If match is NULL, all set commands will be executed, otherwise
        #id:  only a set with the exact name.  Only used during startup.
        #id:  set once to clear the cvar from +set for early init code
        """
        raise NotImplementedError()

    def init_tool(self, tool_flag, id_dict):
        raise NotImplementedError()

    def activate_tool(self, active):
        # id:  Activates or deactivates a tool.
        raise NotImplementedError()

    def write_config_file(self, filename):
        # id:  Writes the user's configuration to a file
        raise NotImplementedError()

    def write_flagged_cvars_to_file(self, filename, flags, set_cmd):
        ##id:  Writes cvars with the given flags to a file.
        raise NotImplementedError()

    def begin_redirect(self, buffer, flush):
        # id:  Begins redirection of console output to the given buffer.
        raise NotImplementedError()

    def end_redirect(self):
        # id:  Stops redirection of console output.
        raise NotImplementedError()

    def set_refresh_on_print(self, bool_set):
        # id:  Update the screen with every message printed.
        raise NotImplementedError()

    def get_language_dict(self):
        # id:  Returns a pointer to the dictionary with language specific strings.
        raise NotImplementedError()

    def keys_from_binding(self, bind):
        # id:  Returns key bound to the command
        raise NotImplementedError()

    def binding_from_key(self, key):
        # id:  Returns the binding bound to the key
        raise NotImplementedError()

    def button_state(self, key):
        # id:  Directly sample a button.
        raise NotImplementedError()

    def key_state(self):
        # id:  Directly sample a keystate.
        raise NotImplementedError()

    _instance = None

    @staticmethod
    def get_instance():
        return IdCommon._instance

    def __init__(self):
        IdCommon._instance = self


class IdCommonLocal(IdCommon):
    def __init__(self):
        IdCommon.__init__(self)
        self.com_num_console_lines = 0
        self.com_console_lines = []

    def init_logger(self):
        logger = logging.getLogger()
        logger.setLevel(10)
        name = 'game.log'
        try:
            os.remove(name)
        except:
            pass
        fh = logging.FileHandler(name)
        fh.setLevel(logging.INFO)
        """
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        """
        formatter = logging.Formatter('%(asctime)s : %(levelname)s ::: %(message)s')
        formatter_console = logging.Formatter('%(levelname)s: %(message)s')
        fh.setFormatter(formatter)

        # ch.setFormatter(formatter_console)
        # logger.addHandler(ch)

        logger.addHandler(fh)
        logger.log(logging.INFO, 'Logger created')

    def init(self, args):

        self.init_logger()
        not_implemented_log('switch to dedicated')
        if (SDL_Init(SDL_INIT_TIMER | SDL_INIT_VIDEO)):
            sys_error("Error while initializing SDL: {0}".format(SDL_GetError()))

        sys_init_threads()
        try:
            not_implemented_log('id lib')
            not_implemented_log('warning routines')
            not_implemented_log('parse_command_line')

            cmd_system_instance = IdCmdSystemLocal()
            cmd_system_instance.init()

            cvar_system_instance = IdCvarSystemLocal()
            cvar_system_instance.init()
            not_implemented_log('IdCvar.register_static_variables()')

            sdl_version = SDL_version()
            SDL_GetVersion(ctypes.byref(sdl_version))
            logging.info(get_version_string())
            logging.info('using SDL version {0}.{1}.{2}'.format(sdl_version.major, sdl_version.minor,
                                                                sdl_version.patch))
            key_input_instance = KeyInput().get_instance()
            key_input_instance.init()
            not_implemented_log('console->init')
            sys_init()
            not_implemented_log('Sys_InitNetworking')
            # id: override cvars from command line
            not_implemented_log('StartupVariable')
            # id: set fpu double extended precision
            not_implemented_log('FPU_set')

            # id: initialize processor specific SIMD implementation
            not_implemented_log('SIMD')
            not_implemented_log('InitCommands')
            # id: game specific initialization
            self.init_game()
            not_implemented_log('Console routines')
            self.com_fullyInitialized = True

        except Exception, e:
            sys_error('Error during initialization:' + repr(e))

        async_timer_func_c = SDL_TimerCallback(async_timer_func)
        async_timer = SDL_AddTimer(USERCMD_MSEC, async_timer_func_c, None)
        if not async_timer:
            sys_error("Error while starting the async timer: {0}".format(SDL_GetError()))

    def frame(self):
        try:
            global _com_frame_time, _com_frame_number
            # id: pump all the events
            sys_generate_events()
            not_implemented_log('write config')
            not_implemented_log('change simd')
            not_implemented_log('run_event_loop')

            _com_frame_time = _com_tic_number * USERCMD_MSEC
            not_implemented_log('idAsyncNet:Run, session, etc')

            _com_frame_number += 1
            not_implemented_log('idLib.frameNumber = com_frameNumber')
            # idLib.frameNumber = com_frameNumber

        except IdException:
            return  # id:  an ERP_DROP was thrown

    def async(self):
        global _last_tic_msec
        msec = sys_milliseconds()
        if not _last_tic_msec:
            _last_tic_msec = msec - USERCMD_MSEC
        not_implemented_log('async com_preciseTic.GetBool()')
        if False:
            # id: just run a single tic, even if the exact msec isn't precise
            self.single_async_tic()
            return
        tic_msec = USERCMD_MSEC

        # id: the number of msec per tic can be varies with the timescale cvar
        not_implemented_log('timescale')
        timescale = 1.0
        if (timescale != 1.0):
            tic_msec /= timescale
            if tic_msec < 1:
                tic_msec = 1

        # id:  don't skip too many
        if (timescale == 1.0):
            if (_last_tic_msec + 10 * USERCMD_MSEC < msec):
                _last_tic_msec = msec - 10 * USERCMD_MSEC

        while _last_tic_msec + tic_msec <= msec:
            self.single_async_tic()
            _last_tic_msec += tic_msec

    def single_async_tic(self):
        """
        id:
        The system will asyncronously call this function 60 times a second to
        handle the time-critical functions that we don't want limited to
        the frame rate:
        sound mixing
        user input generation (conditioned by com_asyncInput)
        packet server operation
        packet client operation
        We are not using thread safe libraries, so any functionality put here must
        be VERY VERY careful about what it calls.
        """

        """
        id: main thread code can prevent this from happening while modifying
        critical data structures
        """
        global _com_tic_number
        sys_enter_critical_section(0)
        not_implemented_log('async tic routines')
        # id : we update com_ticNumber after all the background tasks  have completed their work for this tic
        _com_tic_number += 1
        not_implemented_log('async tic: stat')
        sys_leave_critical_section(0)

    def init_game(self):
        # id: initialize the file system
        fs =IdFileSystemLocal()
        fs.init()
        not_implemented_log('many things in init game')
        # id: initialize the renderSystem data structures, but don't start OpenGL yet
        render = IdRenderSystemLocal()
        render.init()

    def startup_variable(self, match, once):
        i = 0
        while (i < self.com_num_console_lines):
            if self.com_console_lines[i].argv(0) == 'set':
                i += 1
                continue
            s = self.com_console_lines[i].argv(1)
            not_implemented_log('!idStr::Icmp( s, match )')
            if not match or False:
                not_implemented_log('cvarSystem->SetCVarString( s, com_consoleLines[ i ].Argv( 2 ) );')
                if once:
                    # id: kill the line
                    j = i + 1
                    while j < self.com_num_console_lines:
                        self.com_console_lines[j - 1] = self.com_console_lines[j]
                        j += 1
                    self.com_num_console_lines -= 1
                    continue
            i += 1
