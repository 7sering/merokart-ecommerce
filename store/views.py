from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.

def store(request, category_slug=None):
    categories = None #Category slug code
    products = None # Category slug code
    
    if category_slug != None: #checking if Category slug is not null
        categories = get_object_or_404(Category, slug=category_slug) #Category slug codes
        products = Product.objects.filter(category=categories, is_available=True) # Category slug codes
        product_count = products.count() #counting product
    else:
        products = Product.objects.all().filter(is_available=True) #Getting all product
        product_count = products.count() # Counting Products
        
    context = {'products': products, 'product_count':product_count} # Passing product value thru context for fatching value in html front end page
    
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context = {'single_product': single_product} 
    
    return render(request, 'store/product_detail.html', context)