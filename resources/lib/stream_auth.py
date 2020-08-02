import json

import requests

from aussieaddonscommon import session
from aussieaddonscommon import utils
from aussieaddonscommon.exceptions import AussieAddonsException

from resources.lib import config
from resources.lib import telstra_auth

import xbmcaddon

try:
    import StorageServer
except ImportError:
    utils.log("script.common.plugin.cache not found!")
    import resources.lib.storageserverdummy as StorageServer

cache = StorageServer.StorageServer(config.ADDON_ID, 1)
sess = session.Session(force_tlsv1=True)
addon = xbmcaddon.Addon()
username = addon.getSetting('LIVE_USERNAME')
password = addon.getSetting('LIVE_PASSWORD')


def clear_ticket():
    """
    Remove stored ticket from cache storage
    """
    cache.delete('NETBALLTICKET')
    utils.dialog_message('Login token removed')


def get_user_ticket():
    """
    send user login info and retrieve ticket for session
    """
    stored_ticket = cache.get('NETBALLTICKET')
    if stored_ticket != '':
        utils.log('Using ticket: {0}******'.format(stored_ticket[:-6]))
        return stored_ticket
    else:
        auth = telstra_auth.TelstraAuth(username, password)
        ticket = auth.get_free_token()
    cache.set('NETBALLTICKET', ticket)
    return ticket


def get_media_auth_token(ticket, video_id):
    """
    send our user token to get our embed token, including api key
    """
    url = config.MEDIA_AUTH_URL.format(video_id=video_id)
    sess.headers = {}
    sess.headers.update(
        {'X-YinzCam-Ticket': ticket,
         'Accept': 'application/json'})
    try:
        req = sess.get(url)
        data = req.text
        json_data = json.loads(data)
        if json_data.get('Fault'):
            raise AussieAddonsException(
                json_data.get('fault').get('faultstring'))
        media_auth_token = json_data.get('VideoToken')
    except requests.exceptions.HTTPError as e:
        utils.log('Error getting embed token. '
                  'Response: {0}'.format(e.response.text))
        cache.delete('NETBALLTICKET')
        if e.response.status_code == 401:
            raise AussieAddonsException('Login token has expired, '
                                        'please try again.')
        else:
            raise e
    return media_auth_token
