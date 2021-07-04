from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0 # cart count variable 
    if 'admin' in request.path:
        return() #if we're inside the admin whe don't want see anything in cart counter
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request)) #getting cart
            cart_items = CartItem.objects.all().filter(cart=cart[:1]) #getting cart product(item)
            for cart_item in cart_items: #loop thru cart_item 
                cart_count += cart_item.quantity
                
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)