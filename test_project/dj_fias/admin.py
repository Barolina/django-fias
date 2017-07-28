from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *


class ItemAdmin(admin.ModelAdmin):
    class Media:
        js = ['//code.jquery.com/jquery-2.1.4.min.js']

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemWithArea, ItemAdmin)