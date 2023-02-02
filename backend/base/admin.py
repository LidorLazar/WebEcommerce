from django.contrib import admin
from .models import Product,Order,OrderItem,Reviwe,ShippingAddress
# Register your models here.


admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Reviwe)
admin.site.register(ShippingAddress)