from __future__ import absolute_import, unicode_literals

import io
import os
try:
    import mock
except ImportError:
    import unittest.mock as mock

import responses

import testtools

import resources.lib.config as config
import resources.lib.stream_auth as stream_auth


class StreamAuthTests(testtools.TestCase):
    @classmethod
    def setUpClass(self):
        cwd = os.path.join(os.getcwd(), 'resources/tests')
        with open(os.path.join(cwd, 'fakes/xml/VIDEO_TOKEN.xml'),
                  'rb') as f:
            self.VIDEO_TOKEN_XML = io.BytesIO(f.read()).read()
        with open(os.path.join(cwd, 'fakes/xml/VIDEO_TOKEN_FAIL.xml'),
                  'rb') as f:
            self.VIDEO_TOKEN_FAIL_XML = io.BytesIO(f.read()).read()

    @mock.patch('resources.lib.stream_auth.cache.delete')
    def test_clear_ticket(self, mock_delete):
        stream_auth.clear_ticket()
        mock_delete.assert_called_with('NETBALLTICKET')

    @mock.patch('resources.lib.stream_auth.cache.get')
    def test_get_user_ticket_cached(self, mock_ticket):
        mock_ticket.return_value = 'foobar123456'
        observed = stream_auth.get_user_ticket()
        self.assertEqual('foobar123456', observed)

    @mock.patch(
        'resources.lib.stream_auth.telstra_auth.TelstraAuth.get_free_token')
    @mock.patch('resources.lib.stream_auth.addon.getSetting')
    @mock.patch('resources.lib.stream_auth.cache.get')
    def test_get_user_ticket_free(self, mock_ticket, mock_sub_type,
                                  mock_token):
        mock_ticket.return_value = ''
        mock_sub_type.return_value = '0'
        mock_token.return_value = 'foobar456789'
        observed = stream_auth.get_user_ticket()
        self.assertEqual('foobar456789', observed)
