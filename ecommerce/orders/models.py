from django.db import models
from django.contrib.auth import get_user_model
from carts.models import Cart
# Create your models here.


User = get_user_model()


STATUS_CHOICES = [
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Finished", "Finished"),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.CharField(max_length=120, default="ABC", unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    tax_total = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2)
    
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.order_id
    