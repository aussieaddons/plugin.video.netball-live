import xbmcgui
import xbmcplugin
import xbmcaddon
import comm
import sys
import os
from aussieaddonscommon import utils

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_path = xbmcaddon.Addon().getAddonInfo("path")


def make_matches_list(params, live=False):
    """
    Build match listing for Kodi
    """
    try:
        listing = []
        matches = comm.list_matches(params, live)

        for m in matches:
            li = xbmcgui.ListItem(label=str(m.title),
                                  iconImage=m.thumb,
                                  thumbnailImage=m.thumb)
            url = '{0}?action=listmatches{1}'.format(_url, m.make_kodi_url())
            is_folder = False
            li.setProperty('IsPlayable', 'true')
            li.setInfo('video', {'plot': m.desc, 'plotoutline': m.desc})
            listing.append((url, li, is_folder))

        if live:
            upcoming = comm.get_upcoming()
            for event in upcoming:
                thumb = os.path.join(addon_path, 'resources', 'soon.jpg')
                li = xbmcgui.ListItem(event.title, iconImage=thumb)
                url = '{0}?action=listmatches{1}'.format(_url,
                                                         event.make_kodi_url())
                is_folder = False
                listing.append((url, li, is_folder))
            xbmcplugin.addSortMethod(
                _handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)

        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.endOfDirectory(_handle)
    except Exception:
        utils.handle_error('Unable to display matches')
