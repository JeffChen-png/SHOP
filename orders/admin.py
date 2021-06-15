from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'country', 'region', 'city', 'address', 'postal_code', 'payment', 'status', 'created', 'updated']
    list_filter = ['payment', 'status', 'created', 'updated']
    search_fields = ['id', 'first_name', 'last_name', ]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
