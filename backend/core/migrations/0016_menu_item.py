# Generated by Django 4.1.7 on 2023-03-15 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_otp_delete_book_remove_notification_followed_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('LUNCH', 'LUNCH'), ('DINNER', 'DINNER')], max_length=100)),
                ('closing', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('name', models.CharField(max_length=100)),
                ('extras', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.menu')),
            ],
        ),
    ]
