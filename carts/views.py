from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# from django.http import HttpResponse

# Create your views here.

#Function for getting cart id from browser session key
def _cart_id(request):
    cart = request.session.session_key #Requesting session key for car id 
    if not cart: #if cart session key is not availabe creating session key 
        cart = request.session.create()
    return cart



# Add to Cart Function Codes 
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id) #Geting products
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) #Fetching Cart ID from session id
    except Cart.DoesNotExist: #creating cart if not exist
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
    try: # getting cart item in kart
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist: #If Cart Item doesnot exist creating new cart item
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    # return HttpResponse(cart_item.product)
    # exit()
    return redirect('cart')

#Remove Cart item   decrement function 
def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request)) 
    product = get_object_or_404(Product, id=product_id) # Getting Product 
    cart_item = CartItem.objects.get(product=product, cart=cart) #Getting cart items
    if cart_item.quantity > 1: # Checking if product in cart greater then 1 then below its minus by 1
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart.item.delete()
    return redirect('cart')


#Remove Cart item  function single product
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request)) 
    product = get_object_or_404(Product, id=product_id) # Getting Product 
    cart_item = CartItem.objects.get(product=product, cart=cart) #Getting cart items
    cart_item.delete()
    
    return redirect('cart')
    
    
    
        

# Cart Function Codes
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # Getting Cart id 
        cart_items = CartItem.objects.filter(cart=cart, is_active=True) # Getting Item in Cart
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) # Sub Total of Product
            quantity += cart_item.quantity # Total Quantity of Product
        tax = (3 * total)/100 # Tax adding 
        grand_total = total + tax #Grand Total of cart
    except ObjectDoesNotExist:
        pass # If object not exist just ignore
    context = {
        'total' : total,
        'quantity': quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' : grand_total,
    }
    
    return render(request, 'store/cart.html', context)

