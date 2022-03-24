from django.test import RequestFactory, TestCase
from friends.models import FriendList, FriendRequest
from users.models import User
from friends.views import accept_friend_request

class FriendRequestTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(email='albert@gmail.com', username='albert', password='albertpassword')
        FriendList.objects.create(user=self.user1)
        self.user2 = User.objects.create_user(email='candice@gmail.com', username='candice', password='candicepassword')
        FriendList.objects.create(user=self.user2)

    def test_create_request(self):
        request = FriendRequest(sender=self.user1, receiver=self.user2)
        self.assertIsInstance(request, FriendRequest)
        self.assertEqual(request.sender, self.user1)
        self.assertEqual(request.receiver, self.user2)

    def test_accept_request(self):
        friend_request = FriendRequest(sender=self.user1, receiver=self.user2)
        request = self.factory.get(f'friend/accept_friend_request/{friend_request.pk}')
        request.user = self.user2
        response = accept_friend_request(request)
        self.assertEqual(response.status_code, 200)