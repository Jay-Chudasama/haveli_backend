# Generated by Django 4.1.7 on 2023-03-18 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_order_type_alter_orderitemquantity_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('PROCESSING', 'PROCESSING'), ('PACKED', 'PACKED'), ('OUT_FOR_DELIVERY', 'OUT_FOR_DELIVERY'), ('DELIVERED', 'DELIVERED'), ('FAILED', 'FAILED')], default=('ACCEPTED', 'ACCEPTED'), max_length=100),
        ),
    ]