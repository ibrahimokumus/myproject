# Generated by Django 3.0.8 on 2020-08-20 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_auto_20200820_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='stok_durum',
            field=models.IntegerField(),
        ),
    ]
