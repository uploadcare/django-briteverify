# coding: utf-8
import mock

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from django import forms
from django.core.exceptions import ValidationError

from django_briteverify.forms import BriteverifyFormMixin


class TestForm(BriteverifyFormMixin, forms.Form):
    email = forms.EmailField(required=False)
    name = forms.CharField()


@mock.patch('django_briteverify.forms.check_email')
class FormTestCase(unittest.TestCase):
    def test_not_called_when_email_is_none(self, check_email):
        form = TestForm({'name': 'name'})

        self.assertTrue(form.is_valid())
        self.assertFalse(check_email.called)

    def test_not_called_with_errors(self, check_email):
        form = TestForm()

        self.assertFalse(form.is_valid())
        self.assertFalse(check_email.called)

    def test_invalid_status(self, check_email):
        check_email.return_value = {'valid': False}

        form = TestForm({'name': 'name', 'email': 'invalid@test.ru'})

        self.assertFalse(form.is_valid())
        self.assertTrue(check_email.called)
        self.assertEqual(form.errors['email'],
                         [form.error_messages['invalid_email']])

    def test_is_disposable(self, check_email):
        check_email.return_value = {'valid': True, 'disposable': True}

        form = TestForm({'name': 'name', 'email': 'disposable@test.ru'})

        self.assertFalse(form.is_valid())
        self.assertTrue(check_email.called)
        self.assertEqual(form.errors['email'],
                         [form.error_messages['disposable_email']])

    def test_form_is_valid(self, check_email):
        check_email.return_value = {'valid': True, 'disposable': False}

        form = TestForm({'name': 'name', 'email': 'valid@test.ru'})

        self.assertTrue(form.is_valid())
        self.assertTrue(check_email.called)
