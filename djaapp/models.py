from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    name=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=6, decimal_places=2)
    covers=models.ImageField(upload_to="covers", null=True, blank=True)
    

    def __str__(self):
        return f"{self.name} by {self.author}"

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} x {self.book.name} by {self.book.author}"
    