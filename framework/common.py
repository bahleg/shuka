from id_sys.sys_platform import bit

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
    raise NotImplementedError()


class IdCommon:
    def __init__(self, args):
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


class IdCommonLocal(IdCommon):
    pass 