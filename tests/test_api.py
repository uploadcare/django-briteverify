# coding: utf-8
import mock

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from django.core.exceptions import ValidationError
from requests.exceptions import HTTPError

from django_briteverify.api import check_email, ENTRY_POINT, TIMEOUT


EXAMPLE_API_RESPONSE = {
    'status': 'invalid',
    'account': 'test',
    'error': 'Email domain invalid',
    'disposable': False,
    'domain': 'test.ru',
    'connected': None,
    'role_address': False,
    'address': 'test@test.ru',
    'duration': 0.010371642,
    'error_code': 'email_domain_invalid'
}

BRITEVERIFY_API_KEY = 'some-key'

DEFAULT_RESULT = dict(valid=True, disposable=False)


@mock.patch('django_briteverify.api.settings')
@mock.patch('django_briteverify.api.session.get')
@mock.patch('django_briteverify.api.logger.exception')
class CheckEmailTestCase(unittest.TestCase):
    example_email = EXAMPLE_API_RESPONSE['address']

    def test_checking_disable(self, logger_exception, get, settings):
        settings.BRITEVERIFY_API_KEY = None
        self.assertDictEqual(DEFAULT_RESULT,
                             check_email(self.example_email))
        self.assertFalse(get.called)

    def test_request_doing_with_right_params(self, logger_exception, get,
                                             settings):
        settings.BRITEVERIFY_API_KEY = BRITEVERIFY_API_KEY
        check_email(self.example_email)
        get.assert_called_with(
            ENTRY_POINT,
            data={'address': self.example_email,
                  'apikey': BRITEVERIFY_API_KEY},
            timeout=TIMEOUT)

    def test_checking_network_error(self, logger_exception, get, settings):
        get.side_effect = HTTPError
        settings.BRITEVERIFY_API_KEY = BRITEVERIFY_API_KEY
        self.assertDictEqual(DEFAULT_RESULT,
                             check_email(self.example_email))
        self.assertTrue(get.called)
        logger_exception.assert_called_with('Briteverify service error.')

    def test_invalid_json_data(self, logger_exception, get, settings):
        json_method = mock.MagicMock()
        json_method.side_effect = ValueError
        get.return_value.json = json_method
        settings.BRITEVERIFY_API_KEY = BRITEVERIFY_API_KEY

        self.assertDictEqual(DEFAULT_RESULT,
                             check_email(self.example_email))
        self.assertTrue(get.called)
        self.assertTrue(json_method.called)
        logger_exception.assert_called_with(
            'Briteverify service error. No json received.')

    def test_bad_json_structure(self, logger_exception, get, settings):
        json_method = mock.MagicMock()
        json_method.return_value = dict()
        get.return_value.json = json_method
        settings.BRITEVERIFY_API_KEY = BRITEVERIFY_API_KEY

        self.assertDictEqual(DEFAULT_RESULT,
                             check_email(self.example_email))
        self.assertTrue(get.called)
        self.assertTrue(json_method.called)

        logger_exception.assert_called_with(
            'Briteverify service error. Bad json data: %r',
            json_method.return_value)

    def test_email_not_valid(self, logger_exception, get, settings):
        json_method = mock.MagicMock()
        json_method.return_value = dict(EXAMPLE_API_RESPONSE)
        get.return_value.json = json_method
        settings.BRITEVERIFY_API_KEY = BRITEVERIFY_API_KEY

        self.assertDictEqual(dict(DEFAULT_RESULT, valid=False),
                             check_email(self.example_email))
        self.assertTrue(get.called)
        self.assertTrue(json_method.called)
        self.assertFalse(logger_exception.called)

    def test_email_disposable(self, logger_exception, get, settings):
        json_method = mock.MagicMock()
        json_method.return_value = dict(EXAMPLE_API_RESPONSE,
                                        disposable=True, status='valid')
        get.return_value.json = json_method
        settings.BRITEVERIFY_API_KEY = BRITEVERIFY_API_KEY

        self.assertDictEqual(dict(DEFAULT_RESULT, disposable=True),
                             check_email(self.example_email))
        self.assertTrue(get.called)
        self.assertTrue(json_method.called)
        self.assertFalse(logger_exception.called)

    def test_email_valid(self, logger_exception, get, settings):
        json_method = mock.MagicMock()
        json_method.return_value = dict(EXAMPLE_API_RESPONSE,
                                        disposable=False, status='valid')
        get.return_value.json = json_method
        settings.BRITEVERIFY_API_KEY = BRITEVERIFY_API_KEY

        self.assertDictEqual(DEFAULT_RESULT, check_email(self.example_email))
        self.assertTrue(get.called)
        self.assertTrue(json_method.called)
        self.assertFalse(logger_exception.called)
