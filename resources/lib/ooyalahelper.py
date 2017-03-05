# Copyright 2017 Glenn Guy
# This file is part of Netball Live Kodi Addon
#
# Netball Live is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NRL Live is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Netball Live.  If not, see <http://www.gnu.org/licenses/>.

import urllib
import urllib2
import requests
import cookielib
import ssl

import time
import os
import sys
from urlparse import parse_qsl
import xml.etree.ElementTree as ET
import json
import base64

import config
import utils
import xbmcaddon
import xbmc
import telstra_auth
from exception import NetballLiveException

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.poolmanager import PoolManager
import platform


# Ignore InsecureRequestWarning warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
session.verify = False

addon = xbmcaddon.Addon()
username = addon.getSetting('LIVE_USERNAME')
password = addon.getSetting('LIVE_PASSWORD')

    
def get_user_token():
    """send user login info and retrieve user id for session"""
    
    stored_ticket = addon.getSetting('TICKET')
    if stored_ticket != '':
        return stored_ticket
    
    ticket = telstra_auth.get_free_token(username, password)
    addon.setSetting('TICKET', ticket)
    return ticket

def fetch_hds_smil(video_id):
    """ contact ooyala server and retrieve smil data to be decoded"""
    url = config.SMIL_URL.format(video_id)
    utils.log("Fetching URL: {0}".format(url))
    res = session.get(url)
    return res.text

def get_hds_url(encrypted_smil):
    """ decrypt smil data and return HDS url from the xml data"""
    from ooyala import ooyalaCrypto
    decrypt = ooyalaCrypto.ooyalaCrypto()
    smil_xml = decrypt.ooyalaDecrypt(encrypted_smil)
    tree = ET.fromstring(smil_xml)
    return tree.find('content').find('video').find('httpDynamicStreamUrl').text


def get_embed_token(user_token, video_id):
    """send our user token to get our embed token, including api key"""
    url = config.EMBED_TOKEN_URL.format(video_id)
    session.headers.update({'X-YinzCam-Ticket': user_token, 
                            'Accept': 'application/json'})
    utils.log("Fetching URL: {0}".format(url))
    try:
        req = session.get(url, verify=False)
        data = req.text
        json_data = json.loads(data)
        video_token = json_data.get('VideoToken')
    except:
        addon.setSetting('TICKET', '')
        raise Exception
    return urllib.quote(video_token)

#common ooyala functions
 
def get_secure_token(secure_url, videoId):
    """send our embed token back with a few other url encoded parameters"""
    res = session.get(secure_url)
    data = res.text
    parsed_json = json.loads(data)
    iosToken =  parsed_json['authorization_data'][videoId]['streams'][0]['url']['data']
    return base64.b64decode(iosToken)

def get_m3u8_streams(secure_token_url):
    """ fetch our m3u8 file which contains streams of various qualities"""
    res = session.get(secure_token_url)
    data = res.text.splitlines()
    return data
   
def parse_m3u8_streams(data, live, secure_token_url):
    """ Parse the retrieved m3u8 stream list into a list of dictionaries
        then return the url for the highest quality stream. Different 
        handling is required of live m3u8 files as they seem to only contain
        the destination filename and not the domain/path."""
    if live:
        qual = int(addon.getSetting('LIVEQUALITY'))
        if qual >= 6:
            addon.setSetting('LIVEQUALITY', '5')
            qual = 5
    else:
        qual = int(addon.getSetting('HLSQUALITY'))
        if qual >= 6:
            addon.setSetting('HLSQUALITY', '5')
            qual = 5
    if '#EXT-X-VERSION:3' in data:
        data.remove('#EXT-X-VERSION:3')
    count = 1
    m3u_list = []
    prepend_live = secure_token_url[:secure_token_url.find('index')]
    while count < len(data):
        line = data[count]
        line = line.strip('#EXT-X-STREAM-INF:')
        line = line.strip('PROGRAM-ID=1,')
        line = line[:line.find('CODECS')]
        
        if line.endswith(','):
            line = line[:-1]
        
        line = line.strip()
        line = line.split(',')
        linelist = [i.split('=') for i in line]
        
        if not live:
            linelist.append(['URL',data[count+1]])
        else:
            linelist.append(['URL',prepend_live+data[count+1]])
        
        m3u_list.append(dict((i[0], i[1]) for i in linelist))
        count += 2
    
    sorted_m3u_list = sorted(m3u_list, key=lambda k: int(k['BANDWIDTH']))
    if qual >= len(sorted_m3u_list):
        utils.log('Error in expected amount of streams or qual value, '
                  'defaulting to highest')
        qual = len(sorted_m3u_list)-1
    stream = sorted_m3u_list[qual]['URL']
    return stream
   
def get_m3u8_playlist(video_id, live):
    """ Main function to call other functions that will return us our m3u8 HLS
        playlist as a string, which we can then write to a file for Kodi
        to use"""
    login_token = get_user_token()
    embed_token = get_embed_token(login_token, video_id)
    authorize_url = config.AUTH_URL.format(config.PCODE, video_id, embed_token)
    secure_token_url = get_secure_token(authorize_url, video_id)
    utils.log(secure_token_url)
    if 'chunklist.m3u8' in secure_token_url:
        return secure_token_url

    m3u8_data = get_m3u8_streams(secure_token_url)
    m3u8_playlist_url = parse_m3u8_streams(m3u8_data, live, secure_token_url)
    return m3u8_playlist_url