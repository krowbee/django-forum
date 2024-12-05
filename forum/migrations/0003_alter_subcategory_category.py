# Generated by Django 5.1.3 on 2024-11-06 23:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("forum", "0002_alter_subcategory_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subcategory",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subcategory",
                to="forum.category",
                verbose_name="Категорія",
            ),
        ),
    ]