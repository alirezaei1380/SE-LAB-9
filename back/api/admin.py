from django.contrib import admin

from api.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
