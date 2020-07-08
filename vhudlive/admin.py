from django.contrib import admin
from .models import Storage, Data

class StorageAdmin(admin.ModelAdmin):
     fields = ('name', 'type', 'active', 'owner')
     list_display = ('name', 'type', 'active', 'id', 'owner')
     list_filter = ('name', 'type', 'owner')

class DataAdmin(admin.ModelAdmin):
     fields = ('data_of', 'name', 'details', 'units', 'active')
     list_display = ('name', 'details', 'updated_date', 'units', 'active')
     list_filter = ('name', 'details', 'units','active')

admin.site.register(Storage, StorageAdmin)
admin.site.register(Data, DataAdmin)

