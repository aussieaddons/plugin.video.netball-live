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

import xml.etree.ElementTree as ET
import classes
import xbmc
import urllib2
import utils
import config
import time
import datetime


def list_matches(params, live=False):
    """ go through our xml file and retrive all we need to pass to kodi"""
    if live:
        return list_live_matches()
    url = config.XML_URL
    utils.log("Fetching URL: {0}".format(url))
    response = urllib2.urlopen(url)
    data = response.read()
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
            if content_type != params['category']:
                continue
            
            g = classes.game()       
            g.title = gm.find('Title').text.encode('ascii', 'replace')
            if gm.find('Description') is not None:
                g.desc = gm.find('Description').text.encode('ascii', 'replace')
            g.video_id = gm.find('Video').attrib['Id']
            g.live = gm.find('LiveNow').text
            g.thumb = gm.find('FullImageUrl').text
            g.time = utils.ensure_ascii(gm.find('Date').text)
            listing.append(g)
    return listing

def list_live_matches():
    """ go through list of xml objects and return listing of game objects"""
    tree_list = find_live_matches()
    listing = []
    for tree in tree_list:
        g = classes.game()
        home = tree.find('HomeTeam').attrib['FullName']
        away = tree.find('AwayTeam').attrib['FullName']
        match_id = tree.find('Id').text
        score = get_score(match_id)
        title = '[COLOR green][LIVE NOW][/COLOR] {0} v {1} {2}'
        g.title = title.format(home, away, score)
        media_url = tree.find('WatchButton').find('URL').text
        video_id = media_url[media_url.find('Id=')+3:]
        media_tree = get_media_tree(video_id)
        g.video_id = media_tree.find('Video').attrib['Id']
        g.live = 'true'
        listing.append(g)
    return listing
        

def get_media_tree(video_id):
    """ get xml with info about live match"""
    url = config.LIVE_MEDIA_URL.format(video_id)
    utils.log("Fetching URL: {0}".format(url))
    response = urllib2.urlopen(url)
    tree = ET.fromstring(response.read())
    return tree.find('Item')

def get_index():
    """ get index of current round's games so we can find the 'box' URL
        and make a list of game ids,
    """
    utils.log("Fetching URL: {0}".format(config.INDEX_URL))
    response = urllib2.urlopen(config.INDEX_URL)
    tree = ET.fromstring(response.read())
    listing = []
    for elem in tree.find('HeadlineGames'):
        listing.append(elem.attrib['Id'])
    return listing

def find_live_matches():
    """ returns a list of ElementTree objects to parse for live matches
    """
    id_list = get_index()
    listing = []
    for game_id in id_list:
        url = config.BOX_URL.format(game_id)
        utils.log("Fetching URL: {0}".format(url))
        response = urllib2.urlopen(url)
        tree = ET.fromstring(response.read())
        if tree.find('WatchButton') is not None:
            listing.append(tree)
    return listing

def get_upcoming():
    """ similar to get_score but this time we are searching for upcoming live
        match info"""
    utils.log("Fetching URL: {0}".format(config.SCORE_URL))
    response = urllib2.urlopen(config.SCORE_URL)
    tree = ET.fromstring(response.read())
    listing = []
    
    for elem in tree.findall("Day"):
        for subelem in elem.findall("Game"):
            if subelem.find('GameState').text == 'Full Time':
                continue
            g = classes.game()
            home = subelem.find('HomeTeam').attrib['FullName']
            away = subelem.find('AwayTeam').attrib['FullName']
            timestamp = subelem.find('Timestamp').text
            #convert zulu to local time
            airtime = utils.get_airtime(timestamp)
            title = ('[COLOR red]Upcoming:[/COLOR] '
                     '{0} v {1} - [COLOR yellow]{2}[/COLOR]')
            g.title = title.format(home, away, airtime)
            g.dummy = True
            listing.append(g)
    return listing

def get_score(match_id):
    """fetch score xml and return the scores for corresponding match IDs"""
    utils.log("Fetching URL: {0}".format(config.SCORE_URL))
    response = urllib2.urlopen(config.SCORE_URL)
    tree = ET.fromstring(response.read())

    for elem in tree.findall("Day"):
        for subelem in elem.findall("Game"):     
            if subelem.attrib['Id'] == str(match_id):
                home_score =  str(subelem.find('HomeTeam').attrib['Score'])
                away_score = str(subelem.find('AwayTeam').attrib['Score'])
                return '[COLOR yellow]{0} - {1}[/COLOR]'.format(
            home_score,away_score)