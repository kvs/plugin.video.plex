import xbmcaddon

__plugin__  = "Plex"
__author__  = "kvs"
__version__ = "0.1.0"

print "[PLUGIN] '%s: version %s' initialized!" % (__plugin__, __version__)

if __name__ == "__main__":
	from resources.lib import plex_main
	plex_main.Main()

sys.modules.clear()
