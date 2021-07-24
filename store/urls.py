from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='product_by_category'), #Slug url for category url
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),# Slug url for product
    path('search/', views.search, name='search'),# Search Url
     path('submit_review/<int:product_id>/' , views.submit_review, name='submit_review')
] 