# Generated by Django 3.2.10 on 2022-03-23 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='thumb',
            field=models.PositiveSmallIntegerField(default='default_product.jpg', null=True),
        ),
    ]
