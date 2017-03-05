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

import requests
import collections
import json
import urlparse
import urllib
import config
import re
import uuid
import ssl
import utils
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import xbmcgui

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.poolmanager import PoolManager


# Ignore InsecureRequestWarning warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
header_order = ''


class TelstraAuthException(Exception):
    """ A Not Fatal Exception is used for certain conditions where we do not
        want to give users an option to send an error report
    """
    pass


class TLSv1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def get_free_token(username, password):
    """ Obtain a valid token from Telstra/Yinzcam, will be used to make requests for 
        Ooyala embed tokens"""    
    session = requests.Session()
    session.verify = False
    session.mount("https://", TLSv1Adapter(max_retries=5))
    
    prog_dialog = xbmcgui.DialogProgress()
    prog_dialog.create('Logging in with Telstra ID')
    prog_dialog.update(1, 'Obtaining user token')
    
    # Send our first login request to Yinzcam, recieve (unactivated) token
    # and 'msisdn' URL
    session.headers = config.YINZCAM_AUTH_HEADERS
    data = config.NEW_LOGIN_DATA1.format(uuid.uuid4())
    ticket_resp = session.post(config.YINZCAM_AUTH_URL, data=data)
    ticket = json.loads(ticket_resp.text).get('Ticket')
    session.headers = {}
    session.headers.update({'X-YinzCam-Ticket': ticket})
    yinz_resp = session.get(config.YINZCAM_AUTH_URL2)
    jsondata = json.loads(yinz_resp.text)
    token = jsondata.get('TpUid')
    if not token:
        raise TelstraAuthException('Unable to get token from Netball API')
    msisdn_url = jsondata.get('Url')
    msisdn_url = msisdn_url.replace('?tpUID', '.html?device=mobile&tpUID')
    prog_dialog.update(20, 'Signing on to telstra.com')
    
    # Sign in to telstra.com to recieve cookies, get the SAML auth, and 
    # modify the escape characters so we can send it back later
    session.headers = config.SIGNON_HEADERS
    signon_data = config.SIGNON_DATA
    signon_data.update({'username': username, 'password': password})
    signon = session.post(config.SIGNON_URL, data=signon_data)
    
    signon_pieces = urlparse.urlsplit(signon.url)
    signon_query = dict(urlparse.parse_qsl(signon_pieces.query))

    utils.log('Sign-on result: %s' % signon_query)

    if 'errorcode' in signon_query:
        if signon_query['errorcode'] == '0':
            raise TelstraAuthException('Please enter your username '
                                       'in the settings')
        if signon_query['errorcode'] == '1':
            raise TelstraAuthException('Please enter your password '
                                       'in the settings')
        if signon_query['errorcode'] == '2':
            raise TelstraAuthException('Please enter your username and '
                                       'password in the settings')
        if signon_query['errorcode'] == '3':
            raise TelstraAuthException('Please check your username and '
                                       'password in the settings')
    soup = BeautifulSoup(signon.text, 'html.parser')
    saml_base64 = soup.find(attrs={'name': 'SAMLResponse'}).get('value')
    prog_dialog.update(40, 'Obtaining API token')
    
    # Send the SAML login data and retrieve the auth token from the response
    session.headers = {}
    session.headers = config.SAML_LOGIN_HEADERS
    session.cookies.set('saml_request_path', msisdn_url)
    saml_data = 'SAMLResponse=' + urllib.quote(saml_base64)
    utils.log('Fetching stream auth token: {0}'.format(config.SAML_LOGIN_URL))   
    saml_login = session.post(config.SAML_LOGIN_URL, data=saml_data)
    confirm_url = saml_login.url
    auth_token_match = re.search('apiToken = "(\w+)"', saml_login.text)
    auth_token = auth_token_match.group(1)
    prog_dialog.update(60, 'Determining eligible services')
    
    # 'Order' the subscription package to activate our token/login
    offer_id = dict(urlparse.parse_qsl(urlparse.urlsplit(msisdn_url)[3]))['offerId']
    media_order_headers = config.MEDIA_ORDER_HEADERS
    media_order_headers.update({'Authorization': 'Bearer {0}'.format(auth_token), 
                                'Referer': confirm_url})
    session.headers = media_order_headers
    # First check if there are any eligible services attached to the account
    offers = session.get(config.OFFERS_URL)
    try:
        offers.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            message = json.loads(e.response.text).get('userMessage')
            message += (' Please visit {0} '.format(config.HUB_URL) +
                        'for further instructions to link your mobile '
                        'service to the supplied Telstra ID')
            raise TelstraAuthException(message)
        else:
            raise TelstraAuthException(e.response.status_code)
    try:
        offer_data = json.loads(offers.text)
        offers_list = offer_data['data']['offers']
        for offer in offers_list:
            if offer.get('name') != 'Netball Live Pass':
                continue
            data = offer.get('productOfferingAttributes')
            ph_no = [x['value'] for x in data if x['name'] == 'ServiceId'][0]
    except:
        raise TelstraAuthException('Unable to determine eligible services')
    prog_dialog.update(80, 'Obtaining Live Pass')
    order_data = config.MEDIA_ORDER_JSON.format(ph_no, offer_id, token)
    order = session.post(config.MEDIA_ORDER_URL, data=order_data)
    # check to make sure order has been placed correctly
    if order.status_code == 201:
        try:
            order_json = json.loads(order.text)
            status = order_json['data'].get('status') == 'COMPLETE'
            if status:
                utils.log('Order status complete')
        except:
            utils.log('Unable to check status of order, continuing anyway')

    session.close()
    prog_dialog.update(100, 'Finished!')
    prog_dialog.close()
    return ticket