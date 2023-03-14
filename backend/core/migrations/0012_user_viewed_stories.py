# Generated by Django 4.1.7 on 2023-03-07 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_follow_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='viewed_stories',
            field=models.ManyToManyField(blank=True, related_name='user_set', to='core.storyimage'),
        ),
    ]
