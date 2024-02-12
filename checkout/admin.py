from django.contrib import admin
from .models import Price

class PriceAdmin(admin.ModelAdmin):
    list_display = ('lesson_price',)
    fields = ('lesson_price',)

admin.site.register(Price)