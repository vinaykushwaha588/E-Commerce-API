# Generated by Django 5.0.3 on 2024-03-23 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_dob_user_image_user_status_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_inactive',
            field=models.BooleanField(default=False),
        ),
    ]
