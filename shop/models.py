from django.db import models
from django.core.validators import RegexValidator  # Імпорт валідатора для регулярних виразів


# Модель для представлення одиниці асортименту кондитерських виробів
class AssortmentItem(models.Model):
    """Модель, що представляє товар в асортименті кондитерської."""
    name = models.CharField(max_length=100, verbose_name="Назва виробу")  # Назва товару
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")  # Ціна товару
    # Поле для зображення товару. Зображення завантажуються в папку 'media/assortment/'.
    # blank=True та null=True означають, що поле не є обов'язковим.
    image = models.ImageField(upload_to='assortment/', verbose_name="Зображення", blank=True, null=True)

    # Стандартний менеджер моделі Django. Дозволяє виконувати запити до бази даних.
    objects = models.Manager()

    def __str__(self):
        """Повертає рядкове представлення об'єкта моделі (назва товару)."""
        return self.name

    class Meta:
        """Мета-клас для налаштування моделі."""
        verbose_name = "Асортимент"  # Назва моделі в однині для адмін-панелі та інших місць
        verbose_name_plural = "Асортимент"  # Назва моделі у множині
        # (Примітка: 'Асортимент' в однині та множині може бути не зовсім коректно лінгвістично,
        # можливо, краще "Товар асортименту" / "Товари асортименту" або "Позиція асортименту" / "Позиції асортименту")


# Модель для представлення замовлення, зробленого клієнтом
class Order(models.Model):
    """Модель для зберігання інформації про замовлення клієнтів."""

    # Визначення можливих статусів замовлення
    STATUS_CHOICES = [
        ('новий', 'Новий'),
        ('прийнято', 'Прийнято'),
        ('виконується', 'Виконується'),
        ('готово', 'Готово'),
        ('доставлено', 'Доставлено'),
    ]

    # Зв'язок із моделлю AssortmentItem (один товар може бути у багатьох замовленнях).
    # on_delete=models.PROTECT запобігає видаленню товару, якщо на нього є замовлення.
    product = models.ForeignKey(AssortmentItem, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Кількість")  # Кількість замовленого товару
    order_date = models.DateField(
        verbose_name="Дата замовлення")  # Дата, на яку оформлено замовлення (встановлюється у view)
    delivery_date = models.DateField(verbose_name="Дата доставки")  # Бажана дата доставки
    customer_name = models.CharField(max_length=100, verbose_name="Ім'я замовника")  # Ім'я клієнта

    # Валідатор для формату номера телефону
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  # Регулярний вираз для перевірки номера
        message="Номер телефону повинен бути в форматі: '+999999999'. До 15 цифр."  # Повідомлення про помилку
    )
    phone_number = models.CharField(
        validators=[phone_regex],  # Застосування валідатора до поля
        max_length=17,  # Максимальна довжина рядка для номера телефону
        verbose_name="Номер телефону"
    )
    email = models.EmailField(verbose_name="Email замовника")  # Email клієнта
    comment = models.TextField(verbose_name="Коментар", blank=True)  # Коментар до замовлення (необов'язкове поле)

    # Статус замовлення, вибирається зі списку STATUS_CHOICES
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,  # Використання визначених варіантів статусу
        default='новий',  # Статус замовлення за замовчуванням
        verbose_name="Статус замовлення"
    )
    # Дата та час створення запису про замовлення (встановлюється автоматично при створенні)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    # Дата та час останнього оновлення запису про замовлення (оновлюється автоматично при збереженні)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        """Повертає рядкове представлення об'єкта замовлення."""
        return f"Замовлення №{self.id} від {self.customer_name}"

    class Meta:
        """Мета-клас для налаштування моделі."""
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['-created_at']  # Сортування замовлень за замовчуванням (спочатку найновіші)