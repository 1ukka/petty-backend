from django.contrib import admin
from petappbackend.ecommerce.models import *
from nested_inline.admin import NestedModelAdmin

admin.site.register(profile)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderStatus)
admin.site.register(Article)

class ProductImage(admin.TabularInline):
    model = Images
    inlines = []
    extra = 1

@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    inlines = [ProductImage]

    list_display = ['name', 'price', 'category', 'is_active', 'qty']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'price', 'category']
    list_per_page = 20
