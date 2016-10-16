from id_sys.sys_platform import bit

CVAR_FLAGS = {
    'CVAR_ALL': -1,  # id:  all flags
    'CVAR_BOOL': bit(0),  # id:  variable is a boolean
    'CVAR_INTEGER': bit(1),  # id:  variable is an integer
    'CVAR_FLOAT': bit(2),  # id:  variable is a float
    'CVAR_SYSTEM': bit(3),  # id:  system variable
    'CVAR_RENDERER': bit(4),  # id:  renderer variable
    'CVAR_SOUND': bit(5),  # id:  sound variable
    'CVAR_GUI': bit(6),  # id:  gui variable
    'CVAR_GAME': bit(7),  # id:  game variable
    'CVAR_TOOL': bit(8),  # id:  tool variable
    'CVAR_USERINFO': bit(9),  # id:  sent to servers, available to menu
    'CVAR_SERVERINFO': bit(10),  # id:  sent from servers, available to menu
    'CVAR_NETWORKSYNC': bit(11),  # id:  cvar is synced from the server to clients
    'CVAR_STATIC': bit(12),  # id:  statically declared, not user created
    'CVAR_CHEAT': bit(13),  # id:  variable is considered a cheat
    'CVAR_NOCHEAT': bit(14),  # id:  variable is not considered a cheat
    'CVAR_INIT': bit(15),  # id:  can only be set from the command-line
    'CVAR_RO0M': bit(16),  # id:  display only, cannot be set by user at all
    'CVAR_ARCHIVE': bit(17),  # id:  set to cause it to be saved to a config file
    'CVAR_MODIFIED': bit(18)  # id:  set when the variable is modified
}


class IdCVar:
    def __init__(self, name, value, flags, description,  value_strings= None,value_min=1, value_max=-1, value_completion=None):
        self.name = name
        self.value = value
        self.flags = flags
        self.description = description
        self.flags = flags | CVAR_FLAGS['CVAR_STATIC']
        self.value_min = value_min
        self.value_max = value_max
        self.value_strings = value_strings
        self.valueCompletion = value_completion
        self.int_value = 0
        self.float_value = 0.0
        self.integer_var = self
        raise NotImplementedError()
        """
        if ( staticVars != (idCVar *)0xFFFFFFFF ) {
		this->next = staticVars;
		staticVars = this;
	    } else {
		cvarSystem->Register( this );
	    }

	    None fields completion
	    """
