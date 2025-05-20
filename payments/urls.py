from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('add-address/', views.add_address, name='add_address'),
]
