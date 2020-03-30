from django.shortcuts import render, Http404
from .models import Product, ProductImage
from marketing.models import MarketingMessage, Slider
from marketing.forms import EmailForm

# Create your views here.
def home(request):
    sliders = Slider.objects.featured()
    products = Product.objects.all()
    template="products/home.html"
    context = {'products': products,
               'sliders': sliders,}
    return render(request, template, context)

def all(request):
    products = Product.objects.all()
    template="products/all.html"
    context = {'products': products,}
    return render(request, template, context)

def single(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        images = ProductImage.objects.filter(product=product)
        template="products/single.html"
        context = {'product': product, "images": images}
        return render(request, template, context)
    except:
        raise Http404
    
def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None   
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {'query':q, 'products': products}
        template="products/results.html"
    else:
        context = {}
        template="products/home.html"
    return render(request, template, context)