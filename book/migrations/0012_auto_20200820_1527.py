# Generated by Django 3.0.8 on 2020-08-20 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_book_son_durum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='son_durum',
            new_name='stok_durum',
        ),
    ]
