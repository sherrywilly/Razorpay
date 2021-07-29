from customer.models import Order, Payouts, Shopprofile, Transaction
from django.contrib import admin

# Register your models here.
admin.site.register(Order)
admin.site.register(Shopprofile)
admin.site.register(Payouts)

admin.site.register(Transaction)