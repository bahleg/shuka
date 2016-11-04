"""
id:
DOOM FILESYSTEM
All of Doom's data access is through a hierarchical file system, but the contents of
the file system can be transparently merged from several sources.
A "relativePath" is a reference to game file data, which must include a terminating zero.
"..", "\\", and ":" are explicitly illegal in qpaths to prevent any references
outside the Doom directory system.
The "base path" is the path to the directory holding all the game directories and
usually the executable. It defaults to the current directory, but can be overridden
with "+set fs_basepath c:\doom" on the command line. The base path cannot be modified
at all after startup.
The "save path" is the path to the directory where game files will be saved. It defaults
to the base path, but can be overridden with a "+set fs_savepath c:\doom" on the
command line. Any files that are created during the game (demos, screenshots, etc.) will
be created reletive to the save path.
The "cd path" is the path to an alternate hierarchy that will be searched if a file
is not located in the base path. A user can do a partial install that copies some
data to a base path created on their hard drive and leave the rest on the cd. It defaults
to the current directory, but it can be overridden with "+set fs_cdpath g:\doom" on the
command line.
The "dev path" is the path to an alternate hierarchy where the editors and tools used
during development (Radiant, AF editor, dmap, runAAS) will write files to. It defaults to
the cd path, but can be overridden with a "+set fs_devpath c:\doom" on the command line.
If a user runs the game directly from a CD, the base path would be on the CD. This
should still function correctly, but all file writes will fail (harmlessly).
The "base game" is the directory under the paths where data comes from by default, and
can be either "base" or "demo".
The "current game" may be the same as the base game, or it may be the name of another
directory under the paths that should be searched for files before looking in the base
game. The game directory is set with "+set fs_game myaddon" on the command line. This is
the basis for addons.
No other directories outside of the base game and current game will ever be referenced by
filesystem functions.
To save disk space and speed up file loading, directory trees can be collapsed into zip
files. The files use a ".pk4" extension to prevent users from unzipping them accidentally,
but otherwise they are simply normal zip files. A game directory can have multiple zip
files of the form "pak0.pk4", "pak1.pk4", etc. Zip files are searched in decending order
from the highest number to the lowest, and will always take precedence over the filesystem.
This allows a pk4 distributed as a patch to override all existing data.
Because we will have updated executables freely available online, there is no point to
trying to restrict demo / oem versions of the game with code changes. Demo / oem versions
should be exactly the same executables as release versions, but with different data that
automatically restricts where game media can come from to prevent add-ons from working.
After the paths are initialized, Doom will look for the product.txt file. If not found
and verified, the game will run in restricted mode. In restricted mode, only files
contained in demo/pak0.pk4 will be available for loading, and only if the zip header is
verified to not have been modified. A single exception is made for DoomConfig.cfg. Files
can still be written out in restricted mode, so screenshots and demos are allowed.
Restricted mode can be tested by setting "+set fs_restrict 1" on the command line, even
if there is a valid product.txt under the basepath or cdpath.
If the "fs_copyfiles" cvar is set to 1, then every time a file is sourced from the cd
path, it will be copied over to the save path. This is a development aid to help build
test releases and to copy working sets of files.
If the "fs_copyfiles" cvar is set to 2, any file found in fs_cdpath that is newer than
it's fs_savepath version will be copied to fs_savepath (in addition to the fs_copyfiles 1
behaviour).
If the "fs_copyfiles" cvar is set to 3, files from both basepath and cdpath will be copied
over to the save path. This is useful when copying working sets of files mainly from base
path with an additional cd path (which can be a slower network drive for instance).
If the "fs_copyfiles" cvar is set to 4, files that exist in the cd path but NOT the base path
will be copied to the save path
NOTE: fs_copyfiles and case sensitivity. On fs_caseSensitiveOS 0 filesystems ( win32 ), the
copied files may change casing when copied over.
The relative path "sound/newstuff/test.wav" would be searched for in the following places:
for save path, dev path, base path, cd path:
	for current game, base game:
		search directory
		search zip files
downloaded files, to be written to save path + current game's directory
The filesystem can be safely shutdown and reinitialized with different
basedir / cddir / game combinations, but all other subsystems that rely on it
(sound, video) must also be forced to restart.
"fs_caseSensitiveOS":
This cvar is set on operating systems that use case sensitive filesystems (Linux and OSX)
It is a common situation to have the media reference filenames, whereas the file on disc
only matches in a case-insensitive way. When "fs_caseSensitiveOS" is set, the filesystem
will always do a case insensitive search.
IMPORTANT: This only applies to files, and not to directories. There is no case-insensitive
matching of directories. All directory names should be lowercase, when "com_developer" is 1,
the filesystem will warn when it catches bad directory situations (regardless of the
"fs_caseSensitiveOS" setting)
When bad casing in directories happen and "fs_caseSensitiveOS" is set, BuildOSPath will
attempt to correct the situation by forcing the path to lowercase. This assumes the media
is stored all lowercase.
"additional mod path search":
fs_game_base can be used to set an additional search path
in search order, fs_game, fs_game_base, BASEGAME
for instance to base a mod of D3 + D3XP assets, fs_game mymod, fs_game_base d3xp
"""

from common import *
from cvar_system import *
from shuka_lib.utils import get_os
_fs_restrict = IdCVar("fs_restrict", "", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'] | CVAR_FLAGS['CVAR_BOOL'],
                      "")
from functools import partial
import sys


class IdFileSystem:
    _instance = None

    @staticmethod
    def get_instance():
        return IdFileSystem._instance

    def __init__(self):
        IdFileSystem._instance = self

    def init(self):
        raise NotImplementedError()


class IdFileSystemLocal(IdFileSystem):
    def __init__(self):
        IdFileSystem.__init__(self)
        self.fs_restrict = IdCVar("fs_restrict", "",
                                  CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'] | CVAR_FLAGS['CVAR_BOOL'], "")
        self.fs_debug = IdCVar("fs_debug", "0", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INTEGER'], 0, 2,
                               value_completion=partial(IdCmdSystem.arg_completion_integer, args=(0, 2)))
        self.fs_copyfiles = IdCVar("fs_copyfiles", "0",
                                   CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INTEGER'] | CVAR_FLAGS['CVAR_INIT'], 0,
                                   4, value_completion=partial(IdCmdSystem.arg_completion_integer, args=(0, 3)))
        self.fs_basepath = IdCVar("fs_basepath", "", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'], "")
        self.fs_configpath = IdCVar("fs_configpath", "", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'], "")
        self.fs_savepath = IdCVar("fs_savepath", "", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'], "")
        self.fs_cdpath = IdCVar("fs_cdpath", "", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'], "")
        self.dev_path = IdCVar("dev_path", "", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'], "")
        self.fs_game = IdCVar("fs_game", "",
                              CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'] | CVAR_FLAGS['CVAR_SERVERINFO'],
                              "mod path")
        self.fs_game_base = IdCVar("fs_game_base", "",
                                   CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'] | CVAR_FLAGS['CVAR_SERVERINFO'],
                                   "alternate mod path, searched after the main fs_game path, before the basedir")
        if get_os()=='win':
            self.fs_case_sensitive_OS = IdCVar("fs_caseSensitiveOS", "0",
                                               CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_BOOL'], "")
        else:
            self.fs_case_sensitive_OS = IdCVar("fs_caseSensitiveOS", "1",
                                               CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_BOOL'], "")
        self.fs_search_addons = IdCVar("fs_searchAddons", "0", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_BOOL'],
                                       "search all addon pk4s ( disables addon functionality )")

    def init(self):
        """
        id:
        allow command line parms to override our defaults
        we have to specially handle this, because normal command
        line variable sets don't happen until after the filesystem
        has already been initialized
        """
        IdCommon.get_instance().startup_variable('fs_configpath', False)
        IdCommon.get_instance().startup_variable('fs_savepath', False)
        IdCommon.get_instance().startup_variable('fs_cdpath', False)
        IdCommon.get_instance().startup_variable('fs_devpath', False)
        IdCommon.get_instance().startup_variable('fs_game', False)
        IdCommon.get_instance().startup_variable('fs_game_base', False)
        IdCommon.get_instance().startup_variable('fs_copyfiles', False)
        IdCommon.get_instance().startup_variable('fs_restrict', False)
        IdCommon.get_instance().startup_variable('fs_searchAddons', False)
        path = ''
        if self.fs_basepath.get_string()[0] == '\0' and
	if (fs_basepath.GetString()[0] == '\0' && Sys_GetPath(PATH_BASE, path))
		fs_basepath.SetString(path);

	if (fs_savepath.GetString()[0] == '\0' && Sys_GetPath(PATH_SAVE, path))
		fs_savepath.SetString(path);

	if (fs_configpath.GetString()[0] == '\0' && Sys_GetPath(PATH_CONFIG, path))
		fs_configpath.SetString(path);

	if ( fs_devpath.GetString()[0] == '\0' ) {
#ifdef WIN32
		fs_devpath.SetString( fs_cdpath.GetString()[0] ? fs_cdpath.GetString() : fs_basepath.GetString() );
#else
		fs_devpath.SetString( fs_savepath.GetString() );
#endif
	}
