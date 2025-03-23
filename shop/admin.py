from django.contrib import admin
from .models import AssortmentItem, Order


@admin.register(AssortmentItem)
class AssortmentAdmin(admin.ModelAdmin):
    """Налаштування відображення моделі Асортименту в адмін-панелі"""
    list_display = ('name', 'price')
    search_fields = ('name',)
    list_per_page = 20

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Налаштування відображення моделі Замовлення в адмін-панелі"""
    list_display = ('id', 'customer_name', 'product',
                    'delivery_date', 'status', 'created_at')
    list_filter = ('status', 'product')
    search_fields = ('customer_name', 'phone_number', 'email')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Інформація про замовника', {
            'fields': ('customer_name', 'phone_number', 'email')
        }),
        ('Деталі замовлення', {
            'fields': ('product', 'quantity', 
                      'order_date', 'delivery_date', 'comment')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
