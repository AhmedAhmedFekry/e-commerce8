from django.contrib import admin

from vendor.models import Vendor


class Vendoradmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']


admin.site.register(Vendor, Vendoradmin)
