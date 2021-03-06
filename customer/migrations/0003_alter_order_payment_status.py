# Generated by Django 3.2.5 on 2021-07-28 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20210727_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('success', 'SUCCESS'), ('failure', 'FAILURE'), ('pending', 'PENDING'), ('refunded', 'REFUNDED')], default='pending', max_length=100),
        ),
    ]
