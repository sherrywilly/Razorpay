from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class Shopprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_id = models.CharField(max_length=100,blank=True,null=True)
    fund_id = models.CharField(max_length=100,blank=True,null=True)


class Order(models.Model):
    payment_status_choices = (
        ('success', 'SUCCESS'),
        ('failure', 'FAILURE' ),
        ('pending', 'PENDING'),
        ('refunded', 'REFUNDED'),
    )
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None) 
    user = models.ForeignKey(User, on_delete = models.PROTECT,related_name='user_from')
    amount = models.DecimalField(default=00,decimal_places=2, max_digits=6)
    to_user = models.ForeignKey(User, on_delete = models.PROTECT,related_name='user_to')
    payment_status = models.CharField(max_length=100,choices = payment_status_choices, default='pending')
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now=True)  
    

class Refunds(models.Model):
    order = models.OneToOneField(Order,on_delete=models.PROTECT)
    refund_id = models.CharField(max_length=100)
   
class Payouts(models.Model):
    p_id = models.CharField(max_length=100)
    amount = models.DecimalField(default=00,decimal_places=2, max_digits=6)
    paid_amount = models.DecimalField(default=00,decimal_places=2, max_digits=6)
    commission = models.DecimalField(default=00,decimal_places=2, max_digits=6)
    user = models.ForeignKey(User,on_delete=models.PROTECT)