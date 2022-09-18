from django.contrib import admin

from ecommerce.models import Profile, Product, Category, Order, OrderStatus, Item, Article, Images

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderStatus)
admin.site.register(Article)


class ProductImage(admin.TabularInline):
    model = Images
    inlines = []
    extra = 1


# @admin.register(Product)
# class ProductAdmin(NestedModelAdmin):
#     inlines = [ProductImage]

#     list_display = ['name', 'price', 'category', 'is_active', 'qty']
#     list_filter = ['is_active', 'category']
#     search_fields = ['name', 'price', 'category']
#     list_per_page = 20

admin.site.register(Product)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    list_per_page = 20


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'address']
    list_per_page = 20
