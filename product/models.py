from __future__ import unicode_literals
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=250)
    category_slug = models.SlugField(unique=True)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    product_slug = models.SlugField(unique=True)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    def __str__(self):
        return self.name
