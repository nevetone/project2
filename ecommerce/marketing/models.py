from django.db import models
import datetime
# Create your models here.

class MarketingQueryset(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def featured(self):
        return self.filter(featured=True)\
            .filter(start_date__lte=datetime.datetime.now())\
            .filter(end_date__gt=datetime.datetime.now())

class MarketingManager(models.Manager):
    def get_queryset(self):
        return MarketingQueryset(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active()
    
    def featured(self):
        return self.get_queryset().active().featured()
        
    def get_featured_item(self):
        try:
            # __lte mniejsze lub rowne / __gte wieksze lub rowne 
            return self.get_queryset().active().featured()[0]
        except:
            return None
            

class MarketingMessage(models.Model):
    message = models.CharField(max_length=120)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    
    objects = MarketingManager()
    
    def __str__(self):
        return str(self.message[:12])
    
    class Meta:
        ordering = ['-start_date', '-end_date']


def slider_upload(instance, filename):
    return "images/marketing/slider/%s" % filename


class Slider(models.Model):
    image = models.ImageField(upload_to=slider_upload, max_length=100)
    order = models.IntegerField(default=0)
    url_link = models.CharField(max_length=250, null=True, blank=True)
    header_text = models.CharField(max_length=120, null=True, blank=True)
    text = models.CharField(max_length=120, null=True, blank=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    
    objects = MarketingManager()
    
    def __str__(self):
        return str(self.header_text) + ' | path:  ' + str(self.image)
    
    class Meta:
        ordering = [ 'order' ,'-start_date', '-end_date']
        
    