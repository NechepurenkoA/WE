from .models import FriendRequest, User


class FriendRequestServices(object):
    """Сервися для отправки/принятия запросов дружбы."""

    def __init__(self, request):
        self.request = request

    def send_friend_request(self, user: User) -> None:
        instance = FriendRequest.objects.create(
            sender=self.request.user,
            receiver=user,
            status=1,
        )
        instance.save()
        return None

    def cancel_friend_request(self, user: User) -> None:
        FriendRequest.objects.filter(sender=self.request.user, receiver=user).delete()
        return None

    # WIP
    def accept_friend_request(self, user: User) -> None:
        return None

    def decline_friend_request(self, user: User) -> None:
        return None
