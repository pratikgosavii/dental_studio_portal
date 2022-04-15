from django.contrib import admin

from main.models import *

# Register your models here.


admin.site.register(doctor)
admin.site.register(order)
admin.site.register(order_detials)