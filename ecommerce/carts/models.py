from django.db import models
from products.models import Product, Variation
# Create your models here.




class Cart(models.Model):
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return "Cart id: %s" % self.id

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    
    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title
    