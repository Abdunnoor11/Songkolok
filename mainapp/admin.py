from django.contrib import admin
from .models import *
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date_orderd']

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Poster)
