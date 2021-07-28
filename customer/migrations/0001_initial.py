# Generated by Django 3.2.5 on 2021-07-27 11:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, default=None, max_length=100, null=True, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('payment_status', models.IntegerField(choices=[('success', 'SUCCESS'), ('failure', 'FAILURE'), ('pending', 'PENDING'), ('refunded', 'REFUNDED')], default=3)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_from', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]