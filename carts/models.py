from django.db import models
from store.models import Product, Variation

# Create your models here.

# carr model
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    

#cart item model
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    #Sub total for product in Cart item
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product
    
    
    
    
    
      
    
    
