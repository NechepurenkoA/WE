# Generated by Django 5.0.1 on 2024-01-29 07:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_group"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="group",
            options={
                "ordering": ["slug"],
                "verbose_name": "Группа",
                "verbose_name_plural": "Группы",
            },
        ),
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ["username"],
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]
