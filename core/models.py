from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField(null=True)
    product_id = models.IntegerField(unique=True)
    
    def __str__(self):
        name = self.product_name
        return name
    

class Payment(models.Model):
    payment_id = models.IntegerField(unique=True)
    authorized_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        name = f"{self.payment_id}"
        return name
    
    def total_price(self):
        total = 0
        for item in self.paymentitem_set.all():
            total = item.total_price() + total
        
        return total
    
    
    
class PaymentItem(models.Model):
    product = models.ForeignKey(Product, related_name='paymentitem', on_delete=models.DO_NOTHING)
    count = models.IntegerField()
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        identifier = f"{ self.product } - { self.count }"
        return identifier
            
    def total_price(self):
        total_price = self.product.product_price * self.count
        return total_price
        