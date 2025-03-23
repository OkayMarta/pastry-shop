from django import forms
from .models import Order
from django.utils import timezone

class OrderForm(forms.ModelForm):
    """Форма для створення замовлення"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Встановлюємо мінімальну дату замовлення як сьогодні
        self.fields['order_date'].initial = timezone.now().date()
        self.fields['delivery_date'].initial = timezone.now().date()

        # Додаємо CSS класи для стилізації
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })

    class Meta:
        model = Order
        fields = ['product', 'quantity', 'order_date',
                  'delivery_date', 'customer_name', 'phone_number',
                  'email', 'comment']
        widgets = {
            'order_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'delivery_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'comment': forms.Textarea(
                attrs={'rows': 4}
            )
        }

    def clean(self):
        """Валідація форми"""
        cleaned_data = super().clean()
        order_date = cleaned_data.get('order_date')
        delivery_date = cleaned_data.get('delivery_date')

        if order_date and delivery_date:
            if order_date > delivery_date:
                raise forms.ValidationError(
                    "Дата доставки не може бути раніше дати замовлення"
                )

            if order_date < timezone.now().date():
                raise forms.ValidationError(
                    "Дата замовлення не може бути в минулому"
                )

        return cleaned_data