# Generated by Django 4.1.7 on 2023-03-01 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_delete_news_delete_otp_rename_name_user_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='profiles/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories_set', to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followings_set', to='core.user')),
                ('users', models.ManyToManyField(blank=True, to='core.user')),
            ],
        ),
    ]