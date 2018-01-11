import xbmcaddon
import xbmcgui
import xbmcplugin
import sys
import ooyalahelper
from aussieaddonscommon import utils

addon = xbmcaddon.Addon()
_handle = int(sys.argv[1])


def play_video(params):
    """
    Play a video by the provided path.
    :param path: str
    """

    if params['dummy'] == 'True':
        return
    try:
        live = params['live'] == 'true'
        video_id = params['video_id']
        playlist = ooyalahelper.get_m3u8_playlist(video_id, live)
        play_item = xbmcgui.ListItem(path=playlist)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
    except Exception:
        utils.handle_error('Unable to play video')
