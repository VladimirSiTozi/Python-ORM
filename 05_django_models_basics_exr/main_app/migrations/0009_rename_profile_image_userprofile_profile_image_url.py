# Generated by Django 5.0.4 on 2024-06-20 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile_image',
            new_name='profile_image_url',
        ),
    ]
