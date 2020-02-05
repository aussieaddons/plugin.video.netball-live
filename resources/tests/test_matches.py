from __future__ import absolute_import, unicode_literals

import datetime
import io
import os
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

#  https://blog.xelnor.net/python-mocking-datetime/
real_datetime_class = datetime.datetime


def mock_datetime_now(target, dt):
    class DatetimeSubclassMeta(type):
        @classmethod
        def __instancecheck__(mcs, obj):
            return isinstance(obj, real_datetime_class)

    class BaseMockedDatetime(real_datetime_class):
        @classmethod
        def now(cls, tz=None):
            return target.replace(tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return target

    MockedDatetime = DatetimeSubclassMeta(
        str('datetime'), (BaseMockedDatetime,), {})
    return mock.patch.object(dt, 'datetime', MockedDatetime)


class MenusTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/xml/BOX.xml'), 'rb') as f:
            self.BOX_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/INDEX.xml'), 'rb') as f:
            self.INDEX_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/SCORE_INTERNATIONAL.xml'),
                  'rb') as f:
            self.SCORE_INTERNATIONAL_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/SCORE_SUPER.xml'), 'rb') as f:
            self.SCORE_SUPER_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/TAGGEDLIST_REPLAY.xml'),
                  'rb') as f:
            self.TAGGEDLIST_REPLAY_XML = io.BytesIO(f.read()).read()

    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.soccer-live/', '2',
                 '?action=listcategories&category=MatchReplays',
                 'resume:false'])
    @responses.activate
    def test_make_matches_list(self, mock_listitem):
        mock_listitem.side_effect = fakes.FakeListItem
        mock_plugin = fakes.FakePlugin()
        responses.add(responses.GET,
                      config.TAGGEDLIST_REPLAY_URL,
                      body=self.TAGGEDLIST_REPLAY_XML, status=200)
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import resources.lib.matches as matches
            matches.make_matches_list({'category': 'MatchReplays'})
            expected_title = '2019 Round 11: Giants v Firebirds (Replay)'
            expected = fakes.FakeListItem(expected_title)
            expected.setThumbnailImage('example.jpg')
            expected.setIconImage('example.jpg')
            expected.setInfo('video', {'plot': expected_title,
                                       'plotoutline': expected_title})
            expected.setProperty('IsPlayable', 'true')
            observed = mock_plugin.directory[0].get('listitem')
            for attrib in vars(observed):
                self.assertEqual(getattr(expected, attrib),
                                 getattr(observed, attrib))

    @testtools.skip('Need live video data to complete test')
    @mock.patch('xbmcgui.ListItem')
    @mock.patch('sys.argv',
                ['plugin://plugin.video.soccer-live/', '2',
                 '?action=listcategories&category=livematches',
                 'resume:false'])
    @responses.activate
    def test_make_matches_list_live(self, mock_listitem):
        mock_listitem.side_effect = fakes.FakeListItem
        mock_plugin = fakes.FakePlugin()
        responses.add(responses.GET,
                      config.SCORE_URL.format(mode='INTERNATIONAL'),
                      body=self.SCORE_INTERNATIONAL_XML, status=200)
        responses.add(responses.GET,
                      config.SCORE_URL.format(mode='SUPER_NETBALL'),
                      body=self.SCORE_SUPER_XML, status=200)
        responses.add(responses.GET,
                      config.BOX_URL.format('107250301'),
                      body=self.BOX_XML, status=200)
        responses.add(responses.GET,
                      config.INDEX_URL,
                      body=self.INDEX_XML, status=200)
        with mock.patch.dict('sys.modules', xbmcplugin=mock_plugin):
            import resources.lib.matches as matches
            matches.make_matches_list({'category': 'livematches'})
            expected_title = '2019 Round 11: Giants v Firebirds (Replay)'
            expected = fakes.FakeListItem(expected_title)
            expected.setThumbnailImage('example.jpg')
            expected.setIconImage('example.jpg')
            expected.setInfo('video', {'plot': expected_title,
                                       'plotoutline': expected_title})
            expected.setProperty('IsPlayable', 'true')
            observed = mock_plugin.directory[0].get('listitem')
            for attrib in vars(observed):
                self.assertEqual(getattr(expected, attrib),
                                 getattr(observed, attrib))
