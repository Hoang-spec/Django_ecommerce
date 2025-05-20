from django.db import models

# Create your models here.
class Products(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    type = models.CharField(max_length=50, default='general')
    picture = models.TextField(default='a')

    def __str__(self):
        return self.name
