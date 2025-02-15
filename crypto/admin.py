from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Exchange, Price, ArbitrageOpportunity

admin.site.register(Exchange)
admin.site.register(Price)
admin.site.register(ArbitrageOpportunity)
