import sys
import urllib

import urlparse
import xbmcgui
import xbmcplugin
from resources.lib import mechanize

URLS = {
"en":"http://randaris-anime.net/serie/english",
"de": "http://randaris-anime.net/serie/german",
"all": "http://randaris-anime.net/serie/full"
"base" : "http://randaris-anime.net/serie/alpha/"
}
SELECT_SERIES = "tbody > tr > td > a"

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')


def getSeries(url):
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open(url)
    print br
    return "MUH"

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def addDir(name,mode,**kwargs):
    urlDict = {"mode":mode}
    urlDict.update(kwargs)
    url = build_url(urlDict)
    li = xbmcgui.ListItem(name, iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

def endOfDir():
    xbmcplugin.endOfDirectory(addon_handle)

def crawl(url):
    return []
mode = args.get('mode', None)

print "MODE: "+str(mode)
if mode is None: #main menu
    addDir("A - Z","letters")
    addDir("Search","search")
    endOfDir()

elif mode[0] == "letters": #switch between ger, eng, all
    for c in "#ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        addDir(str(c),"showLetter",letter=str(c))
    endOfDir()

elif mode[0] == "showLetter":
    page = args.get("page","")
    letter = args["letter"][0]
    letter = "asc" if letter=="#" else letter
    addDir("Series starting with "+str(letter),"showLetter",letter=letter)
    toCrawl = URLS["base"]+letter+"/"+page
    series = crawl(toCrawl)
    for s in series: #add entries
        addDir(s["name"],"sUrl","url"="")
    #add pages
    endOfDir()
    
elif mode[0] == "all":
    lang = args["lang"][0]
    listUrl = URLS[lang]
    addDir(listUrl,"URL")
    getSeries(listUrl)
    endOfDir()

elif mode[0] == 'a_to_z_ger':
    url = 'http://localhost/some_video.mkv'
    li = xbmcgui.ListItem(getSeries(), iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    endOfDir()
    
    
