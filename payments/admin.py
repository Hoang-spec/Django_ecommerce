from django.contrib import admin
from .models import Address, Order, OrderItem

# Đăng ký mô hình Address để hiển thị trong admin
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
