# Generated by Django 5.1.2 on 2024-12-04 10:39

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0006_remove_profile1_account_age_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile1",
            name="saved_recipes",
        ),
    ]
