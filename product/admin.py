from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('name',), }
@admin.register(Product)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug': ('name',), }