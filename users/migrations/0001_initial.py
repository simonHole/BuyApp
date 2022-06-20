# Generated by Django 4.0.4 on 2022-06-07 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('biography', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default='profiles/default.png', null=True, upload_to='profiles/')),
                ('github', models.CharField(blank=True, max_length=200, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=200, null=True)),
                ('facebook', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
