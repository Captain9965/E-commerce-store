from django.contrib import admin

from .models import Order, OrderItem


class OrderInline(admin.TabularInline):
    model = OrderItem
    fields = ('id', 'product','size','quantity',)
    readonly_fields = ('product',)

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = (OrderInline,)

admin.site.register(Order, OrderAdmin)
