from django.test import RequestFactory, TestCase
from userposts.views import home_page
from users.models import User

class UsersViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_user(self):
        user = User.objects.create_user(email='albert@gmail.com', username='albert', password='albertpassword')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'albert@gmail.com')
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)