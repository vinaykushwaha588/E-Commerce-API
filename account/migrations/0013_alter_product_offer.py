# Generated by Django 5.0.3 on 2024-03-23 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]