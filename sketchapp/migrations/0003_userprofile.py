# Generated by Django 3.2.9 on 2022-01-17 12:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sketchapp.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sketchapp', '0002_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True)),
                ('phone', models.BigIntegerField(default=None)),
                ('image', models.FileField(blank=True, upload_to=sketchapp.models.file_upload)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('email', models.TextField(blank=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_user', models.BooleanField(default=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]