from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from products.models import Products


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}★"

    @classmethod
    def get_average_rating(cls, product):
        return cls.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0

    def verify_purchase(self):
        from orders.models import OrderItem
        return OrderItem.objects.filter(
            order__user=self.user,
            product=self.product,
            order__status='completed'
        ).exists()

    def save(self, *args, **kwargs):
        if not self.verified_purchase:
            self.verified_purchase = self.verify_purchase()
        super().save(*args, **kwargs)
