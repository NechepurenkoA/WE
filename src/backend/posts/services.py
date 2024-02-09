from rest_framework.validators import ValidationError


def validate_text_or_image(data: dict, object_to_validate, dict_key: str):
    """
    Сервис для валидации текста вместе с картинкой в посте.
    Если оба поля null -> ValidationError
    Если 1 поле null, а другое отсутствует -> ValidationError
    Если все OK -> object
    """
    if dict_key not in data.keys() and object_to_validate is None:
        raise ValidationError("Нельзя создать пустой пост!")
    if dict_key in data.keys():
        another_object = data[dict_key]
        if object_to_validate is None and another_object is None:
            raise ValidationError("Нельзя создать пустой пост!")
    return object_to_validate
