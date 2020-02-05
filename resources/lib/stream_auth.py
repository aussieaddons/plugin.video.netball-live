import urllib
import json
import base64
import config
import re
import requests
import xbmcaddon
import telstra_auth

from aussieaddonscommon.exceptions import AussieAddonsException
from aussieaddonscommon import session
from aussieaddonscommon import utils

try:
    import StorageServer
except:
    utils.log("script.common.plugin.cache not found!")
    import storageserverdummy as StorageServer
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
