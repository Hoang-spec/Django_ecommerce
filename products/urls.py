from django.urls import path
from .views import ProductListCreateView
from . import  views

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('search/', views.product_search, name='search_products'),
    path('api/autocomplete/', views.product_autocomplete, name='product_autocomplete'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('Contact/', views.contact_view, name='contact'),
]