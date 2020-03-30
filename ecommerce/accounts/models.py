import stripe
import random
import hashlib
import encodings
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.template.loader import render_to_string

# pip install django-localflavor
from localflavor.pl.pl_administrativeunits import ADMINISTRATIVE_UNIT_CHOICES 


# Create your models here.

class UserDefaultAddress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey("UserAddress", related_name="user_address_shipping_default",\
          on_delete=models.CASCADE, null=True, blank=True)
    billing = models.ForeignKey("UserAddress", related_name="user_address_billing_default",\
         on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.user.username)
    
    
class UserAddressMenager(models.Manager):
    def get_billing_addresses(self, user):
        return super(UserAddressMenager, self).filter(billing=True).filter(user=user)

class UserAddress(models.Model):
    cities = sorted(ADMINISTRATIVE_UNIT_CHOICES)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, choices=cities)
    country = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    zipcode = models.CharField(max_length=25)
    phone = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    billing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def __str__(self):
        return str(self.user.username)
    
    def get_address(self):
        return "%s, %s, %s, %s, %s" %(self.country, self.city, self.address, self.zipcode, self.phone)
    
    objects = UserAddressMenager()
    
    class Meta:
        ordering = ['-updated', '-timestamp'] 
    
class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True) 
    
    def __str__(self):
        return str(self.stripe_id)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " | " + str(self.confirmed)
    
    
    # wysylanie i aktywaowanie emaili
    def activate_user_email(self):
        activation_url = 'http://192.168.1.28:80/accounts/activate/%s/' % self.activation_key
        context ={
            "activation_key": self.activation_key,
            "activation_url" : activation_url,
            "user" : self.user.username
        }
        message = render_to_string("accounts/activation_message.txt", context)
        subject = "Activate your Email"
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        
        
    def email_user(self, subject, message, from_email=None, *kwargs):
        send_mail(subject, message, from_email, [self.user.email])


class EmailMarketingSignUp(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    #confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.email)
    







# stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()

def get_create_stripe(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
        email = str(user.email)
        )
        new_user_stripe.stripe_id = customer.id
        new_user_stripe.save()

def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    if created:
        get_create_stripe(user)
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            # tworzenie unikatowego klucza
            short_hash = hashlib.sha1(str(random.random()).encode()).hexdigest()[:5]
            base, domain = str(user.email).split("@")
            activation_key = hashlib.sha1(str(short_hash + base).encode()).hexdigest()
            # wysywalnie klucza do bazy 
            email_confirmed.activation_key = activation_key
            email_confirmed.save()
            # odpalanie funkcji 
            email_confirmed.activate_user_email()
    

post_save.connect(user_created, sender=User)



