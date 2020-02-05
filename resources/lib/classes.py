import datetime
import time
import unicodedata
from builtins import str
from collections import OrderedDict

from future.moves.urllib.parse import parse_qsl, quote_plus, unquote_plus


class Video(object):
    """
    object that contains all the info for a particular match
    """
    def __init__(self):
        self.video_id = None
        self.policy_key = None
        self.account_id = None
        self.thumb = None
        self.title = None
        self.live = None
        self.time = None
        self.desc = None
        self.dummy = None
        self.start_date = None
        self.home = None
        self.away = None

    def make_kodi_url(self):
        d_original = OrderedDict(
            sorted(self.__dict__.items(), key=lambda x: x[0]))
        d = d_original.copy()
        for key, value in d_original.items():
            if not value:
                d.pop(key)
                continue
            if isinstance(value, str):
                d[key] = unicodedata.normalize(
                    'NFKD', value).encode('ascii', 'ignore').decode('utf-8')
        url = ''
        for key in d.keys():
            if isinstance(d[key], (str, bytes)):
                val = quote_plus(d[key])
            else:
                val = d[key]
            url += '&{0}={1}'.format(key, val)
        return url

    def parse_kodi_url(self, url):
        params = dict(parse_qsl(url))
        self.parse_params(params)

    def parse_params(self, params):
        for item in params.keys():
            setattr(self, item, unquote_plus(params[item]))
        if self.start_date:  # quote date to preserve '+'
            setattr(self, 'start_date', quote_plus(self.start_date))

    def get_live_title(self):
        if self.home and self.away:
            return '[COLOR green][LIVE NOW][/COLOR] {0} v {1}'.format(
                self.home, self.away)

    def get_tz_delta(self):
        delta = ((time.mktime(time.localtime()) -
                  time.mktime(time.gmtime())) / 3600)
        if time.localtime().tm_isdst:
            delta += 1
        return delta

    def get_airtime(self):
        try:
            delta = self.get_tz_delta()
            ts_format = "%Y-%m-%dT%H:%M:%SZ"
            ts = datetime.datetime.fromtimestamp(
                time.mktime(time.strptime(
                    unquote_plus(self.start_date), ts_format)))
            ts += datetime.timedelta(hours=delta)
            return ts.strftime("%A %d %b @ %I:%M %p").replace(' 0', ' ')
        except OverflowError:
            return ts