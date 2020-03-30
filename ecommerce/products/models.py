from django.db import models
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    sale_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ['title', 'slug']
    
    def get_price(self):
        return self.price
    
    def get_absolute_url(self):
        return reverse("single_product", kwargs={"slug": self.slug})
    
    
    
class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/', max_length=None, null=True, blank=True)
    featured = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return self.product.title
 
class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)
    def sizes(self):
        return self.all().filter(category='size')
    def color(self):
        return self.all().filter(category='color')
    def package(self):
        return self.all().filter(category='package')
    


VAR_CATEGORIES = [
    ('size', 'size'),
    ('color', 'color'),
    ('package', 'package'),
]
    
class Variation(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    image = models.ForeignKey("ProductImage", null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    objects = VariationManager()
    def __str__(self):
        return str(self.category) + " " + str(self.title) + " | " + str(self.product)
    