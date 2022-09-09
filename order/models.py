from django.contrib.auth.models import User
from django.db import models
from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=2, null=True)
    amount_due = models.DecimalField(max_digits=8, decimal_places= 2, blank= 2, null=True)
    paid = models.BooleanField(default=False, null=False)
    delivered = models.BooleanField(default=False, null=False)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    checkoutRequestId = models.CharField(max_length= 50, null=True)
    result_description = models.CharField(max_length=200, null=True)
    class Meta:
        ordering = ['-created_at',]
    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete= models.CASCADE)
    product = models.ForeignKey(Product,related_name='items', on_delete= models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    size = models.IntegerField(default=39, null=False)

    def __str__(self):
        return '%s' % self.id
