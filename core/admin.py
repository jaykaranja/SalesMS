from django.contrib import admin
from .models import Product, PaymentItem, Payment

# Register your models here.

admin.site.register(Product)
admin.site.register(PaymentItem)
admin.site.register(Payment)