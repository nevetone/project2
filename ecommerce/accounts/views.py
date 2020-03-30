import re
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
# Create your views here.
from .forms import LoginForm, RegistrationForm, UserAddressForm
from .models import EmailConfirmed, UserDefaultAddress
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logged OUT.")
    return HttpResponseRedirect('%s' % reverse('auth_login'))

def login_view(request):
    form = LoginForm(request.POST or None)
    btn = "Login"
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Successfully Logged IN.")
        return HttpResponseRedirect('/')
    context={"form":form, 'btn':btn,}
    return render(request, "form.html", context)

def registration_view(request):
    form = RegistrationForm(request.POST or None)
    btn = "Register"
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.save()
        messages.success(request, "Successfully Registered. Please Confirm your Email")
        return HttpResponseRedirect('/')
    context={"form":form, 'btn':btn,}
    return render(request, "form.html", context)

SHA1_RE = re.compile("^[a-f0-9]{40}$")

def activation_view(request, activation_key):
    if SHA1_RE.search(activation_key):
        try:
            instance = EmailConfirmed.objects.get(activation_key = activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            raise Http404
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful! Welcome %s." % instance.user
            instance.confirmed = True
            instance.activation_key = "Confirmation Successful! Welcome"
            instance.save()
            messages.success(request, "Successfully Confirmed.")
        elif instance is not None and instance.confirmed:
            page_message = "Already Confirmed"
            messages.success(request, "Already Confirmed.")
        else:
            page_message = ""
            pass 
        context = {"key": activation_key, 'page_message':page_message,}
        return render(request, "accounts/activation_complete.html", context)
    else:
        raise Http404
def add_user_address(request):
    try:
        next_page = request.GET.get("next")
    except:
        next_page = None
    if request.method == "POST":
        form = UserAddressForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default = form.cleaned_data['default']
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.shipping = new_address
                default_address.save()
            if next_page is not None:
                return HttpResponseRedirect(reverse(str(next_page))+"?address_added=True")
    else:
        raise Http404
def account(request):
    context = { }
    return render(request, "accounts/account.html", context)