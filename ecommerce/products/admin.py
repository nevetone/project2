from django.contrib import admin
from .models import Product, ProductImage, Variation
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp' # sortowanie po dacie
    search_fields = ['title', 'description'] # wyszukiwanie
    list_display = ['title', 'price', 'active', 'updated'] # wyswietlanie modeli
    list_editable = ['price', 'active'] # edytowanie modeli
    list_filter = ['price', 'active'] # filter z prawej strony
    readonly_fields = ['updated','timestamp'] # dodanie pola readonly
    prepopulated_fields = {"slug": ['title']} # automatyczne robienie sluga
    
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Variation)