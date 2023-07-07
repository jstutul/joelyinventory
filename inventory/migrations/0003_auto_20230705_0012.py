# Generated by Django 3.2 on 2023-07-04 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_product_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(default=10.0),
        ),
    ]