from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )  # Phần trăm giảm giá
    active = models.BooleanField()

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and (self.valid_from <= now <= self.valid_to)