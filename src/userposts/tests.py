from django.test import RequestFactory, TestCase
from userposts.views import home_page
from users.models import User

class HomePageViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='albert@gmail.com', username='albert', password='albertpassword')    

    def test_home_page_view(self):
        request = self.factory.get('')
        request.user = self.user
        response = home_page(request)
        self.assertEqual(response.status_code, 200)