import logging
from unittest.mock import patch
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.authentication import (
    PERSONA_VERIFY_URL, PersonaAuthenticationBackend
)

User = get_user_model()

@patch('accounts.authentication.requests.post')
class AuthenticationTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        user = User(email='other@user.com')
        user.username = 'otheruser'
        user.save()

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data={'assertion': 'an assertion', 'audience': settings.DOMAIN}
        )

    def test_returns_none_if_response_errors(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        actual_user = User.objects.create(email='a@b.com')
        found_user = self.backend.authenticate('an assertion')
        self.assertEqual(actual_user, found_user)

    def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        found_user = self.backend.authenticate('an assertion')
        new_user = User.objects.get(email='a@b.com')
        self.assertEqual(found_user, new_user)

    def test_logs_non_okay_responses_from_persona(self, mock_post):
        response_json = {
            'status': 'not okay', 'reason': 'eg, audience mismatch'
        }
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = response_json

        logger = logging.getLogger('accounts.authentication')
        with patch.object(logger, 'warning') as mock_log_warning:
            self.backend.authenticate('an assertion')

        mock_log_warning.assert_called_once_with(
            'Persona says no. Json was: {}'.format(response_json)
        )

    # this is an example of how to mock the Django ORM so we don't touch the database
class GetUserTest(TestCase):

    @patch('accounts.authentication.User.objects.get')
    def test_gets_user_from_ORM_using_email(self, mock_User_get):
        backend = PersonaAuthenticationBackend()
        found_user = backend.get_user('a@b.com')
        self.assertEqual(found_user, mock_User_get.return_value)
        mock_User_get.assert_called_once_with(email='a@b.com')

    @patch('accounts.authentication.User.objects.get')
    def test_returns_none_if_user_does_not_exist(self, mock_User_get):
        def raise_no_user_error(*_, **__):
            raise User.DoesNotExist()
        mock_User_get.side_effect = raise_no_user_error
        backend = PersonaAuthenticationBackend()

        self.assertIsNone(backend.get_user('a@b.com'))