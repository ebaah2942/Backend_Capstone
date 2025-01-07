# Generated by Django 5.1.4 on 2025-01-06 21:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='is_repost',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='Hashtags',
            field=models.ManyToManyField(blank=True, to='api.hashtag'),
        ),
        migrations.CreateModel(
            name='SharedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
