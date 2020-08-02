import sys

from aussieaddonscommon import utils

from resources.lib import comm
from resources.lib import stream_auth

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
        media_auth_token = None
        if params.get('live') == 'true':
            ticket = stream_auth.get_user_ticket()
            media_auth_token = stream_auth.get_media_auth_token(
                ticket, params.get('video_id'))
        playlist = comm.get_stream_url(params, media_auth_token)
        listitem = xbmcgui.ListItem(path=playlist)
        listitem.setProperty('inputstreamaddon', 'inputstream.adaptive')
        listitem.setProperty('inputstream.adaptive.manifest_type', 'hls')
        xbmcplugin.setResolvedUrl(_handle, True, listitem=listitem)
    except Exception:
        raise
        utils.handle_error('Unable to play video')
