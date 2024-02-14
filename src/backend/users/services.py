from .models import FriendRequest, Friendship, User


class FriendRequestServices(object):
    """Сервися для отправки/принятия запросов дружбы."""

    def __init__(self, request):
        self.request = request

    def send_friend_request(self, user: User) -> None:
        instance = FriendRequest.objects.create(
            sender=self.request.user,
            receiver=user,
        )
        instance.save()
        return None

    def cancel_friend_request(self, user: User) -> None:
        """Отменить отправленный запрос."""
        FriendRequest.objects.filter(
            sender_id=self.request.user.id,
            receiver_id=user.id,
        ).delete()
        return None

    def accept_friend_request(self, user: User) -> None:
        """Принятие запроса дружбы."""
        Friendship.objects.bulk_create(
            [
                Friendship(
                    current_user=self.request.user,
                    another_user=user,
                ),
                Friendship(
                    current_user=user,
                    another_user=self.request.user,
                ),
            ]
        )
        FriendRequest.objects.filter(
            sender_id=user.id, receiver_id=self.request.user.id
        ).delete()
        return None

    def decline_friend_request(self, user: User) -> None:
        """Отклонение запроса дружбы."""
        FriendRequest.objects.filter(
            sender_id=user.id,
            receiver_id=self.request.user.id,
        ).delete()
        return None


class FriendshipServices(object):

    def __init__(self, request):
        self.request = request

    def remove_friend(self, user: User) -> None:
        Friendship.objects.filter(
            another_user_id=user.id,
            current_user_id=self.request.user.id,
        ).delete()
        Friendship.objects.filter(
            another_user_id=self.request.user.id,
            current_user_id=user.id,
        ).delete()
        return None
