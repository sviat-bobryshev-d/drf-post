# Generated by Django 4.2.5 on 2023-09-29 06:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0002_alter_post_owner_profile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="user",
            new_name="owner",
        ),
    ]