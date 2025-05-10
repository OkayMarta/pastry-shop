from django import forms
from .models import Order  # Імпорт моделі Order для створення форми на її основі
from django.utils import timezone  # Для роботи з датою та часом, зокрема для встановлення поточної дати


# Визначення форми для створення та редагування замовлень на основі моделі Order
class OrderForm(forms.ModelForm):
    """Форма для створення та валідації даних замовлення."""

    def __init__(self, *args, **kwargs):
        """
        Ініціалізатор форми.
        Встановлює початкове значення для дати доставки та додає CSS-клас 'form-control'
        до всіх полів форми для стилізації за допомогою Bootstrap.
        Також встановлює мінімально допустиму дату для поля 'delivery_date'.
        """
        super().__init__(*args, **kwargs)
        # Встановлення початкового значення для поля 'delivery_date' як поточна дата
        self.fields['delivery_date'].initial = timezone.now().date()

        # Додавання CSS-класу 'form-control' до всіх полів форми
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })
            # Встановлення HTML-атрибуту 'min' для поля 'delivery_date',
            # щоб обмежити вибір дати в минулому на стороні клієнта (в браузері)
            if field_name == 'delivery_date':
                field.widget.attrs.update({'min': timezone.now().date().isoformat()})

    class Meta:
        """
        Мета-клас для конфігурації ModelForm.
        Визначає модель, на основі якої створюється форма, список полів,
        що відображаються, та кастомні віджети для окремих полів.
        """
        model = Order  # Модель, з якою пов'язана форма
        # Список полів моделі, які будуть включені у форму
        fields = ['product', 'quantity', 'delivery_date', 'customer_name',
                  'phone_number', 'email', 'comment']
        # Кастомні віджети для полів форми
        widgets = {
            'delivery_date': forms.DateInput(
                attrs={'type': 'date'},  # Використання HTML5 віджета для вибору дати
                format='%Y-%m-%d'  # Формат дати, що очікується від віджета
            ),
            'comment': forms.Textarea(
                attrs={'rows': 4}  # Встановлення кількості рядків для текстового поля коментаря
            )
        }


    # Загальний метод валідації форми (виконується після індивідуальних clean_<fieldname>() методів)
    def clean(self):
        """
        Загальний метод валідації для форми.
        Перевіряє, чи дата доставки не встановлена в минулому.
        """
        cleaned_data = super().clean()
        delivery_date = cleaned_data.get('delivery_date')

        # Валідація, щоб дата доставки не була в минулому.
        # Ця перевірка дублює логіку в clean_delivery_date.
        # Варто залишити цю логіку тільки в одному місці (переважно в clean_delivery_date).
        if delivery_date and delivery_date < timezone.now().date():
            raise forms.ValidationError(
                "Дата доставки не може бути в минулому."
            )
        return cleaned_data

    # Спеціальний метод для валідації поля 'delivery_date'
    def clean_delivery_date(self):
        """
        Валідація для поля 'delivery_date'.
        Перевіряє, що обрана дата доставки не є датою в минулому.
        """
        delivery_date = self.cleaned_data.get('delivery_date')
        # Перевірка, що дата доставки не раніше поточної дати
        if delivery_date and delivery_date < timezone.now().date():
            raise forms.ValidationError("Дата доставки не може бути в минулому.")

        return delivery_date