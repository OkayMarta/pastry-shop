from django import forms
from .models import Order
from django.utils import timezone

class OrderForm(forms.ModelForm):
    """Форма для створення замовлення"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Встановлюємо мінімальну дату доставки як сьогодні (order_date видалено)
        # self.fields['order_date'].initial = timezone.now().date() # Цей рядок більше не потрібен
        self.fields['delivery_date'].initial = timezone.now().date()

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                # 'placeholder': self.fields[field].label # Можливо, плейсхолдери краще прибрати, якщо є labels
            })
            # Для дати доставки можна встановити мінімальну дату
            if field == 'delivery_date':
                 self.fields[field].widget.attrs.update({'min': timezone.now().date().isoformat()})

    class Meta:
        model = Order
        fields = ['product', 'quantity', # 'order_date' видалено звідси
                  'delivery_date', 'customer_name', 'phone_number',
                  'email', 'comment']
        widgets = {
            # 'order_date': forms.DateInput( # Віджет для order_date більше не потрібен
            #     attrs={'type': 'date'},
            #     format='%Y-%m-%d'
            # ),
            'delivery_date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
            'comment': forms.Textarea(
                attrs={'rows': 4}
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        # order_date = cleaned_data.get('order_date') # order_date більше не буде в cleaned_data з форми
        delivery_date = cleaned_data.get('delivery_date')

        # Тепер order_date буде встановлюватися у view,
        # тому валідацію order_date > delivery_date потрібно буде робити
        # з урахуванням того, що order_date - це timezone.now().date()
        # або перенести цю логіку в метод clean_delivery_date, якщо можливо

        # Прибираємо валідацію, пов'язану з order_date, яка береться з форми
        # if order_date and delivery_date:
        #     if order_date > delivery_date:
        #         raise forms.ValidationError(
        #             "Дата доставки не може бути раніше дати замовлення"
        #         )
        #     if order_date < timezone.now().date(): # Це теж більше не актуально для поля форми
        #         raise forms.ValidationError(
        #             "Дата замовлення не може бути в минулому"
        #         )

        # Залишаємо валідацію для delivery_date, якщо потрібно
        if delivery_date and delivery_date < timezone.now().date():
            raise forms.ValidationError(
                "Дата доставки не може бути в минулому."
            )
        return cleaned_data

    # Опціонально, для більш чистої валідації дати доставки:
    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        if delivery_date and delivery_date < timezone.now().date():
            raise forms.ValidationError("Дата доставки не може бути в минулому.")
        # Якщо у вас є логіка, що дата доставки має бути не раніше сьогоднішньої дати + X днів,
        # додайте її тут.
        return delivery_date