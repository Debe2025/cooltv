import xbmcplugin, xbmcgui, xbmcaddon, requests, urllib.parse, sys
addon = xbmcaddon.Addon()
handle = int(sys.argv[1])

def play(url):
    li = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(handle, True, li)

def list_channels():
    m3u = addon.getSetting('m3u_urls') or 'https://iptv-org.github.io/iptv/index.m3u'
    urls = [u.strip() for u in m3u.split(',') if u.strip()]
    channels = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            lines = r.text.splitlines()
            name = ""
            for line in lines:
                if line.startswith('#EXTINF'):
                    name = line.split(',', 1)[-1].strip()
                elif line.startswith('http') and name:
                    channels.append((name, line.strip()))
                    name = ""
        except: pass
    for name, url in channels:
        li = xbmcgui.ListItem(name)
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle, f"{sys.argv[0]}?play={urllib.parse.quote(url)}", li, False)
    xbmcplugin.endOfDirectory(handle)

params = urllib.parse.parse_qs(urllib.parse.urlparse(sys.argv[2]).query)
if 'play' in params:
    play(urllib.parse.unquote(params['play'][0]))
else:
    list_channels()
