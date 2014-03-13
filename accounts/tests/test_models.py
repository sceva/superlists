from django.contrib.auth import get_user_model
from django.test import TestCase

__author__ = 's'  # created on 3/13/14.


User = get_user_model()

class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='a@b.com')
        user.full_clean() # should not raise

    def test_email_is_primary_key(self):
        user = User()
        self.assertFalse(hasattr(user, 'id'))
