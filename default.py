import os
import sys

from future.moves.urllib.parse import parse_qsl

from aussieaddonscommon import utils

from resources.lib import categories
from resources.lib import matches
from resources.lib import play
from resources.lib import stream_auth

import xbmcaddon

import xbmcgui

_url = sys.argv[0]
_handle = int(sys.argv[1])
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')
addonPath = xbmcaddon.Addon().getAddonInfo("path")
fanart = os.path.join(addonPath, 'fanart.jpg')


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    """
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listcategories':
            if params['category'] == 'settings':
                addon.openSettings()
            else:
                matches.make_matches_list(params)
        elif params['action'] == 'listmatches':
            play.play_video(params)
        elif params['action'] == 'clearticket':
            stream_auth.clear_ticket()
        elif params['action'] == 'sendreport':
            utils.user_report()
        elif params['action'] == 'open_ia_settings':
            try:
                import drmhelper
                if drmhelper.check_inputstream(drm=False):
                    ia = drmhelper.get_addon()
                    ia.openSettings()
                else:
                    utils.dialog_message(
                        "Can't open inputstream.adaptive settings")
            except Exception:
                utils.dialog_message(
                    "Can't open inputstream.adaptive settings")
    else:
        categories.list_categories()


if __name__ == '__main__':
    if addon.getSetting('firstrun') == 'true':
        xbmcgui.Dialog().ok(addonname, ('Please enter your Netball Live '
                                        'Pass (Telstra ID) username and '
                                        'password to access the content '
                                        'in this service.'))
        addon.openSettings()
        addon.setSetting('firstrun', 'false')
    router(sys.argv[2][1:])
