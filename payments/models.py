from django.db import models
from django.contrib.auth.models import User
from products.models import Products  # Giả sử bạn đã có mô hình Products

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='N')
    street = models.CharField(max_length=255, default='No phone')
    city = models.CharField(max_length=100, default='No phone')
    state = models.CharField(max_length=100, default='No phone')
    zip_code = models.CharField(max_length=20, default='No phone')
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_default = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code} ({self.phone})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Liên kết với người dùng
    address = models.CharField(max_length=255)  # Địa chỉ giao hàng
    phone = models.CharField(max_length=20)  # Số điện thoại người nhận
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Tổng giá trị đơn hàng
    status = models.CharField(max_length=20, default='Pending')  # Trạng thái đơn hàng (Pending, Completed, v.v.)
    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo đơn hàng

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Liên kết với đơn hàng
    product = models.ForeignKey(Products, on_delete=models.CASCADE)  # Liên kết với sản phẩm
    quantity = models.PositiveIntegerField()  # Số lượng sản phẩm
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Tổng giá trị sản phẩm (price * quantity)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (user: {self.user.username})"
