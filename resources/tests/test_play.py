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

from future.moves.urllib.parse import parse_qsl

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
        with open(os.path.join(cwd, 'fakes/xml/VIDEO_TOKEN.xml'),
                  'rb') as f:
            self.VIDEO_TOKEN_XML = io.BytesIO(f.read()).read()

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
