"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from products.views import home, all, single, search
from django.conf import settings
from django.conf.urls.static import static
from carts.views import view as cartView
from carts.views import add_to_cart, remove_from_cart
from orders.views import checkout, orders
from accounts.views import logout_view, login_view, registration_view, activation_view, add_user_address, account
from marketing.views import dismiss_marketing_message, email_signup

urlpatterns = [
    re_path(r'^$', home, name='home'),
    path('products/', all, name='products'),
    # path('products/<slug>/', single, name='single_product'),
    re_path(r'^products/(?P<slug>[\w-]+)/$', single, name='single_product'),
    path('admin/', admin.site.urls),
    path('s/', search, name='search'),
    re_path(r'^cart/$', cartView, name='cart'),
    re_path(r'^checkout/$', checkout, name='checkout'),
    re_path(r'^orders/$', orders, name='user_orders'),
    re_path(r'^ajax/dismiss_marketing_message/$', dismiss_marketing_message, name='dismiss_marketing_message'),
    re_path(r'^ajax/email_signup/$', email_signup, name='ajax_email_signup'),
    re_path(r'^ajax/add_user_address/$', add_user_address, name='ajax_add_user_address'),
    # path('cart/<slug>/<qty>/', update_cart, name='update_cart'),
    re_path(r'^cart/(?P<id>\d+)/$', remove_from_cart, name='remove_from_cart'),
    re_path(r'^cart/(?P<slug>[\w-]+)/$', add_to_cart, name='add_to_cart'),
    path('accounts/logout/', logout_view, name='auth_logout' ),
    path('accounts/login/', login_view, name='auth_login' ),
    path('accounts/account/', account, name='account' ),
    path('accounts/register/', registration_view, name='auth_register' ),
    re_path(r'^accounts/activate/(?P<activation_key>\w+)/$', activation_view, name='activation_view'),
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    
    