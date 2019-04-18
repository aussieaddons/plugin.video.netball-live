# flake8: noqa

NAME = 'Netball Live'
ADDON_ID = 'plugin.video.netball-live'

GITHUB_API_URL = 'https://api.github.com/repos/glennguy/plugin.video.netball-live'
ISSUE_API_URL = GITHUB_API_URL + '/issues'
ISSUE_API_AUTH = 'eGJtY2JvdDo1OTQxNTJjMTBhZGFiNGRlN2M0YWZkZDYwZGQ5NDFkNWY4YmIzOGFj'
GIST_API_URL = 'https://api.github.com/gists'

MAX_LIVEQUAL = 4
MAX_REPLAYQUAL = 7

# XML template to insert username and password into
LOGIN_DATA ='<Subscriber><Type>TDI</Type><User>{0}</User><Password>{1}</Password><Email>{0}</Email><AdobeCheckResult>0</AdobeCheckResult></Subscriber>'

# url used to request ooyala token
EMBED_TOKEN_URL ='https://signon-league-net.yinzcam.com/subscription/videotoken?application=NET_LEAGUE&ff=mobile&mnc=0&app_version=2.1.3&carrier=&version=5.6&width=1080&height=1776&os_version=6.0&mcc=0&application=NET_LEAGUE&embed_code={0}&ycurl_version=1&os=Android'

# url used to request playlist
AUTH_URL = 'http://player.ooyala.com/sas/player_api/v2/authorization/embed_code/{0}/{1}?device=html5&domain=http%3A%2F%2Fwww.ooyala.com&embedToken={2}&supportedFormats=m3u8'

# main url for xml that contains metadata for other non-live videos            
XML_URL = 'http://app-league-net.yinzcam.com/V1/Media/LongList?carrier=&height=1776&ycurl_version=1&os=Android&platform=Android&ff=mobile&mnc=0&app_version=2.4.0&mode=SUPER_NETBALL&version=5.7&width=1080&os_version=7.1.2&mcc=0&application=NET_LEAGUE'

# xml for replay videos
REPLAY_URL = 'http://app-league-net.yinzcam.com/V1/Media/TaggedList/card/matchreplays?carrier=&height=1776&ycurl_version=1&os=Android&platform=Android&ff=mobile&mnc=0&app_version=2.4.0&mode=SUPER_NETBALL&version=5.7&width=1080&os_version=7.1.2&mcc=0&application=NET_LEAGUE'          

# url for xml that contains match scores
SCORE_URL = 'http://app-league-net.yinzcam.com/V1/Game/Scores/?carrier=&height=1776&ycurl_version=1&os=Android&platform=Android&ff=mobile&mnc=0&app_version=2.4.0&mode=SUPER_NETBALL&version=5.7&width=1080&os_version=7.1.2&mcc=0&application=NET_LEAGUE'

# index of android app homepage - has current round game id's
INDEX_URL = 'http://app-league-net.yinzcam.com/V1/Home/Index?carrier=&height=1776&ycurl_version=1&os=Android&platform=Android&ff=mobile&mnc=0&app_version=2.4.0&mode=SUPER_NETBALL&version=5.7&width=1080&os_version=7.1.2&mcc=0&application=NET_LEAGUE'

# Score and team names for upcoming games
BOX_URL = 'http://app-league-net.yinzcam.com/V1/Game/Box/{0}?carrier=&height=1776&ycurl_version=1&os=Android&platform=Android&ff=mobile&mnc=0&app_version=2.4.0&mode=SUPER_NETBALL&version=5.7&width=1080&os_version=7.1.2&mcc=0&application=NET_LEAGUE'

# used to get metadata for playing live matches
LIVE_MEDIA_URL = 'http://app-league-net.yinzcam.com/V1/Media/Video/{0}?carrier=&height=1776&ycurl_version=1&os=Android&platform=Android&ff=mobile&mnc=0&app_version=2.4.0&mode=SUPER_NETBALL&version=5.7&width=1080&os_version=7.1.2&mcc=0&application=NET_LEAGUE'

# used for HDS metadata retrieval
SMIL_URL = "http://player.ooyala.com/nuplayer?embedCode={0}"

# ooyala provider indentifier code used in contructing request uris            
PCODE = 'BudDUxOt2GEh8L5PMMpcbz1wJFwm'          

CATEGORIES = {'1 Live Matches': 'livematches',
              '2 Full Match Replays': 'MatchReplays',
              '3 Match Highlights': 'MatchHighlights',
              '4 Features': 'Features',
              '5 Settings': 'settings'}

# New auth config for 2017

USER_AGENT_LONG = 'Mozilla/5.0 (Linux; Android 6.0; HTC One_M8 Build/MRA58K.H15; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/56.0.2924.87 Mobile Safari/537.36'

NEW_LOGIN_DATA1 = '<TicketRequest><Anonymous><AppId>NET_LEAGUE</AppId><VendorId>{adid}</VendorId><InstallId>{deviceid}</InstallId></Anonymous></TicketRequest>'

NEW_LOGIN_DATA2 = '<Subscriber><Type>TOKEN</Type><User>{0}</User></Subscriber>'

STATUS_URL = 'https://signon-league-net.yinzcam.com/subscription/status?application=NET_LEAGUE'

YINZCAM_AUTH_URL = 'https://signon-league-net.yinzcam.com/ticket?mnc=0&ff=mobile&app_version=2.1.3&carrier=&version=5.6&height=1776&width=1080&mcc=0&application=NET_LEAGUE&ycurl_version=1&os=Android'

YINZCAM_AUTH_URL2 = 'https://signon-league-net.yinzcam.com/telstra/oneplace/url?application=NET_LEAGUE'

YINZCAM_AUTH_HEADERS = {'Content-Type': 'application/xml', 
                        'Accept': 'application/json', 
                        'Connection': 'close',  
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; HTC One_M8 Build/MRA58K.H15)', 
                        'Accept-Encoding': 'gzip'}

SIGNON_HEADERS = {'Connection': 'keep-alive', 
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
                        
OFFERS_URL = 'https://tapi.telstra.com/v1/media-products/catalogues/media/offers'

HUB_URL = 'http://hub.telstra.com.au/sp2017-netball-app'

SSO_URL = 'https://tapi.telstra.com/v1/sso/auth'

SSO_PARAMS = {'redirect_uri': 'https://hub.telstra.com.au/offers/content/cached/callback.html',
              'response_type': 'id_token token',
              'scope': 'openid email profile phone telstra.user.sso.profile'}
              
SSO_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'en-AU,en-US;q=0.9',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': USER_AGENT_LONG,
               'X-Requested-With': 'au.com.netball'}

SPC_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'en-AU,en-US;q=0.9',
               'User-Agent': USER_AGENT_LONG,
               'X-Requested-With': 'au.com.netball'}

MEDIA_ORDER_HEADERS = {'Content-Type': 'application/json', 
                       'Accept': 'application/json, text/plain, */*', 
                       'Connection': 'keep-alive', 
                       'Origin': 'https://hub.telstra.com.au',
                       'User-Agent': USER_AGENT_LONG, 
                       'Accept-Encoding': 'gzip, deflate', 
                       'Accept-Language': 'en-AU,en-US;q=0.8', 
                       'X-Requested-With': 'au.com.netball'}
                        
MEDIA_ORDER_URL = 'https://tapi.telstra.com/v1/media-commerce/orders'

MEDIA_ORDER_JSON = '{{"serviceId":"{0}","serviceType":"MSISDN","offer":{{"id":"{1}"}},"pai":"{2}"}}'

YINZ_CALLBACK_URL = 'https://signon-league-net.yinzcam.com/telstra/oneplace/callback/NET_LEAGUE?type=SportPassConfirmation&statusCode=200&tpUID={0}'
