# Generated by Django 3.0.8 on 2020-08-13 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20200812_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='hint',
        ),
        migrations.AddField(
            model_name='book',
            name='pageNumber',
            field=models.CharField(default=2, max_length=4),
            preserve_default=False,
        ),
    ]
