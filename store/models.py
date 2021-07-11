from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length = 200, unique=True)
    slug = models.SlugField(max_length = 200, unique=True)
    description = models.TextField(max_length = 1000, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/product')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    #single product page detail ur link 
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
        
    
    def __str__(self):
        return self.product_name
    
    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
        
    


#Variation Model
variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length = 150, choices=variation_category_choice)
    variation_value = models.CharField(max_length = 150)
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    
    def __str__(self):
        return self.variation_value
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    