from django.contrib import admin

from stocks.models import Stock, Transaction

# Register your models here.
admin.site.register(Stock)
admin.site.register(Transaction)
