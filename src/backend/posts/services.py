from rest_framework.request import Request
from rest_framework.validators import ValidationError

from posts.models import Post


def validate_text_or_image(data: dict, object_to_validate, dict_key: str):
    """
    Сервис для валидации текста вместе с картинкой в посте.
    Если оба поля null -> ValidationError
    Если 1 поле null, а другое отсутствует -> ValidationError
    Если все OK -> object
    """
    try:
        another_object = data[dict_key]
        if object_to_validate is None and another_object is None:
            raise ValidationError("Нельзя создать пустой пост!")
    except KeyError:
        if object_to_validate is None:
            raise ValidationError("Нельзя создать пустой пост!")
    return object_to_validate


class PostServices(object):

    def __init__(self, request: Request):
        self.request = request

    def like_post(self, post: Post) -> None:
        post.likes.add(self.request.user)
        post.save()

    def unlike_post(self, post: Post) -> None:
        post.likes.remove(self.request.user)
        post.save()
