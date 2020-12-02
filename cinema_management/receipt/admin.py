from django.contrib import admin

from .models import ComboDetail, Receipt, Ticket

# Register your models here.
admin.site.register(ComboDetail)
admin.site.register(Receipt)
admin.site.register(Ticket)
