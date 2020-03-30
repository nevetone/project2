from django.contrib import admin
from .models import UserStripe, EmailConfirmed, EmailMarketingSignUp, UserAddress, UserDefaultAddress
# Register your models here.

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)


class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ["__str__", "timestamp",]
    class Meta:
        model = EmailMarketingSignUp


admin.site.register(EmailMarketingSignUp, EmailMarketingSignUpAdmin)

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ["__str__", "timestamp",]
    class Meta:
        model = UserAddress


admin.site.register(UserAddress, UserAddressAdmin)


class UserDefaultAddressAdmin(admin.ModelAdmin):
    list_display = ["__str__",]
    class Meta:
        model = UserDefaultAddress

admin.site.register(UserDefaultAddress, UserDefaultAddressAdmin)

