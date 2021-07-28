# Generated by Django 3.2.5 on 2021-07-27 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.IntegerField(choices=[('success', 'SUCCESS'), ('failure', 'FAILURE'), ('pending', 'PENDING'), ('refunded', 'REFUNDED')], default='pending'),
        ),
        migrations.AlterField(
            model_name='order',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_to', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Shopprofile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_id', models.CharField(blank=True, max_length=100, null=True)),
                ('fund_id', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Refunds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refund_id', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('process', 'PROCESSING'), ('completed', 'COMPLETED')], max_length=50)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='customer.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payouts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
