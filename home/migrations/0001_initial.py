# Generated by Django 3.0.8 on 2020-08-11 11:00

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('fax', models.CharField(blank=True, max_length=15)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('smtpserver', models.CharField(blank=True, max_length=20)),
                ('smtpemail', models.CharField(blank=True, max_length=20)),
                ('smtppassword', models.CharField(blank=True, max_length=10)),
                ('smtpport', models.CharField(blank=True, max_length=5)),
                ('icon', models.ImageField(blank=True, upload_to='images/')),
                ('facebook', models.CharField(blank=True, max_length=50)),
                ('instagram', models.CharField(blank=True, max_length=50)),
                ('twitter', models.CharField(blank=True, max_length=50)),
                ('aboutus', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('contact', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('reference', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('status', models.CharField(choices=[('True', 'Evet'), ('False', 'Hayır')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
