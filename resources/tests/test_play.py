from __future__ import absolute_import, unicode_literals

import io
import json
import os
import re
import sys

try:
    import mock
except ImportError:
    import unittest.mock as mock

from future.moves.urllib.parse import parse_qsl, quote_plus

import responses

import testtools

import resources.lib.config as config
from resources.tests.fakes import fakes


def escape_regex(s):
    escaped = re.escape(s)
    return escaped.replace('\\{', '{').replace('\\}', '}')


class PlayTests(testtools.TestCase):
    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/BC_EDGE.json'), 'rb') as f:
            self.BC_EDGE_JSON = io.BytesIO(f.read()).read()
            with open(os.path.join(cwd, 'fakes/json/SIGN.json'), 'rb') as f:
                self.SIGN_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/json/VIDEO_TOKEN.json'),
                  'rb') as f:
            self.VIDEO_TOKEN_JSON = io.BytesIO(f.read()).read()

    @responses.activate
    @mock.patch('resources.lib.stream_auth.cache.get')
    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.nrl-live/',
                 '2',
                 '?action=listmatches&video_id=1647215572322985741'
                 '&account_id=6057984925001&'])
    def test_play_video(self, mock_listitem, mock_ticket):
        params = dict(parse_qsl(sys.argv[2][1:]))
        escaped_bc_url = re.escape(
            config.BC_URL).replace('\\{', '{').replace('\\}', '}')
        bc_url = re.compile(escaped_bc_url.format('.*', '.*'))
        responses.add(responses.GET,
                      bc_url,
                      body=self.BC_EDGE_JSON, status=200)
        mock_ticket.return_value = json.dumps({'pai': fakes.FAKE_UUID[0],
                                               'bearer': 'abc123'})
        mock_listitem.side_effect = fakes.FakeListItem

        mock_plugin = fakes.FakePlugin()
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import resources.lib.play as play
            play.play_video(params)
            self.assertEqual('https://foo.bar/video.m3u8',
                             mock_plugin.resolved[2].getPath())

    @responses.activate
    @mock.patch('resources.lib.stream_auth.cache.get')
    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.nrl-live/',
                 '2',
                 '?action=listmatches&account_id=6057994524001&live=true'
                 '&policy_key=BCpkADawqM0iZ1kHqDZmhGgwf0SHhCi1smeoD8j7dq'
                 'BuRKGB5dzhXBAPFe3Pfw5BPXW6FTSWBD9a_GCsbukIhk7e0r3P8Olh'
                 '6-tXCsDgNFKVlZm6Ca2UJza8Tt5TkTrIhPZ4mJUEIxc2y96M&title'
                 '=%5BCOLOR+green%5D%5BLIVE+NOW%5D%5B%2FCOLOR%5D+Adelaid'
                 'e+Thunderbirds+v+West+Coast+Fever+%5BCOLOR+yellow%5D6+'
                 '-+6%5B%2FCOLOR%5D&video_id=6112170884001'])
    def test_play_video_live(self, mock_listitem, mock_ticket):
        params = dict(parse_qsl(sys.argv[2][1:]))
        escaped_bc_url = re.escape(
            config.BC_URL).replace('\\{', '{').replace('\\}', '}')
        bc_url = re.compile(escaped_bc_url.format('.*', '.*'))
        responses.add(responses.GET,
                      bc_url,
                      body=self.BC_EDGE_JSON, status=200)
        responses.add(responses.GET,
                      config.MEDIA_AUTH_URL.format(video_id='6112170884001'),
                      body=self.VIDEO_TOKEN_JSON, status=200)
        responses.add(responses.GET,
                      config.SIGN_URL.format(
                          quote_plus('https://foo.bar/video.m3u8')),
                      body=self.SIGN_JSON, status=200)
        mock_ticket.return_value = json.dumps({'pai': fakes.FAKE_UUID[0],
                                               'bearer': 'abc123'})
        mock_listitem.side_effect = fakes.FakeListItem

        mock_plugin = fakes.FakePlugin()
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import resources.lib.play as play
            play.play_video(params)
            self.assertEqual('https://foo.bar/index.m3u8?signed',
                             mock_plugin.resolved[2].getPath())
