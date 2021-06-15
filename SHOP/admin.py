from django.contrib import admin
from .models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'created', 'updated']
    list_filter = ['stock', 'created', 'updated']
    list_editable = ['price', 'stock']
    prepopulated_fields = {'slug': ('name',)}

class HashTagAdmin(admin.ModelAdmin):
    list_display = ['hash_tag',]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(HashTag, HashTagAdmin)