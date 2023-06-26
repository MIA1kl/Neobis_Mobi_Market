from django.db import models
from authentication.models import User

class Product(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.PositiveIntegerField()
    product_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    short_description = models.CharField(max_length=150)
    detailed_description = models.TextField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"id: {self.pk} - user_id: {self.username_id} - title: {self.product_name}"
