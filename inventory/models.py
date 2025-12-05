
from enum import unique
from django.db import models
from django.conf import settings



class Category(models.Model):
    name = models.CharField(max_length=100)
    # unique=True ensures no duplicate URLs
    slug = models.SlugField(unique=True, help_text="URL-friendly name (e.g. 'summer-sale')")

    class Meta:
        verbose_name_plural = "Categories" # Fixes "Categorys" typo in Admin

    def __str__(self):
        return self.name

class Item(models.Model):
    # --- RELATIONSHIPS ---
    # Links Item to Category. on_delete=CASCADE means if Category is deleted, Items go with it.
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='items'
    )

    # --- BASIC DATA ---
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=20, unique=True, help_text="Stock Keeping Unit")
    slug=models.SlugField(max_length=250,unique=True)

    
    # --- FINANCIAL DATA ---
    # SENIOR RULE: Never use FloatField for money.
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.PositiveIntegerField(default=0)

    # --- AUDIT TRAIL ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    # --- BUSINESS LOGIC ---
    # We define logic here so it is reusable everywhere (Admin, Views, API)
    @property
    def is_low_stock(self):
        return self.quantity < 5

RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

class Review(models.Model):

    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item=models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.item.name} ({self.rating}★)"