# Generated by Django 4.2.4 on 2023-08-24 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_verified_email_emailverification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailverification',
            old_name='expiretion',
            new_name='expiration',
        ),
    ]
