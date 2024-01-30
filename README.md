# Социальная сеть "Паутина"

## Описание проекта

Проект разрабатывается исключительно в ознакомительных целях и
не позиционирует себя как коммерческий.

## Запланировано:
   ### Начальная стадия разработки (API + Django models)
   - Регистрация пользователей и авторизация;
   - Новостная лента с возможностью просмотра недавних постов групп и
пользователей;
   - Чат между пользователями;
   - Запуск бэкэнда с помощью Docker, подключение PostgreSQL.
### Поздняя стадия разработки (Frontend составляющая)
   - Внедрение фронтенда, планируется React JS;
   - Запуск всего проекта через Docker.

## Используемый стек

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![DRF][DRF-badge]][DRF-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Nginx][Nginx-badge]][Nginx-url]

## Архитектура проекта

| Директория    | Описание                                                |
|---------------|---------------------------------------------------------|
| `infra`       | Файлы для запуска с помощью Docker, настройки Nginx     |
| `src/backend` | Код Django приложения                                   |

# Подготовка

## Требования

1. **Python 3.12**  
   Убедитесь, что у вас установлена нужная версия Python или активирована в
   pyenv.

2. **Poetry**  
   Зависимости и пакеты управляются через poetry. Убедитесь, что
   poetry [установлен](https://python-poetry.org/docs/#installing-with-the-official-installer)
   на вашем компьютере и ознакомьтесь
   с [документацией](https://python-poetry.org/docs/basic-usage/).  
   Установка зависимостей

    ```
    poetry install
    ```

    Также будет создано виртуальное окружение, если привычнее видеть его в
    директории проекта, то
    используйте [настройку](https://python-poetry.org/docs/configuration/#adding-or-updating-a-configuration-setting) `virtualenvs.in-project`


3. **Docker**

   To be written

4. **pre-commit**
   [Документация](https://pre-commit.com/)  
   При каждом коммите выполняются хуки (автоматизации) перечисленные в
   .pre-commit-config.yaml. Если не понятно какая ошибка мешает сделать коммит
   можно запустить хуки вручную и посмотреть ошибки:
    ```shell
    pre-commit run --all-files
    ```


# Разворачиваем проект локально

_To be written_

<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white

[DRF-url]: https://github.com/encode/django-rest-framework

[DRF-badge]: https://img.shields.io/badge/DRF-a30000?style=for-the-badge

[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-306189?style=for-the-badge&logo=postgresql&logoColor=white

[Nginx-url]: https://nginx.org

[Nginx-badge]: https://img.shields.io/badge/nginx-009900?style=for-the-badge&logo=nginx&logoColor=white
