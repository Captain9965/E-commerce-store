from django.contrib import admin

from .models import Order, OrderItem


class OrderInline(admin.TabularInline):
    model = OrderItem
    fields = ('id', 'product')
    readonly_fields = ('product',)

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = (OrderInline,)

admin.site.register(Order, OrderAdmin)
