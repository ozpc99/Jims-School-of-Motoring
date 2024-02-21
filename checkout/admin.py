from django.contrib import admin
from .models import Price

class PriceAdmin(admin.ModelAdmin):
    list_display = ('get_lesson_price',)
    
    def get_lesson_price(self, obj):
        return obj.lesson_price

    def has_add_permission(self, request):
        existing_prices_count = Price.objects.count()

        return existing_prices_count == 0

    get_lesson_price.short_description = 'Lesson Price'

admin.site.register(Price, PriceAdmin)