from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'phone', 'address', 'postal_code', 'city', 'region']

admin.site.register(Customer, CustomerAdmin)


class TemporaryBanIpAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'status', 'attempts', 'time_unblock')
    search_fields = ('ip_address',)

admin.site.register(TemporaryBanIp, TemporaryBanIpAdmin)