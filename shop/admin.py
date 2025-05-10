from django.contrib import admin
from .models import AssortmentItem, Order  # Імпорт моделей для реєстрації в адмін-панелі


# Реєстрація моделі AssortmentItem в адмін-панелі з кастомними налаштуваннями
@admin.register(AssortmentItem)
class AssortmentAdmin(admin.ModelAdmin):
    """Клас для налаштування відображення моделі 'AssortmentItem' (Асортимент) в адмін-панелі Django."""

    list_display = ('name', 'price', 'id') # Поля, що відображаються у списку об'єктів моделі
    search_fields = ('name',) # Поля, за якими можна здійснювати пошук у списку
    list_per_page = 20 # Кількість об'єктів на одній сторінці списку


# Реєстрація моделі Order в адмін-панелі з кастомними налаштуваннями
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Клас для налаштування відображення моделі 'Order' (Замовлення) в адмін-панелі Django."""

    # Поля, що відображаються у списку замовлень
    list_display = (
        'id',  # Ідентифікатор замовлення
        'customer_name',  # Ім'я замовника
        'phone_number',  # Номер телефону замовника
        'email',  # Email замовника
        'product',  # Замовлений товар
        'delivery_date',  # Дата доставки
        'status',  # Статус замовлення
        'created_at'  # Дата та час створення замовлення
    )
    # Поля, за якими можна фільтрувати список замовлень
    list_filter = ('status', 'product', 'delivery_date')
    # Поля, за якими можна здійснювати пошук (включаючи пошук за назвою товару через зв'язок)
    search_fields = ('customer_name', 'phone_number', 'email', 'product__name')
    # Поля, які будуть доступні тільки для читання у формі редагування замовлення
    readonly_fields = ('created_at', 'updated_at', 'order_date')
    # Кількість замовлень на одній сторінці списку
    list_per_page = 20

    # Структурування полів у формі редагування/створення замовлення за допомогою наборів полів (fieldsets)
    fieldsets = (
        # Секція "Інформація про замовника"
        ('Інформація про замовника', {
            'fields': ('customer_name', 'phone_number', 'email')
        }),
        # Секція "Деталі замовлення"
        ('Деталі замовлення', {
            'fields': ('product', 'quantity',
                       'order_date',  # Поле дати замовлення (тільки для читання)
                       'delivery_date', 'comment')
        }),
        # Секція "Статус"
        ('Статус', {
            'fields': ('status',)
        }),
        # Секція "Системна інформація", згорнута за замовчуванням
        ('Системна інформація', {
            'fields': ('created_at', 'updated_at'),  # Поля дати створення та оновлення
            'classes': ('collapse',)  # CSS-клас для згортання секції
        }),
    )

    # Сортування списку замовлень за замовчуванням (від найновіших до найстаріших)
    ordering = ('-created_at',)