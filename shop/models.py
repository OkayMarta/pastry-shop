from django.db import models
from django.core.validators import RegexValidator


class AssortmentItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва виробу")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='assortment/', verbose_name="Зображення", blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Асортимент"
        verbose_name_plural = "Асортимент"


class Order(models.Model):
    """Модель для зберігання замовлень"""
    STATUS_CHOICES = [
        ('новий', 'Новий'),
        ('прийнято', 'Прийнято'),
        ('виконується', 'Виконується'),
        ('готово', 'Готово'),
        ('доставлено', 'Доставлено'),
    ]

    product = models.ForeignKey(AssortmentItem, on_delete=models.PROTECT, verbose_name="Товар", null=True, blank=True)
    quantity = models.PositiveIntegerField(verbose_name="Кількість")
    order_date = models.DateField(verbose_name="Дата замовлення")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    customer_name = models.CharField(max_length=100, verbose_name="Ім'я замовника")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефону повинен бути в форматі: '+999999999'. До 15 цифр."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name="Номер телефону"
    )
    email = models.EmailField(verbose_name="Email замовника")
    comment = models.TextField(verbose_name="Коментар", blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='новий',
        verbose_name="Статус замовлення"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return f"Замовлення №{self.id} від {self.customer_name}"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['-created_at']
