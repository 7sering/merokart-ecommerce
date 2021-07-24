from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating
from category.models import Category
from carts.models import CartItem 
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator #import paginator for pagination 

from carts.views import _cart_id
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct

# from django.http import HttpResponse
# Create your views here.

def store(request, category_slug=None):
    categories = None #Category slug code
    products = None # Category slug code
    
    if category_slug != None: #checking if Category slug is not null
        categories = get_object_or_404(Category, slug=category_slug) #Category slug codes
        products = Product.objects.filter(category=categories, is_available=True) # Category slug codes
        paginator = Paginator(products, 6) #showing 6 product per page in store
        page = request.GET.get('page') #getting page number
        page_products = paginator.get_page(page)
        product_count = products.count() #counting product
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') #Getting all product
        paginator = Paginator(products, 6) #showing 6 product per page in store
        page = request.GET.get('page') #getting page number
        page_products = paginator.get_page(page)
        product_count = products.count() # Counting Products
        
    context = {'products': page_products, 'product_count':product_count} # Passing product value thru context for fatching value in html front end page
    
    return render(request, 'store/store.html', context)

#TODO Product Details Codes
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists() #Its shows if true product in cart if its false product is not in cart
        # return HttpResponse(in_cart) #checking if get the value in front end page
        # exit() 
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        # Checking if logged in user purchased this product or not ofr review sumbit
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        
    #Fetching All reviews in front end 
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
            
    context = {
        'single_product': single_product, 
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        } 
    
    return render(request, 'store/product_detail.html', context)



#TODO Search Functionality 
def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)) # All Product Getting Here
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

#TODO Submit Review Functionality 
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)