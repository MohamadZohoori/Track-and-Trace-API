from django.contrib import admin
from .models import Shipment

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'carrier', 'status', 'article_name', 'article_quantity', 'article_price', 'SKU')
    search_fields = ('tracking_number', 'carrier', 'status', 'article_name')
    list_filter = ('carrier', 'status')
    ordering = ('-id',)  # Orders by most recent

admin.site.register(Shipment, ShipmentAdmin)

