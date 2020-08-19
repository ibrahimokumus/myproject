from django.contrib import admin

# Register your models here.
from order.models import ShopCart, Order, OrderBook


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','book','quantity']
    list_filter = ['user']


class Orderbookline(admin.TabularInline):
    model = OrderBook
    readonly_fields = ('user', 'book', 'quantity', 'stok_durum')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'city', 'status']
    list_filter = ['status']
    readonly_fields = (
    'user', 'address', 'city', 'country', 'phone', 'first_name', 'ip', 'last_name', 'phone', 'city', )
    can_delete = False
    inlines = [Orderbookline]


class OrderbookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book',  'quantity', 'stok_durum']
    list_filter = ['user']
admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderBook,OrderbookAdmin)