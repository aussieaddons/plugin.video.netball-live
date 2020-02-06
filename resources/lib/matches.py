import os
import sys

from aussieaddonscommon import utils

from resources.lib import comm

import xbmcaddon

import xbmcgui

import xbmcplugin

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon_path = xbmcaddon.Addon().getAddonInfo("path")


def make_matches_list(params):
    """
    Build match listing for Kodi
    """
    try:
        listing = []
        matches = comm.list_matches(params)

        for m in matches:
            li = xbmcgui.ListItem(label=str(m.title),
                                  iconImage=m.thumb,
                                  thumbnailImage=m.thumb)
            url = '{0}?action=listmatches{1}'.format(_url, m.make_kodi_url())
            is_folder = False
            li.setProperty('IsPlayable', 'true')
            li.setInfo('video', {'plot': m.title, 'plotoutline': m.title})
            listing.append((url, li, is_folder))

        if params['category'] == 'livematches':
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
