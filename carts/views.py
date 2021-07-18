from django.shortcuts import render, redirect,get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

#Function for getting cart id from browser session key
def _cart_id(request):
    cart = request.session.session_key #Requesting session key for car id 
    if not cart: #if cart session key is not availabe creating session key 
        cart = request.session.create()
    return cart



# Add to Cart Function Codes 
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
 
    
    #If User is Not Authenticated 
    else:
        product_variation = []
        if request.method == 'POST': #for variation codes start
            for item in request.POST:
                key = item
                value = request.POST[key]
                # print(key, value)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation) #strong variation value inside of cart item 
                    # print(variation)
                except:
                    pass
                
                #above code is product
                
                
        #carts adding code   
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #Fetching Cart ID from session id
        except Cart.DoesNotExist: #creating cart if not exist
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        
        
        #cart item code
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists: # getting cart item in kart
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
                print(ex_var_list)
            if product_variation in ex_var_list:
                #increase cart item id #updating product quantity by 1 without adding anthoer variable 
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
                
        else: #If Cart Item doesnot exist creating new cart item
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0: 
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        # return HttpResponse(cart_item.product)
        # exit()
        return redirect('cart')




#Remove Cart item   decrement function 
def remove_cart(request, product_id, cart_item_id):
     
    product = get_object_or_404(Product, id=product_id) # Getting Product 
    try:
        if request.user.is_authenticated: #if user is logged in system 
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) #Getting cart items
        if cart_item.quantity > 1: # Checking if product in cart greater then 1 then below its minus by 1
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


#Remove Cart item  function single product
def remove_cart_item(request, product_id, cart_item_id):
     
    product = get_object_or_404(Product, id=product_id) # Getting Product
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request)) 
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id) #Getting cart items
    cart_item.delete()
    
    return redirect('cart')
    
    
    
        

# Cart Function Codes
def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True) # Getting Item in Cart if user is login user
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # Getting Cart id  for none login user
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



#checkout function 
@login_required(login_url = "login")
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True) # Getting Item in Cart if user is login user
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # Getting Cart id  for none login user
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
    return render(request, 'store/checkout.html', context)