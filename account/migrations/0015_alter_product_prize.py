# Generated by Django 5.0.3 on 2024-03-23 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_remove_product_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='prize',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
