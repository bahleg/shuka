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
from id_sys.linux_port.main import sys_get_path
from functools import partial


class IdFileSystem:
    _instance = None

    @staticmethod
    def get_instance():
        return IdFileSystem._instance

    def __init__(self):
        IdFileSystem._instance = self

    def init(self):
        raise NotImplementedError()


class _Directory:
    def __init__(self):
        self.path = ''  # id: c:\doom
        self.gamedir = ''  # id: base


class _SearchPath:
    def __init__(self):
        self.pack = None  # id:  only one of pack / dir will be non NULL
        self.dir = None


class _Pack:
    def __init__(self):
        self.pak_filename = ''  # id: c:\doom\base\pak0.pk4
        self.handle = None
        self.checksum = 0
        self.num_files = 0
        self.length = 0
        self.referenced = False
        self.addon = False  # id: this is an addon pack - addon_search tells if it's 'active'
        self.addon_info = None
        self.pure_status = None
        self.is_new = False  # id: for downloaded packs
        self.hashTable = None
        self.build_buffer = None


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
        self.fs_dev_path = IdCVar("fs_devpath", "", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'], "")
        self.fs_game = IdCVar("fs_game", "",
                              CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'] | CVAR_FLAGS['CVAR_SERVERINFO'],
                              "mod path")
        self.fs_game_base = IdCVar("fs_game_base", "",
                                   CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_INIT'] | CVAR_FLAGS['CVAR_SERVERINFO'],
                                   "alternate mod path, searched after the main fs_game path, before the basedir")
        if get_os() == 'win':
            self.fs_case_sensitive_OS = IdCVar("fs_caseSensitiveOS", "0",
                                               CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_BOOL'], "")
        else:
            self.fs_case_sensitive_OS = IdCVar("fs_caseSensitiveOS", "1",
                                               CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_BOOL'], "")
        self.fs_search_addons = IdCVar("fs_searchAddons", "0", CVAR_FLAGS['CVAR_SYSTEM'] | CVAR_FLAGS['CVAR_BOOL'],
                                       "search all addon pk4s ( disables addon functionality )")

        self.search_paths = []
        self.read_count = 0
        self.load_count = 0
        self.load_stack = 0
        self.dir_cache_index = 0
        self.dir_cache_count = 0
        self.d3xp = 0
        self.loaded_file_from_dir = False
        self.background_thread_exit = False
        self.addon_packs = []
        # id: this will be a single name without separators
        self.game_folder = ''

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
        path = sys_get_path('PATH_BASE')
        if self.fs_basepath.get_string() == '' and path:
            self.fs_basepath.set_string(path)

        path = sys_get_path('PATH_SAVE')
        if self.fs_savepath.get_string() == '' and path:
            self.fs_savepath.set_string(path)

        path = sys_get_path('PATH_CONFIG')
        if self.fs_configpath.get_string() == '' and path:
            self.fs_configpath.set_string(path)

        if self.fs_dev_path.get_string() == '':
            if get_os() == 'win':
                if self.fs_cdpath.get_string() != '':
                    self.fs_dev_path.set_string(self.fs_cdpath.get_string())
                else:
                    self.fs_dev_path.set_string(self.fs_basepath.get_string())
            else:
                self.fs_dev_path.set_string(self.fs_savepath.get_string())
        self.startup()

    def add_game_directory(self, path, dir):
        """
        id: Sets gameFolder, adds the directory to the head of the search paths, then loads any pk4 files.
        """
        # id: check if the search path already exists
        for search in self.search_paths:
            # id:  f this element is a pak file
            if not search.dir:
                continue
            if search.dir.path == path and search.dir == dir:
                return
        self.game_folder = dir
        # id: add the directory to the search path
        search = _SearchPath()
        search.dir = _Directory()
        search.pack = None
        search.dir.path = path
        search.dir.gamedir = dir
        self.search_paths.append(search)
        # id: find all pak files in this directory
        pakfile = os.path.join(path, dir)
        pakfiles = [f for f in os.listdir(pakfile) if f.endswith('.pk4')]
        # id: sort them so that later alphabetic matches override
        # earlier ones. This makes pak1.pk4 override pak0.pk4
        pakfiles.sort(reverse=True)
        for i in xrange(len(pakfiles)):
            pakfile = os.path.join(path, dir, pakfiles[i])
            pak = self.load_zip_file(pakfile)
            if not pak:
                continue
            # id: insert the pak after the directory it comes from
            search = _SearchPath()
            search.dir = None
            search.pack = pak
            self.search_paths.append(search)
            logging.info('Loaded pk4 {0} with checksum {1}'.format(pakfile, pak.checksum))

    def load_zip_file(self, zipfile):
        raise NotImplementedError()

    def startup(self):
        logging.info('----- Initializing File System -----')
        not_implemented_log('checknums rouitines')
        """



	SetupGameDirectories( BASE_GAMEDIR );

	// fs_game_base override
	if ( fs_game_base.GetString()[0] &&
		 idStr::Icmp( fs_game_base.GetString(), BASE_GAMEDIR ) ) {
		SetupGameDirectories( fs_game_base.GetString() );
	}

	// fs_game override
	if ( fs_game.GetString()[0] &&
		 idStr::Icmp( fs_game.GetString(), BASE_GAMEDIR ) &&
		 idStr::Icmp( fs_game.GetString(), fs_game_base.GetString() ) ) {
		SetupGameDirectories( fs_game.GetString() );
	}

	// currently all addons are in the search list - deal with filtering out and dependencies now
	// scan through and deal with dependencies
	search = &searchPaths;
	while ( *search ) {
		if ( !( *search )->pack || !( *search )->pack->addon ) {
			search = &( ( *search )->next );
			continue;
		}
		pak = ( *search )->pack;
		if ( fs_searchAddons.GetBool() ) {
			// when we have fs_searchAddons on we should never have addonChecksums
			assert( !addonChecksums.Num() );
			pak->addon_search = true;
			search = &( ( *search )->next );
			continue;
		}
		addon_index = addonChecksums.FindIndex( pak->checksum );
		if ( addon_index >= 0 ) {
			assert( !pak->addon_search );	// any pak getting flagged as addon_search should also have been removed from addonChecksums already
			pak->addon_search = true;
			addonChecksums.RemoveIndex( addon_index );
			FollowAddonDependencies( pak );
		}
		search = &( ( *search )->next );
	}

	// now scan to filter out addons not marked addon_search
	search = &searchPaths;
	while ( *search ) {
		if ( !( *search )->pack || !( *search )->pack->addon ) {
			search = &( ( *search )->next );
			continue;
		}
		assert( !( *search )->dir );
		pak = ( *search )->pack;
		if ( pak->addon_search ) {
			common->Printf( "Addon pk4 %s with checksum 0x%x is on the search list\n",
							pak->pakFilename.c_str(), pak->checksum );
			search = &( ( *search )->next );
		} else {
			// remove from search list, put in addons list
			searchpath_t *paksearch = *search;
			*search = ( *search )->next;
			paksearch->next = addonPaks;
			addonPaks = paksearch;
			common->Printf( "Addon pk4 %s with checksum 0x%x is on addon list\n",
							pak->pakFilename.c_str(), pak->checksum );
		}
	}

	// all addon paks found and accounted for
	assert( !addonChecksums.Num() );
	addonChecksums.Clear();	// just in case

	if ( restartChecksums.Num() ) {
		search = &searchPaths;
		while ( *search ) {
			if ( !( *search )->pack ) {
				search = &( ( *search )->next );
				continue;
			}
			if ( ( i = restartChecksums.FindIndex( ( *search )->pack->checksum ) ) != -1 ) {
				if ( i == 0 ) {
					// this pak is the next one in the pure search order
					serverPaks.Append( ( *search )->pack );
					restartChecksums.RemoveIndex( 0 );
					if ( !restartChecksums.Num() ) {
						break; // early out, we're done
					}
					search = &( ( *search )->next );
					continue;
				} else {
					// this pak will be on the pure list, but order is not right yet
					searchpath_t	*aux;
					aux = ( *search )->next;
					if ( !aux ) {
						// last of the list can't be swapped back
						if ( fs_debug.GetBool() ) {
							common->Printf( "found pure checksum %x at index %d, but the end of search path is reached\n", ( *search )->pack->checksum, i );
							idStr checks;
							checks.Clear();
							for ( i = 0; i < serverPaks.Num(); i++ ) {
								checks += va( "%p ", serverPaks[ i ] );
							}
							common->Printf( "%d pure paks - %s \n", serverPaks.Num(), checks.c_str() );
							checks.Clear();
							for ( i = 0; i < restartChecksums.Num(); i++ ) {
								checks += va( "%x ", restartChecksums[ i ] );
							}
							common->Printf( "%d paks left - %s\n", restartChecksums.Num(), checks.c_str() );
						}
						common->FatalError( "Failed to restart with pure mode restrictions for server connect" );
					}
					// put this search path at the end of the list
					searchpath_t *search_end;
					search_end = ( *search )->next;
					while ( search_end->next ) {
						search_end = search_end->next;
					}
					search_end->next = *search;
					*search = ( *search )->next;
					search_end->next->next = NULL;
					continue;
				}
			}
			// this pak is not on the pure list
			search = &( ( *search )->next );
		}
		// the list must be empty
		if ( restartChecksums.Num() ) {
			if ( fs_debug.GetBool() ) {
				idStr checks;
				checks.Clear();
				for ( i = 0; i < serverPaks.Num(); i++ ) {
					checks += va( "%p ", serverPaks[ i ] );
				}
				common->Printf( "%d pure paks - %s \n", serverPaks.Num(), checks.c_str() );
				checks.Clear();
				for ( i = 0; i < restartChecksums.Num(); i++ ) {
					checks += va( "%x ", restartChecksums[ i ] );
				}
				common->Printf( "%d paks left - %s\n", restartChecksums.Num(), checks.c_str() );
			}
			common->FatalError( "Failed to restart with pure mode restrictions for server connect" );
		}
	}

	// add our commands
	cmdSystem->AddCommand( "dir", Dir_f, CMD_FL_SYSTEM, "lists a folder", idCmdSystem::ArgCompletion_FileName );
	cmdSystem->AddCommand( "dirtree", DirTree_f, CMD_FL_SYSTEM, "lists a folder with subfolders" );
	cmdSystem->AddCommand( "path", Path_f, CMD_FL_SYSTEM, "lists search paths" );
	cmdSystem->AddCommand( "touchFile", TouchFile_f, CMD_FL_SYSTEM, "touches a file" );
	cmdSystem->AddCommand( "touchFileList", TouchFileList_f, CMD_FL_SYSTEM, "touches a list of files" );

	// print the current search paths
	Path_f( idCmdArgs() );
	        """
