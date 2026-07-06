from django.test import TestCase
from django.contrib.auth.models import User

class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
    
            email="nicole@example.com",
            password="password123"
        )

        
        self.assertEqual(user.email, "nicole@example.com")
        self.assertTrue(user.check_password("password123"))