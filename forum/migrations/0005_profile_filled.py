# Generated by Django 5.1.3 on 2024-11-15 01:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0004_alter_comment_author_alter_comment_post_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="filled",
            field=models.BooleanField(default=False, verbose_name="Заповнений"),
        ),
    ]
