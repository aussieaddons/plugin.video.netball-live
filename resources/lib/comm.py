import datetime
import json
import time
import xml.etree.ElementTree as ET

from aussieaddonscommon import session
from aussieaddonscommon import utils

from resources.lib import classes
from resources.lib import config


def get_airtime(timestamp):
    try:
        delta = ((time.mktime(time.localtime()) -
                 time.mktime(time.gmtime())) / 3600)
        if time.localtime().tm_isdst:
            delta += 1
        ts = datetime.datetime.fromtimestamp(
            time.mktime(time.strptime(timestamp[:-1], "%Y-%m-%dT%H:%M:%S")))
        ts += datetime.timedelta(hours=delta)
        return ts.strftime("%A %d %b @ %I:%M %p").replace(' 0', ' ')
    except OverflowError:
        return ''


def fetch_url(url, headers=None):
    """
    HTTP GET on url, remove byte order mark
    """
    with session.Session() as sess:
        if headers:
            sess.headers.update(headers)
        resp = sess.get(url)
        return resp.text.encode("utf-8")


def list_matches(params):
    """
    go through our xml file and retrive all we need to pass to kodi
    """
    category = params['category']
    if category == 'livematches':
        return list_live_matches()
    if category == 'MatchReplays':
        url = config.TAGGEDLIST_REPLAY_URL
    else:
        url = config.TAGGEDLIST_PROGRAM_URL.format(category)
    data = fetch_url(url)
    tree = ET.fromstring(data)
    listing = []
    for elem in tree.findall("MediaSection"):
        for gm in elem.findall('Item'):
            # remove items with no video eg. news articles
            if not gm.attrib['Type'] == 'V':
                continue
            # filter videos by category
            for metadata in gm.find('Metadata').findall('Data'):
                key = metadata.attrib['Key']
                if key == 'contentType':
                    content_type = metadata.attrib['Value']
            if content_type != category:
                continue

            v = classes.Video()
            v.title = utils.ensure_ascii(gm.find('Title').text)
            v.video_id = gm.find('Video').attrib['Id']
            v.account_id = gm.find('Video').attrib['AccountId']
            v.policy_key = gm.find('Video').attrib['PolicyKey']
            v.live = gm.find('LiveNow').text
            v.thumb = gm.find('FullImageUrl').text
            v.time = utils.ensure_ascii(gm.find('Date').text)
            listing.append(v)
    return listing


def list_live_matches():
    """
    go through list of xml objects and return listing of game objects
    """
    tree_list = find_live_matches()
    listing = []
    for tree in tree_list:
        v = classes.Video()
        home = tree.find('HomeTeam').attrib['FullName']
        away = tree.find('AwayTeam').attrib['FullName']
        match_id = tree.find('Id').text
        score = get_score(match_id)
        title = '[COLOR green][LIVE NOW][/COLOR] {0} v {1} {2}'
        v.title = title.format(home, away, score)
        media_url = tree.find('WatchButton').find('URL').text
        video_id = media_url[media_url.find('Id=')+3:]
        media_tree = get_media_tree(video_id)
        v.video_id = media_tree.find('Video').attrib['Id']
        v.live = 'true'
        listing.append(v)
    return listing


def get_media_tree(video_id):
    """
    get xml with info about live match
    """
    data = fetch_url(config.LIVE_MEDIA_URL.format(video_id))
    tree = ET.fromstring(data)
    return tree.find('Item')


def get_index():
    """
    get index of current round's games so we can find the 'box' URL
    and make a list of game ids,
    """
    data = fetch_url(config.INDEX_URL)
    tree = ET.fromstring(data)
    listing = []
    for elem in tree.find('HeadlineGames'):
        listing.append(elem.attrib['Id'])
    return listing


def find_live_matches():
    """
    returns a list of ElementTree objects to parse for live matches
    """
    id_list = get_index()
    listing = []
    for game_id in id_list:
        data = fetch_url(config.BOX_URL.format(game_id))
        tree = ET.fromstring(data)
        watch_button = tree.find('WatchButton')
        if watch_button:
            if watch_button.find('Title').text != 'WATCH REPLAY':
                listing.append(tree)
    return listing


def get_upcoming():
    """
    similar to get_score but this time we are searching for upcoming live
    match info
    """
    listing = []

    for mode in ['INTERNATIONAL', 'SUPER_NETBALL']:
        data = fetch_url(config.SCORE_URL.format(mode=mode))
        tree = ET.fromstring(data)

        for elem in tree.findall("Day"):
            for subelem in elem.findall("Game"):
                if subelem.find('GameState').text == 'Full Time':
                    continue
                v = classes.Video()
                home = subelem.find('HomeTeam').attrib['FullName']
                away = subelem.find('AwayTeam').attrib['FullName']
                timestamp = subelem.find('Timestamp').text
                # convert zulu to local time
                airtime = get_airtime(timestamp)
                title = ('[COLOR red]Upcoming:[/COLOR] '
                         '{0} v {1} - [COLOR yellow]{2}[/COLOR]')
                v.title = title.format(home, away, airtime)
                v.dummy = True
                listing.append(v)
    return listing


def get_score(match_id):
    """
    fetch score xml and return the scores for corresponding match IDs
    """
    for mode in ['INTERNATIONAL', 'SUPER_NETBALL']:
        data = fetch_url(config.SCORE_URL.format(mode=mode))
        tree = ET.fromstring(data)

        for elem in tree.findall("Day"):
            for subelem in elem.findall("Game"):
                if subelem.attrib['Id'] == str(match_id):
                    home_score = str(subelem.find('HomeTeam').attrib['Score'])
                    away_score = str(subelem.find('AwayTeam').attrib['Score'])
                    return '[COLOR yellow]{0} - {1}[/COLOR]'.format(
                        home_score, away_score)


def get_stream_url(params):
    bc_url = config.BC_URL.format(params.get('account_id'),
                                  params.get('video_id'))
    data = json.loads(
        fetch_url(bc_url, {'BCOV-POLICY': params.get('policy_key')}))
    src = None
    sources = data.get('sources')
    if len(sources) == 1:
        src = sources[0].get('src')
    else:
        for source in sources:
            ext_ver = source.get('ext_x_version')
            src = source.get('src')
            if ext_ver == '4' and src:
                if src.startswith('https'):
                    break
    if not src:
        utils.log(data.get('sources'))
        raise Exception('Unable to locate video source.')
    return str(src)
