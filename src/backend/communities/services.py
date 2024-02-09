from .models import Community


class FollowService(object):
    """Сервиса для подписывания/отписывания пользователя"""

    def __init__(self, request):
        self.request = request

    def add_follower(self, community: Community) -> None:
        community.followers.add(self.request.user)
        return None

    def remove_follower(self, community: Community) -> None:
        community.followers.remove(self.request.user)
        return None
