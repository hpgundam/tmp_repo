from django.test import TestCase

# Create your tests here.
from .models import validate_nickname


class UserModelTestCase(TestCase):

	def test_nickname(self):
		self.assertTrue(validate_nickname('a1242sdf2sdf'))
		self.assertFalse(validate_nickname('123sdf23sdf'))
		self.assertFalse(validate_nickname('a12se223#$#sdf'))



