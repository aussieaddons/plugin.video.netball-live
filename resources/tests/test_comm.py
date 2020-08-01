from __future__ import absolute_import, unicode_literals

import io
import os

import responses

import testtools

import resources.lib.comm as comm
import resources.lib.config as config

try:
    import mock
except ImportError:
    import unittest.mock as mock


class CommTests(testtools.TestCase):

    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/json/BC_EDGE.json'), 'rb') as f:
            self.BC_EDGE_JSON = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/BOX.xml'), 'rb') as f:
            self.BOX_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/HOME.xml'), 'rb') as f:
            self.HOME_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/INDEX.xml'), 'rb') as f:
            self.INDEX_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/LONGLIST.xml'), 'rb') as f:
            self.LONGLIST_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/SCORE_INTERNATIONAL.xml'),
                  'rb') as f:
            self.SCORE_INTERNATIONAL_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/SCORE_SUPER.xml'), 'rb') as f:
            self.SCORE_SUPER_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/TAGGEDLIST_HIGHLIGHTS.xml'),
                  'rb') as f:
            self.TAGGEDLIST_HIGHLIGHTS_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/TAGGEDLIST_REPLAY.xml'),
                  'rb') as f:
            self.TAGGEDLIST_REPLAY_XML = io.BytesIO(f.read()).read()

    @responses.activate
    def test_fetch_url(self):
        responses.add(responses.GET, 'http://foo.bar/',
                      body=u'Hello World', status=200)
        observed = comm.fetch_url('http://foo.bar/').decode('utf-8')
        self.assertEqual(observed, 'Hello World')

    @responses.activate
    def test_list_matches_replays(self):
        for mode in ['SUPER_NETBALL', 'INTERNATIONAL']:
            responses.add(responses.GET,
                          config.TAGGEDLIST_REPLAY_URL.format(mode=mode),
                          body=self.TAGGEDLIST_REPLAY_XML, status=200)
        observed = comm.list_matches({'category': 'Match Replays'})
        self.assertEqual(400, len(observed))  # 200 * 2
        self.assertEqual('1647221321927449747', observed[4].video_id)

    @responses.activate
    def test_list_matches_highlights(self):
        for mode in ['SUPER_NETBALL', 'INTERNATIONAL']:
            responses.add(responses.GET,
                          config.LONGLIST_URL.format(mode=mode),
                          body=self.TAGGEDLIST_HIGHLIGHTS_XML, status=200)
        observed = comm.list_matches({'category': 'MatchHighlights'})
        self.assertEqual(200, len(observed))  # 100 * 2
        self.assertEqual('1647215383533280406', observed[4].video_id)

    @responses.activate
    def test_get_score(self):
        responses.add(responses.GET,
                      config.SCORE_URL.format(mode='INTERNATIONAL'),
                      body=self.SCORE_INTERNATIONAL_XML, status=200)
        responses.add(responses.GET,
                      config.SCORE_URL.format(mode='SUPER_NETBALL'),
                      body=self.SCORE_SUPER_XML, status=200)
        observed = comm.get_score('111080104')
        self.assertEqual('[COLOR yellow]25 - 30[/COLOR]', observed)

    @responses.activate
    def test_get_index(self):
        for mode in ['SUPER_NETBALL', 'INTERNATIONAL']:
            responses.add(responses.GET,
                          config.INDEX_URL.format(mode=mode),
                          body=self.INDEX_XML, status=200)
        observed = comm.get_index()
        self.assertEqual(['107250301', '107250301'], observed)

    @mock.patch('resources.lib.comm.get_index', lambda: ['107250301'])
    @responses.activate
    def test_find_live_matches(self):
        responses.add(responses.GET,
                      config.BOX_URL.format('107250301'),
                      body=self.BOX_XML, status=200)
        observed = comm.find_live_matches()
        #  convert to and from to remove xml shebang
        expected = comm.ET.tostring(comm.ET.fromstring(self.BOX_XML))
        self.assertEqual(expected, comm.ET.tostring(observed[0]))

    @mock.patch('resources.lib.comm.get_tz_delta', lambda: 11)
    @responses.activate
    def test_get_upcoming(self):
        responses.add(responses.GET,
                      config.SCORE_URL.format(mode='INTERNATIONAL'),
                      body=self.SCORE_INTERNATIONAL_XML, status=200)
        responses.add(responses.GET,
                      config.SCORE_URL.format(mode='SUPER_NETBALL'),
                      body=self.SCORE_SUPER_XML, status=200)
        observed = comm.get_upcoming()
        #  convert to and from to remove xml shebang
        expected = ('[COLOR red]Upcoming:[/COLOR] {0} v {1} - '
                    '[COLOR yellow]{2}[/COLOR]').format(
            'Melbourne Vixens', 'Queensland Firebirds',
            'Saturday 2 May @ 4:00 PM')
        self.assertEqual(expected, observed[0].title)

    @responses.activate
    def test_get_stream_url(self):
        responses.add(responses.GET,
                      config.BC_URL.format('123', '456'),
                      body=self.BC_EDGE_JSON, status=200)
        observed = comm.get_stream_url({'account_id': '123',
                                        'video_id': '456',
                                        'policy_key': '789'})
        expected = 'https://foo.bar/video.m3u8'
        self.assertEqual(expected, observed)
