# Generated by Django 3.2.5 on 2021-07-28 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20210728_0644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refunds',
            name='status',
        ),
    ]