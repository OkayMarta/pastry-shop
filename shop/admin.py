from django.contrib import admin
from .models import AssortmentItem, Order


@admin.register(AssortmentItem)
class AssortmentAdmin(admin.ModelAdmin):
    """Налаштування відображення моделі Асортименту в адмін-панелі"""
    list_display = ('name', 'price', 'id') # Додав 'id' для зручності
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Налаштування відображення моделі Замовлення в адмін-панелі"""
    list_display = (
        'id',
        'customer_name',
        'phone_number',  # <--- ДОДАНО
        'email',  # <--- ДОДАНО
        'product',
        'delivery_date',
        'status',
        'created_at'
    )
    list_filter = ('status', 'product', 'delivery_date')  # Додав delivery_date до фільтрів
    search_fields = ('customer_name', 'phone_number', 'email', 'product__name')  # Додав пошук за назвою товару
    readonly_fields = ('created_at', 'updated_at', 'order_date')  # order_date тепер теж readonly
    list_per_page = 20

    fieldsets = (
        ('Інформація про замовника', {
            'fields': ('customer_name', 'phone_number', 'email')
        }),
        ('Деталі замовлення', {
            'fields': ('product', 'quantity',
                       'order_date',  # order_date тут, щоб бачити, але вона readonly
                       'delivery_date', 'comment')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # 'collapse' робить цю секцію згорнутою за замовчуванням
        }),
    )

    # Можна додати сортування за замовчуванням
    ordering = ('-created_at',)
