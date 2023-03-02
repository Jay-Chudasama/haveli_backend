# Generated by Django 4.1.7 on 2023-03-02 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('followed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
                ('liked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_notifications_set', to='core.user')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications_set', to='core.user')),
            ],
        ),
    ]
