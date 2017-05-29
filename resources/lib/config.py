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
# flake8: noqa

import version

NAME = 'Netball Live'
ADDON_ID = 'plugin.video.netball-live'
VERSION = version.VERSION

GITHUB_API_URL = 'https://api.github.com/repos/glennguy/plugin.video.netball-live'
ISSUE_API_URL = GITHUB_API_URL + '/issues'
ISSUE_API_AUTH = 'eGJtY2JvdDo1OTQxNTJjMTBhZGFiNGRlN2M0YWZkZDYwZGQ5NDFkNWY4YmIzOGFj'
GIST_API_URL = 'https://api.github.com/gists'

MAX_LIVEQUAL = 5
MAX_REPLAYQUAL = 7

# XML template to insert username and password into
LOGIN_DATA ='<Subscriber><Type>TDI</Type><User>{0}</User><Password>{1}</Password><Email>{0}</Email><AdobeCheckResult>0</AdobeCheckResult></Subscriber>'

# url used to request ooyala token
EMBED_TOKEN_URL ='https://signon-league-net.yinzcam.com/subscription/videotoken?application=NET_LEAGUE&ff=mobile&mnc=0&app_version=2.1.3&carrier=&version=5.6&width=1080&height=1776&os_version=6.0&mcc=0&application=NET_LEAGUE&embed_code={0}&ycurl_version=1&os=Android'

# url used to request playlist
AUTH_URL = 'http://player.ooyala.com/sas/player_api/v2/authorization/embed_code/{0}/{1}?device=html5&domain=http%3A%2F%2Fwww.ooyala.com&embedToken={2}&supportedFormats=m3u8'

# main url for xml that contains metadata for other non-live videos            
XML_URL = 'http://app-league-net.yinzcam.com/V1/media/taggedlist/media-type/V?ff=mobile&mnc=0&app_version=2.1.3&carrier=&version=5.6&width=1080&height=1776&os_version=6.0&mcc=0&application=NET_LEAGUE&ycurl_version=1&os=Android'

# xml for replay videos
REPLAY_URL = 'http://app-league-net.yinzcam.com/V1/Media/TaggedList/card/matchreplays?ff=mobile&mnc=0&app_version=2.2.5&carrier=&version=5.6&width=1080&height=1776&os_version=6.0&mcc=0&application=NET_LEAGUE&ycurl_version=1&os=Android'          

# url for xml that contains match scores
SCORE_URL = 'http://app-league-net.yinzcam.com/V1/Game/Scores/?ff=mobile&mnc=0&app_version=2.1.3&carrier=&version=5.6&width=1080&height=1776&os_version=6.0&mcc=0&application=NET_LEAGUE&ycurl_version=1&os=Android'

# index of android app homepage - has current round game id's
INDEX_URL = 'http://app-league-net.yinzcam.com/V1/Home/Index?ff=mobile&mnc=0&app_version=2.1.3&carrier=&version=5.6&width=1080&height=1776&os_version=6.0&mcc=0&application=NET_LEAGUE&ycurl_version=1&os=Android'

# Score and team names for upcoming games
BOX_URL = 'http://app-league-net.yinzcam.com/V1/Game/Box/{0}?ff=mobile&mnc=0&app_version=2.1.3&carrier=&version=5.6&width=1080&height=1776&os_version=6.0&mcc=0&application=NET_LEAGUE&ycurl_version=1&os=Android'

# used to get metadata for playing live matches
LIVE_MEDIA_URL = 'http://app-league-net.yinzcam.com/V1/Media/Video/{0}?ff=mobile&mnc=0&app_version=2.1.3&carrier=&version=5.6&width=1080&height=1776&os_version=6.0&mcc=0&application=NET_LEAGUE&ycurl_version=1&os=Android'

# used for HDS metadata retrieval
SMIL_URL = "http://player.ooyala.com/nuplayer?embedCode={0}"

# ooyala provider indentifier code used in contructing request uris            
PCODE = 'BudDUxOt2GEh8L5PMMpcbz1wJFwm'

YEARS = ['2013', '2014', '2015', '2016', '2017']

CATEGORIES = {'1 Live Matches': 'livematches',
                '2 Full Match Replays': 'MatchReplays',
                '3 Match Highlights': 'MatchHighlights',
                '4 News': 'News',
                '5 Other Videos': 'Others',
                '6 Settings': 'settings'}

COMPS = {'1 Telstra Premiership': '1',
            '2 State of Origin' : '30',
            '3 Auckland Nines'  : '20',
            '4 All Stars'       : '51',
            '5 World Club Series': '42',
            '6 International Tests': '40',
            '7 Country v City'  : '50',
            '8 State or Origin U20': '31',
            '9 Four Nations'    : '41'}
            

# New auth config for 2017

NEW_LOGIN_DATA1 = '<TicketRequest><Anonymous><VendorId>6a7db518-b912-4060-b08b-a733544fc9ef</VendorId><AppId>NET_LEAGUE</AppId><InstallId>{0}</InstallId></Anonymous></TicketRequest>'

NEW_LOGIN_DATA2 = '<Subscriber><Type>TOKEN</Type><User>{0}</User></Subscriber>'

YINZCAM_AUTH_URL = 'https://signon-league-net.yinzcam.com/ticket?mnc=0&ff=mobile&app_version=2.1.3&carrier=&version=5.6&height=1776&width=1080&mcc=0&application=NET_LEAGUE&ycurl_version=1&os=Android'

YINZCAM_AUTH_URL2 = 'https://signon-league-net.yinzcam.com/telstra/oneplace/url?application=NET_LEAGUE'

YINZCAM_AUTH_HEADERS = {'Content-Type': 'application/xml', 
                        'Accept': 'application/json', 
                        'Connection': 'close', 
                        'Content-Length': 'placeholder', 
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; HTC One_M8 Build/MRA58K.H15)', 
                        'Host': 'signon-league-net.yinzcam.com', 
                        'Accept-Encoding': 'gzip'}

SIGNON_HEADERS = {'Host': 'signon.telstra.com', 
                  'Connection': 'keep-alive', 
                  'Cache-Control': 'max-age=0', 
                  'Origin': 'https://signon.telstra.com', 
                  'Upgrade-Insecure-Requests': '1', 
                  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36', 
                  'Content-Type': 'application/x-www-form-urlencoded', 
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
                  'Referer': 'https://signon.telstra.com/login?goto=https%3A%2F%2Fsignon.telstra.com%2Ffederation%2Fsaml2%3FSPID%3Dtelstramedia&gotoNoTok=', 
                  'Accept-Encoding': 'gzip, deflate', 
                  'Accept-Language': 'en-AU,en-US;q=0.8'}
                        
SIGNON_URL = 'https://signon.telstra.com/login'

SIGNON_DATA = {'goto': 'https://signon.telstra.com/federation/saml2?SPID=telstramedia', 'gotoOnFail': '', 'username': None, 'password': None}

SAML_LOGIN_URL = 'https://hub.telstra.com.au/login/saml_login'

SAML_LOGIN_HEADERS = {'Host': 'hub.telstra.com.au', 
                      'Connection': 'keep-alive', 
                      'Cache-Control': 'max-age=0', 
                      'Origin': 'https://signon.telstra.com', 
                      'Upgrade-Insecure-Requests': '1', 
                      'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36', 
                      'Content-Type': 'application/x-www-form-urlencoded', 
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
                      'Referer': 'https://signon.telstra.com/federation/saml2?SPID=telstramedia', 
                      'Accept-Encoding': 'gzip, deflate', 
                      'Accept-Language': 'en-AU,en-US;q=0.8', 
                      'X-Requested-With': 'au.com.netball'}
                        
OFFERS_URL = 'https://api.telstra.com/v1/media-products/catalogues/media/offers?category=netball'

HUB_URL = 'http://hub.telstra.com.au/sp2017-netball-app'

MEDIA_ORDER_HEADERS = {'Content-Type': 'application/json', 
                       'Accept': 'application/json, text/plain, */*', 
                       'Host': 'api.telstra.com', 
                       'Connection': 'keep-alive', 
                       'Origin': 'https://hub.telstra.com.au',
                       'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36', 
                       'Accept-Encoding': 'gzip, deflate', 
                       'Accept-Language': 'en-AU,en-US;q=0.8', 
                       'X-Requested-With': 'au.com.netball'}
                        
MEDIA_ORDER_URL = 'https://api.telstra.com/v1/media-commerce/orders'

MEDIA_ORDER_JSON = '{{"serviceId":"{0}","serviceType":"MSISDN","offer":{{"id":"{1}"}},"pai":"{2}"}}'