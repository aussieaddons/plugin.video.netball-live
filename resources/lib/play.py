import sys

from aussieaddonscommon import utils

from resources.lib import comm

import xbmcaddon

import xbmcgui

import xbmcplugin

addon = xbmcaddon.Addon()
_handle = int(sys.argv[1])


def play_video(params):
    """
    Play a video by the provided path.
    :param path: str
    """

    if params.get('dummy') == 'True':
        return
    try:
        playlist = comm.get_stream_url(params)
        play_item = xbmcgui.ListItem(path=playlist)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
    except Exception:
        utils.handle_error('Unable to play video')
