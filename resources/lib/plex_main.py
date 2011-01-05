import sys, urllib2, xbmcplugin, xbmcgui, xbmcaddon
from BeautifulSoup import BeautifulStoneSoup

__settings__ = xbmcaddon.Addon(id = 'plugin.video.plex')

class Main:
	def __init__(self):
		baseurl = "http://%s:%s" % (__settings__.getSetting('hostname'), __settings__.getSetting('port'))
		handle = int(sys.argv[1])
		section = sys.argv[2][1:] # strip leading '?' from query-args
		if section == "":
			section = "/library/sections"

		response = urllib2.urlopen(baseurl + section)
		soup = BeautifulStoneSoup(response.read(), convertEntities = "xml")

		items = soup.mediacontainer.findAll({'directory': True, 'video': True })
		for item in items:
			name = item["title"]
			url = ""
			thumbnail = item.get("thumb")
			isFolder = False
			infoLabels = { "title": name }

			if thumbnail == None:
				thumbnail = "DefaultFolder.png"
			else:
				thumbnail = baseurl + thumbnail
				icon = thumbnail

			if item.name == "directory":
				isFolder = True
				infoLabels["count"] = item.get("leafCount", 1)

				# Make an absolute URL if item[key] is relative
				if item["key"][0] == "/":
					url = "%s?%s" % (sys.argv[0], item["key"])
				else:
					url = "%s?%s/%s" % (sys.argv[0], section, item["key"])
			elif item.name == "video":
				url = baseurl + item.media.part["key"]
				infoLabels["plot"] = item["summary"]
				infoLabels["rating"] = float(item.get("rating", "0.0"))
				infoLabels["size"] = int(item.media.part["size"])

				if item["type"] == "episode":
					infoLabels["episode"] = int(item["index"])
					if soup.mediacontainer.get("parentIndex"):
						infoLabels["season"] = soup.mediacontainer["parentIndex"]
				else:
					infoLabels["studio"] = item.get("studio", "")
					infoLabels["year"] = int(item.get("year", "0"))

			liz = xbmcgui.ListItem(label = name, iconImage = thumbnail, thumbnailImage = thumbnail, path = url)
			liz.setInfo(type = "Video", infoLabels = infoLabels)
			xbmcplugin.addDirectoryItem(handle = handle, url = url, listitem = liz, isFolder = isFolder, totalItems = len(items))

		xbmcplugin.endOfDirectory(handle)
