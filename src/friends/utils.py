from friends.models import FriendRequest

def friend_request_exists(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, pending=True)
    except FriendRequest.DoesNotExist:
        return False

